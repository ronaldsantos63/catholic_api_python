from flask import jsonify, request

from adapter.logging_adapter import HostLoggerAdapter


class ExceptionLoggingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except Exception as e:
            headers = {key: value for key, value in request.headers}
            self.app.logger.exception(f'Unhandled exception: {e}\nHeaders: {headers}', exc_info=True)
            response = jsonify(error="Internal Server Error", message=str(e))
            start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
            return [response.data]
