import logging


class HostLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f'RemoteAddr: {self.extra["remote_addr"]} - {msg}', kwargs
