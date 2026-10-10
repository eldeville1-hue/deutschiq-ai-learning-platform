"""Real HTTP authentication regression for personalized learning routes."""
import hashlib
import hmac
import json
import time
import unittest
from unittest.mock import patch
from urllib.parse import urlencode

from fastapi.testclient import TestClient

from app.api.endpoints.learning import router as learning_router
from app.api.endpoints.plan import router as plan_router
from app.core.config import settings
from fastapi import FastAPI


def signed_init_data(user_id, token, auth_date=None):
    fields = {
        "auth_date": str(auth_date or int(time.time())),
        "user": json.dumps({"id": user_id}, separators=(",", ":")),
    }
    check = "\n".join(f"{key}={fields[key]}" for key in sorted(fields))
    secret = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
    fields["hash"] = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    return urlencode(fields)


class TelegramPersonalizationHttpTests(unittest.TestCase):
    def setUp(self):
        app = FastAPI()
        app.include_router(learning_router)
        app.include_router(plan_router)
        self.client = TestClient(app)
        self.token = "integration-test-bot-token"

    def test_missing_telegram_auth_rejected_on_both_routes(self):
        for route in ("/api/learning/today/9002", "/api/plan/9002"):
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(401, response.status_code)

    def test_valid_signature_cannot_access_another_learner(self):
        with patch.object(settings, "BOT_TOKEN", self.token), patch.object(settings, "DEBUG", False):
            headers = {"X-Telegram-Init-Data": signed_init_data(9001, self.token)}
            for route in ("/api/learning/today/9002", "/api/plan/9002"):
                with self.subTest(route=route):
                    response = self.client.get(route, headers=headers)
                    self.assertEqual(403, response.status_code)
                    self.assertEqual("User identity mismatch", response.json()["detail"])

    def test_invalid_signature_rejected_before_owner_check(self):
        with patch.object(settings, "BOT_TOKEN", self.token), patch.object(settings, "DEBUG", False):
            headers = {"X-Telegram-Init-Data": signed_init_data(9001, "wrong-bot-token")}
            for route in ("/api/learning/today/9001", "/api/plan/9001"):
                with self.subTest(route=route):
                    response = self.client.get(route, headers=headers)
                    self.assertEqual(401, response.status_code)


if __name__ == "__main__":
    unittest.main()
