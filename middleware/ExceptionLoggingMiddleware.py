from flask import jsonify


class ExceptionLoggingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except Exception as e:
            self.app.logger.exception(f'Unhandled exception: {e}', exc_info=True)
            response = jsonify(error="Internal Server Error", message=str(e))
            start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
            return [response.data]
