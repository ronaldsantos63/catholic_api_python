import unittest

from middleware.security import sanitize_headers


class SecurityHelpersTest(unittest.TestCase):
    def test_sanitize_headers_redacts_sensitive_values(self):
        headers = {
            "Authorization": "Bearer secret",
            "Cookie": "session=secret",
            "X-Api-Key": "secret",
            "User-Agent": "test-client",
        }

        sanitized = sanitize_headers(headers)

        self.assertEqual(sanitized["Authorization"], "[REDACTED]")
        self.assertEqual(sanitized["Cookie"], "[REDACTED]")
        self.assertEqual(sanitized["X-Api-Key"], "[REDACTED]")
        self.assertEqual(sanitized["User-Agent"], "test-client")


if __name__ == "__main__":
    unittest.main()
