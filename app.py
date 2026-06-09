import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request, render_template
from flask_restful import Api, Resource

from adapter.logging_adapter import HostLoggerAdapter
from extractor.config import Config
from extractor.exceptions import ExternalSourceError, InvalidLiturgySourceError, LiturgyNotFoundError
from extractor.extractor_service import ExtractorService
from extractor.utils import Utils
from middleware.ExceptionLoggingMiddleware import ExceptionLoggingMiddleware
from middleware.security import RateLimiter, sanitize_headers

app = Flask(__name__)
api = Api(app)
rate_limiter = RateLimiter()


def get_bool_env(name, default=False):
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in ("1", "true", "yes", "on")


def get_int_env(name, default):
    try:
        value = int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default
    return value if value > 0 else default


app.config.update(
    API_KEY=os.getenv("CATHOLIC_API_KEY"),
    MAX_CONTENT_LENGTH=get_int_env("MAX_CONTENT_LENGTH", 1024),
    RATE_LIMIT_ENABLED=get_bool_env("RATE_LIMIT_ENABLED", True),
    RATE_LIMIT_REQUESTS=get_int_env("RATE_LIMIT_REQUESTS", 120),
    RATE_LIMIT_WINDOW_SECONDS=get_int_env("RATE_LIMIT_WINDOW_SECONDS", 60),
    SECURITY_HSTS_ENABLED=get_bool_env("SECURITY_HSTS_ENABLED", False),
)

# Configuração básica de logging
if os.getenv('FLASK_ENV') != 'development':
    # Configuração de logging em produção
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
else:
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: - %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)

app.logger.handlers.clear()
app.logger.addHandler(handler)
if os.getenv('FLASK_ENV') != 'development':
    app.logger.setLevel(logging.INFO)

app.wsgi_app = ExceptionLoggingMiddleware(app.wsgi_app, app.logger)


def json_error(message, status_code):
    response = jsonify(error=message)
    response.status_code = status_code
    return response


def client_identifier():
    return request.remote_addr or "unknown"


class DailyLurgy(Resource):
    def get(self):
        try:
            period = Utils.normalize_period(request.headers.get('period', None))
            config = Config()
            extractor_service = ExtractorService(config)
            scrapy = extractor_service.daily_liturgy_markdown(period)
            return jsonify(scrapy)
        except ValueError as e:
            return json_error(str(e), 400)
        except LiturgyNotFoundError as e:
            return json_error(str(e), 404)
        except ExternalSourceError as e:
            period = request.headers.get('period', None)
            HostLoggerAdapter(app.logger, extra=dict(remote_addr=request.remote_addr)).warning(
                "External liturgy source failed for period: %s", period, exc_info=True)
            return json_error(str(e), 503)
        except InvalidLiturgySourceError as e:
            period = request.headers.get('period', None)
            HostLoggerAdapter(app.logger, extra=dict(remote_addr=request.remote_addr)).error(
                "Unexpected liturgy source structure for period: %s", period, exc_info=True)
            return json_error(str(e), 502)
        except Exception:
            period = request.headers.get('period', None)
            HostLoggerAdapter(app.logger, extra=dict(remote_addr=request.remote_addr)).error(
                "Unexpected error while scraping liturgy for period: %s", period, exc_info=True)
            return json_error('Internal Server Error', 500)


api.add_resource(DailyLurgy, "/liturgy", endpoint="liturgy")


@app.before_request
def enforce_security_controls():
    if request.content_length and request.content_length > app.config["MAX_CONTENT_LENGTH"]:
        return json_error("Request payload too large", 413)

    api_key = app.config.get("API_KEY")
    if api_key and request.endpoint not in ("hello_world", "privacy", "static"):
        supplied_key = request.headers.get("X-API-Key")
        if supplied_key != api_key:
            return json_error("Unauthorized", 401)

    if app.config["RATE_LIMIT_ENABLED"]:
        allowed, retry_after, remaining = rate_limiter.check(
            client_identifier(),
            app.config["RATE_LIMIT_REQUESTS"],
            app.config["RATE_LIMIT_WINDOW_SECONDS"],
        )
        if not allowed:
            response = json_error("Too many requests", 429)
            response.headers["Retry-After"] = str(retry_after)
            return response
        request.rate_limit_remaining = remaining


@app.before_request
def log_request_info():
    request_host = request.remote_addr
    HostLoggerAdapter(app.logger, {'remote_addr': request_host}).info(
        '%s %s\nHeaders:\n%s',
        request.method,
        request.path,
        sanitize_headers(dict(request.headers)))


@app.after_request
def add_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")

    if request.path == "/privacy":
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")
    else:
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")

    if app.config["SECURITY_HSTS_ENABLED"]:
        response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")

    if hasattr(request, "rate_limit_remaining"):
        response.headers.setdefault("X-RateLimit-Remaining", str(request.rate_limit_remaining))

    return response


@app.route("/")
def hello_world():
    return "<h1>Catholic Api</h1>"


@app.route("/privacy")
def privacy():
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run()
