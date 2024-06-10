import logging


class HostLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f'Host: {self.extra["host"]} - {msg}', kwargs
