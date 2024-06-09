from flask import Flask, jsonify, request, render_template
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


@app.route("/")
def hello_world():
    return "<h1>Catholic Api</h1>";


@app.route("/privacy")
def privacy():
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run()
