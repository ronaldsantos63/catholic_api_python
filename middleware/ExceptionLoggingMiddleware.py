import json

from middleware.security import sanitize_headers


class ExceptionLoggingMiddleware:
    def __init__(self, app, logger=None):
        self.app = app
        self.logger = logger

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except Exception as e:
            headers = self.__headers_from_environ(environ)
            if self.logger:
                self.logger.exception("Unhandled WSGI exception: %s\nHeaders: %s", e, headers)

            body = json.dumps({"error": "Internal Server Error"}).encode("utf-8")
            start_response(
                "500 Internal Server Error",
                [
                    ("Content-Type", "application/json"),
                    ("Content-Length", str(len(body))),
                    ("X-Content-Type-Options", "nosniff"),
                    ("X-Frame-Options", "DENY"),
                    ("Referrer-Policy", "no-referrer"),
                ],
            )
            return [body]

    @staticmethod
    def __headers_from_environ(environ):
        headers = {}
        for key, value in environ.items():
            if key.startswith("HTTP_"):
                header_name = key[5:].replace("_", "-").title()
                headers[header_name] = value
        return sanitize_headers(headers)
