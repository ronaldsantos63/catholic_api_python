import time
from collections import defaultdict, deque
from threading import Lock
from typing import Mapping, Tuple


SENSITIVE_HEADER_NAMES = {
    "authorization",
    "cookie",
    "proxy-authorization",
    "set-cookie",
    "x-api-key",
    "x-auth-token",
    "x-csrf-token",
}


def sanitize_headers(headers: Mapping[str, str]) -> dict:
    sanitized = {}
    for key, value in headers.items():
        normalized = key.lower()
        if normalized in SENSITIVE_HEADER_NAMES or "token" in normalized or "secret" in normalized:
            sanitized[key] = "[REDACTED]"
        else:
            sanitized[key] = value
    return sanitized


class RateLimiter:
    def __init__(self):
        self._requests = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str, limit: int, window_seconds: int) -> Tuple[bool, int, int]:
        now = time.monotonic()
        window_start = now - window_seconds

        with self._lock:
            request_times = self._requests[key]
            while request_times and request_times[0] < window_start:
                request_times.popleft()

            if len(request_times) >= limit:
                retry_after = max(1, int(window_seconds - (now - request_times[0])) + 1)
                return False, retry_after, 0

            request_times.append(now)
            remaining = max(0, limit - len(request_times))
            return True, 0, remaining

    def clear(self):
        with self._lock:
            self._requests.clear()

