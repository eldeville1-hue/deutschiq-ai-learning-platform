import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import patch

from app.services.subscription import has_active_pro, monthly_invoice_payload, subscription_payload, validate_pre_checkout


class SubscriptionTests(unittest.TestCase):
    def test_active_monthly_plan(self):
        user = SimpleNamespace(subscription_status="pro", subscription_end_date=datetime.now(timezone.utc) + timedelta(days=3))
        self.assertTrue(has_active_pro(user))
        self.assertEqual(subscription_payload(user)["subscription_status"], "pro")

    def test_expired_plan_is_free(self):
        user = SimpleNamespace(subscription_status="pro", subscription_end_date=datetime.now(timezone.utc) - timedelta(seconds=1))
        self.assertFalse(has_active_pro(user))
        payload = subscription_payload(user)
        self.assertEqual(payload["subscription_status"], "free")
        self.assertIsNone(payload["subscription_end_date"])
        self.assertIn("payments_enabled", payload)
        self.assertIn("pro_price_stars", payload)

    def test_invoice_payload_is_bound_to_telegram_user(self):
        self.assertEqual(monthly_invoice_payload(123), "deutschiq:pro_monthly:123")

    def test_checkout_is_rejected_while_payments_are_disabled(self):
        query = SimpleNamespace(
            from_user=SimpleNamespace(id=123),
            invoice_payload=monthly_invoice_payload(123),
            currency="XTR",
            total_amount=700,
        )
        with patch("app.services.subscription.settings.PAYMENTS_ENABLED", False):
            self.assertEqual(validate_pre_checkout(query), "Payments are not available yet.")

    def test_checkout_rejects_another_users_invoice(self):
        query = SimpleNamespace(
            from_user=SimpleNamespace(id=123),
            invoice_payload=monthly_invoice_payload(456),
            currency="XTR",
            total_amount=700,
        )
        with patch("app.services.subscription.settings.PAYMENTS_ENABLED", True), patch("app.services.subscription.settings.PRO_PRICE_STARS", 700):
            self.assertIn("another account", validate_pre_checkout(query))

    def test_checkout_accepts_current_stars_price(self):
        query = SimpleNamespace(
            from_user=SimpleNamespace(id=123),
            invoice_payload=monthly_invoice_payload(123),
            currency="XTR",
            total_amount=700,
        )
        with patch("app.services.subscription.settings.PAYMENTS_ENABLED", True), patch("app.services.subscription.settings.PRO_PRICE_STARS", 700):
            self.assertIsNone(validate_pre_checkout(query))

    def test_free_plan(self):
        user = SimpleNamespace(subscription_status="free", subscription_end_date=None)
        self.assertFalse(has_active_pro(user))


if __name__ == "__main__":
    unittest.main()
