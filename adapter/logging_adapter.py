import logging
from typing import Any, MutableMapping, Tuple


class HostLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg: str, kwargs: MutableMapping[str, Any]) -> Tuple[str, MutableMapping[str, Any]]:
        extra = self.extra or {}
        remote_addr = extra.get("remote_addr", "unknown")
        return f'RemoteAddr: {remote_addr} - {msg}', kwargs
