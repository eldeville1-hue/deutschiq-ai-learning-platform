import unittest
from datetime import datetime
from types import SimpleNamespace

from app.services.beta_insights import exercise_health, summarize_events


class BetaInsightsTests(unittest.TestCase):
    def test_event_summary_is_aggregated_and_feedback_has_no_user_id(self):
        now = datetime.now()
        events = [
            SimpleNamespace(user_id=7, event_name="exercise_answered", properties={"learning_mode": "supported", "correct": True}, created_at=now),
            SimpleNamespace(user_id=8, event_name="exercise_answered", properties={"learning_mode": "supported", "correct": False}, created_at=now),
            SimpleNamespace(user_id=7, event_name="api_failed", properties={"path": "/api/plan"}, created_at=now),
            SimpleNamespace(user_id=7, event_name="beta_feedback", properties={"message": "Clear lesson", "language": "en", "page": "/lesson/1"}, created_at=now),
        ]
        summary = summarize_events(events)
        self.assertEqual(50, summary["learning_modes"][0]["accuracy"])
        self.assertEqual(1, summary["reliability"]["api_failed"])
        self.assertNotIn("user_id", summary["feedback"][0])

    def test_exercise_health_flags_only_after_enough_attempts(self):
        hard = [SimpleNamespace(lesson_id=3, exercise_index=1, user_id=index, correct=index == 0) for index in range(6)]
        sparse = [SimpleNamespace(lesson_id=4, exercise_index=0, user_id=1, correct=False)]
        rows = exercise_health([*hard, *sparse], {3: "dative", 4: "articles"})
        self.assertEqual("too_hard", rows[0]["status"])
        self.assertEqual("healthy", rows[1]["status"])


if __name__ == "__main__":
    unittest.main()
