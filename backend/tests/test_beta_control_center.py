import unittest
from datetime import datetime
from types import SimpleNamespace

from app.services.beta_insights import tester_alias, tester_progress


class BetaControlCenterTests(unittest.TestCase):
    def test_alias_is_stable_and_does_not_expose_database_id(self):
        alias = tester_alias(123456, "test-secret")
        self.assertEqual(alias, tester_alias(123456, "test-secret"))
        self.assertTrue(alias.startswith("T-"))
        self.assertNotIn("123456", alias)

    def test_tester_progress_connects_journey_without_telegram_identity(self):
        now = datetime.now()
        enrollment = SimpleNamespace(user_id=7, invite_id=3, joined_at=now, consent=True, goal="conversation")
        user = SimpleNamespace(id=7, language_code="de", diagnostic_completed=True)
        invite = SimpleNamespace(id=3, label="Beta tester 01")
        sessions = [
            SimpleNamespace(user_id=7, status="passed", started_at=now),
            SimpleNamespace(user_id=7, status="active", started_at=now),
        ]
        events = [SimpleNamespace(user_id=7, event_name="beta_feedback", created_at=now)]

        result = tester_progress([enrollment], [user], [invite], sessions, events, "test-secret")[0]

        self.assertEqual("Beta tester 01", result["invite"])
        self.assertEqual(2, result["lessons_started"])
        self.assertEqual(1, result["lessons_completed"])
        self.assertEqual(1, result["feedback_count"])
        self.assertNotIn("user_id", result)


if __name__ == "__main__":
    unittest.main()
