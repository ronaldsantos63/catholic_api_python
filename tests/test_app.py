import unittest
from unittest.mock import patch

from app import app, rate_limiter


class AppSecurityTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["API_KEY"] = None
        app.config["RATE_LIMIT_ENABLED"] = True
        app.config["RATE_LIMIT_REQUESTS"] = 120
        app.config["RATE_LIMIT_WINDOW_SECONDS"] = 60
        rate_limiter.clear()
        self.client = app.test_client()

    def test_invalid_period_returns_400(self):
        response = self.client.get("/liturgy", headers={"period": "31/02/2026"})
        body = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(body)
        self.assertEqual(body["error"], "period must use dd/mm/yyyy and be a valid date")

    def test_liturgy_success_adds_security_headers(self):
        payload = {
            "date_string": {"day": "08", "month": "Jun", "year": "2026"},
            "date": "08/06/2026",
            "color": "Verde",
            "entry_title": "Teste",
            "readings": {},
        }

        with patch("app.ExtractorService") as service_class:
            service_class.return_value.daily_liturgy_markdown.return_value = payload
            response = self.client.get("/liturgy", headers={"period": "08/06/2026"})
        body = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body, payload)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertIn("Content-Security-Policy", response.headers)

    def test_optional_api_key_blocks_liturgy_when_configured(self):
        app.config["API_KEY"] = "secret"

        unauthorized = self.client.get("/liturgy", headers={"period": "08/06/2026"})
        self.assertEqual(unauthorized.status_code, 401)

        with patch("app.ExtractorService") as service_class:
            service_class.return_value.daily_liturgy_markdown.return_value = {"readings": {}}
            authorized = self.client.get(
                "/liturgy",
                headers={"period": "08/06/2026", "X-API-Key": "secret"},
            )

        self.assertEqual(authorized.status_code, 200)

    def test_rate_limit_returns_429(self):
        app.config["RATE_LIMIT_REQUESTS"] = 1

        first = self.client.get("/")
        second = self.client.get("/")

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 429)
        self.assertIn("Retry-After", second.headers)


if __name__ == "__main__":
    unittest.main()
