import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request, render_template, current_app
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
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: - %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

app.wsgi_app = ExceptionLoggingMiddleware(app.wsgi_app)


class DailyLurgy(Resource):
    def get(self):
        try:
            period = request.headers.get('period', None)

            app.logger.info(f"searching liturgy by period: {request.headers.get('period', default=None)}")

            config = Config()
            extractor_service = ExtractorService(config)
            scrapy = extractor_service.daily_liturgy_markdown(period)
            return jsonify(scrapy)
        except Exception as e:
            period = request.headers.get('period', None)
            app.logger.error(f"An unexpected error occurred while scraping the liturgy for the period: %s",
                             period, exc_info=e)
            response = jsonify(error=f'No liturgy found for the period: {period}')
            response.status_code = 404
            return response


api.add_resource(DailyLurgy, "/liturgy", endpoint="liturgy")


@app.before_request
def log_request_info():
    request_host = request.host
    HostLoggerAdapter(app.logger, {'host': request_host}).info('Request received')


@app.route("/")
def hello_world():
    return "<h1>Catholic Api</h1>";


@app.route("/privacy")
def privacy():
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run()
