from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from extractor.config import Config
from extractor.extractor_service import ExtractorService

app = Flask(__name__)
api = Api(app)


class DailyLurgy(Resource):
    def get(self):
        period = request.headers.get('period', None)

        config = Config()
        extractor_service = ExtractorService(config)
        scrapy = extractor_service.daily_liturgy_markdown(period)
        return jsonify(scrapy)


api.add_resource(DailyLurgy, "/liturgy", endpoint="liturgy")


if __name__ == '__main__':
    app.run()
