import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request, render_template
from flask_restful import Api, Resource

from adapter.logging_adapter import HostLoggerAdapter
from extractor.config import Config
from extractor.extractor_service import ExtractorService
from middleware.ExceptionLoggingMiddleware import ExceptionLoggingMiddleware

app = Flask(__name__)
api = Api(app)

# Configuração básica de logging
if os.getenv('FLASK_ENV') != 'development':
    # Configuração de logging em produção
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
else:
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: - %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)

app.logger.handlers.clear()
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

app.wsgi_app = ExceptionLoggingMiddleware(app.wsgi_app)


class DailyLurgy(Resource):
    def get(self):
        try:
            period = request.headers.get('period', None)
            config = Config()
            extractor_service = ExtractorService(config)
            scrapy = extractor_service.daily_liturgy_markdown(period)
            return jsonify(scrapy)
        except Exception as e:
            period = request.headers.get('period', None)
            HostLoggerAdapter(app.logger, extra=dict(remote_addr=request.remote_addr)).error(f"An unexpected error occurred while scraping the liturgy for the period: %s",
                             period, exc_info=e)
            response = jsonify(error=f'No liturgy found for the period: {period}')
            response.status_code = 404
            return response


api.add_resource(DailyLurgy, "/liturgy", endpoint="liturgy")


@app.before_request
def log_request_info():
    request_host = request.remote_addr
    HostLoggerAdapter(app.logger, {'remote_addr': request_host}).info(
        f'{request.method} {request.full_path}\nHeaders:\n{request.headers}')


@app.route("/")
def hello_world():
    return "<h1>Catholic Api</h1>";


@app.route("/privacy")
def privacy():
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run()
