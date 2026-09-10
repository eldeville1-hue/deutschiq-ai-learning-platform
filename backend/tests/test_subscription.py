import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.services.subscription import has_active_pro, subscription_payload


class SubscriptionTests(unittest.TestCase):
    def test_active_monthly_plan(self):
        user = SimpleNamespace(subscription_status="pro", subscription_end_date=datetime.now(timezone.utc) + timedelta(days=3))
        self.assertTrue(has_active_pro(user))
        self.assertEqual(subscription_payload(user)["subscription_status"], "pro")

    def test_expired_plan_is_free(self):
        user = SimpleNamespace(subscription_status="pro", subscription_end_date=datetime.now(timezone.utc) - timedelta(seconds=1))
        self.assertFalse(has_active_pro(user))
        self.assertEqual(subscription_payload(user), {"subscription_status": "free", "subscription_end_date": None})

    def test_free_plan(self):
        user = SimpleNamespace(subscription_status="free", subscription_end_date=None)
        self.assertFalse(has_active_pro(user))


if __name__ == "__main__":
    unittest.main()
