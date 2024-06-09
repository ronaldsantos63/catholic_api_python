import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request, render_template
from flask_restful import Api, Resource

from extractor.config import Config
from extractor.extractor_service import ExtractorService
from middleware.ExceptionLoggingMiddleware import ExceptionLoggingMiddleware

app = Flask(__name__)
api = Api(app)

# Configuração básica de logging
if not app.debug:
    # Configuração de logging em produção
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

app.wsgi_app = ExceptionLoggingMiddleware(app.wsgi_app)


class DailyLurgy(Resource):
    def get(self):
        period: str | None = None
        if request.headers:
            period = request.headers.get('period', None)

        config = Config()
        extractor_service = ExtractorService(config)
        scrapy = extractor_service.daily_liturgy_markdown(period)
        return jsonify(scrapy)


api.add_resource(DailyLurgy, "/liturgy", endpoint="liturgy")


@app.route("/")
def hello_world():
    return "<h1>Catholic Api</h1>";


@app.route("/privacy")
def privacy():
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run()
