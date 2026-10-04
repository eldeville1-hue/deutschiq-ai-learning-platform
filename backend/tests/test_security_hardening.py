import hashlib
import hmac
import json
import unittest
from types import SimpleNamespace
from urllib.parse import urlencode
from unittest.mock import patch

from fastapi import HTTPException

from app.core.security import SECURITY_HEADERS, apply_security_headers
from app.core.telegram_auth import verify_telegram_init_data


def signed_init_data(bot_token: str, user_id: int, auth_date: int) -> str:
    values = {"auth_date": str(auth_date), "query_id": "test-query", "user": json.dumps({"id": user_id}, separators=(",", ":"))}
    check = "\n".join(f"{key}={values[key]}" for key in sorted(values))
    secret = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    values["hash"] = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    return urlencode(values)


class SecurityHardeningTests(unittest.TestCase):
    def test_current_signed_telegram_session_is_accepted(self):
        token = "123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"
        payload = signed_init_data(token, 9981, 1_000_000)
        with patch("app.core.telegram_auth.settings.BOT_TOKEN", token), patch(
            "app.core.telegram_auth.settings.TELEGRAM_AUTH_MAX_AGE_SECONDS", 3600
        ):
            self.assertEqual(9981, verify_telegram_init_data(payload, now=1_003_000))

    def test_expired_signed_telegram_session_is_rejected(self):
        token = "123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"
        payload = signed_init_data(token, 9981, 1_000_000)
        with patch("app.core.telegram_auth.settings.BOT_TOKEN", token), patch(
            "app.core.telegram_auth.settings.TELEGRAM_AUTH_MAX_AGE_SECONDS", 3600
        ):
            with self.assertRaises(HTTPException) as raised:
                verify_telegram_init_data(payload, now=1_003_601)
        self.assertEqual(401, raised.exception.status_code)
        self.assertEqual("Telegram session expired", raised.exception.detail)

    def test_future_dated_session_is_rejected(self):
        token = "123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"
        payload = signed_init_data(token, 9981, 1_000_031)
        with patch("app.core.telegram_auth.settings.BOT_TOKEN", token):
            with self.assertRaises(HTTPException):
                verify_telegram_init_data(payload, now=1_000_000)

    def test_tampered_session_is_rejected_before_age_check(self):
        token = "123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"
        payload = signed_init_data(token, 9981, 1_000_000).replace("9981", "9982")
        with patch("app.core.telegram_auth.settings.BOT_TOKEN", token):
            with self.assertRaises(HTTPException) as raised:
                verify_telegram_init_data(payload, now=1_000_001)
        self.assertEqual("Invalid Telegram signature", raised.exception.detail)

    def test_security_headers_include_hsts_only_for_https(self):
        insecure = SimpleNamespace(headers={})
        secure = SimpleNamespace(headers={})
        apply_security_headers(insecure, secure=False)
        apply_security_headers(secure, secure=True)
        self.assertEqual(SECURITY_HEADERS, insecure.headers)
        self.assertIn("Strict-Transport-Security", secure.headers)
        self.assertEqual("nosniff", secure.headers["X-Content-Type-Options"])


if __name__ == "__main__":
    unittest.main()
