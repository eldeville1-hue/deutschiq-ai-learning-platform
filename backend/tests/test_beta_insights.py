import unittest
from datetime import datetime, timedelta
from types import SimpleNamespace

from app.services.beta_acceptance import acceptance_report
from app.services.beta_insights import beta_readiness, exercise_health, lesson_content_health, retention_cohorts, summarize_events


class BetaInsightsTests(unittest.TestCase):
    def test_event_summary_is_aggregated_and_feedback_has_no_user_id(self):
        now = datetime.now()
        events = [
            SimpleNamespace(user_id=7, event_name="exercise_answered", properties={"learning_mode": "supported", "correct": True}, created_at=now),
            SimpleNamespace(user_id=8, event_name="exercise_answered", properties={"learning_mode": "supported", "correct": False}, created_at=now),
            SimpleNamespace(user_id=7, event_name="api_failed", properties={"path": "/api/plan"}, created_at=now),
            SimpleNamespace(user_id=7, event_name="audio_failed", properties={"lesson_id": 1}, created_at=now),
            SimpleNamespace(user_id=7, event_name="offline_recovered", properties={"page": "/lesson/1"}, created_at=now),
            SimpleNamespace(user_id=7, event_name="beta_feedback", properties={"message": "Clear lesson", "language": "en", "page": "/lesson/1", "category": "unclear", "lesson_id": 1, "exercise_index": 2, "exercise_type": "reorder", "topic": "word_order"}, created_at=now),
        ]
        summary = summarize_events(events)
        self.assertEqual(50, summary["learning_modes"][0]["accuracy"])
        self.assertEqual(1, summary["reliability"]["api_failed"])
        self.assertEqual(1, summary["reliability"]["audio_failed"])
        self.assertEqual(1, summary["recovery"]["offline_recovered"])
        self.assertNotIn("user_id", summary["feedback"][0])
        self.assertEqual("word_order", summary["feedback"][0]["topic"])
        self.assertEqual(2, summary["feedback"][0]["exercise_index"])

    def test_exercise_health_flags_only_after_enough_attempts(self):
        hard = [SimpleNamespace(lesson_id=3, exercise_index=1, user_id=index, correct=index == 0) for index in range(6)]
        sparse = [SimpleNamespace(lesson_id=4, exercise_index=0, user_id=1, correct=False)]
        rows = exercise_health([*hard, *sparse], {3: "dative", 4: "articles"})
        self.assertEqual("too_hard", rows[0]["status"])
        self.assertEqual("healthy", rows[1]["status"])

    def test_retention_uses_eligible_invite_cohorts(self):
        now = datetime.now()
        enrollments = [
            SimpleNamespace(user_id=1, joined_at=now - timedelta(days=8)),
            SimpleNamespace(user_id=2, joined_at=now - timedelta(days=2)),
        ]
        sessions = [
            SimpleNamespace(user_id=1, started_at=now - timedelta(hours=12)),
            SimpleNamespace(user_id=2, started_at=now - timedelta(hours=12)),
        ]
        result = retention_cohorts(enrollments, sessions, now)
        self.assertEqual({"eligible": 2, "retained": 2, "rate": 100}, result["d1"])
        self.assertEqual({"eligible": 1, "retained": 1, "rate": 100}, result["d7"])

    def test_content_health_does_not_invent_rates_for_sparse_samples(self):
        lesson = SimpleNamespace(id=3, topic="introductions", content={"day": 1, "module": 1, "title": "Introduce yourself"})
        attempts = [SimpleNamespace(lesson_id=3, user_id=7, correct=False)]
        sessions = [SimpleNamespace(lesson_id=3, user_id=7, status="practice_needed")]
        rows = lesson_content_health([lesson], attempts, sessions, [], lambda _: [])

        self.assertEqual("collecting", rows[0]["status"])
        self.assertIsNone(rows[0]["signals"]["completion_rate"])
        self.assertIsNone(rows[0]["signals"]["review_success"])
        self.assertEqual(1, rows[0]["sample"]["learners"])

    def test_content_health_flags_failed_changed_context_recall(self):
        lesson = SimpleNamespace(id=3, topic="introductions", content={"day": 1, "module": 1, "title": "Introduce yourself"})
        attempts = [SimpleNamespace(lesson_id=3, user_id=index, correct=True) for index in range(5)]
        sessions = [SimpleNamespace(lesson_id=3, user_id=index, status="passed") for index in range(5)]
        events = []
        for index in range(5):
            events.extend([
                SimpleNamespace(user_id=index, event_name="lesson_started", properties={"lesson_id": 3}),
                SimpleNamespace(user_id=index, event_name="lesson_completed", properties={"lesson_id": 3}),
                SimpleNamespace(user_id=index, event_name="review_answered", properties={"lesson_id": 3, "correct": index == 0}),
            ])
        rows = lesson_content_health([lesson], attempts, sessions, events, lambda _: [])

        self.assertEqual("needs_review", rows[0]["status"])
        self.assertEqual(20, rows[0]["signals"]["review_success"])
        self.assertIn("Changed-context recall is below 60%", rows[0]["reasons"])

    def test_beta_readiness_requires_real_completion_and_recall_samples(self):
        health = [{"publish_ready": True, "status": "collecting"} for _ in range(20)]
        summary = {"counts": {"lesson_completed": 10, "review_answered": 4}}
        result = beta_readiness(health, summary, enrolled=8, active_learners=6)

        self.assertEqual("collecting_evidence", result["stage"])
        self.assertFalse(result["gates"][-1]["passed"])
        summary["counts"]["review_answered"] = 5
        health[0]["status"] = "healthy"
        result = beta_readiness(health, summary, enrolled=8, active_learners=6)
        self.assertEqual("evidence_ready", result["stage"])
        self.assertTrue(result["all_gates_passed"])

    def test_real_device_acceptance_is_explicit_and_blocks_release_gate(self):
        now = datetime.now()
        partial = acceptance_report([
            SimpleNamespace(check_id="iphone_journey", passed=True, notes="iPhone 15", updated_at=now),
        ])
        self.assertEqual(1, partial["passed"])
        self.assertFalse(partial["complete"])
        self.assertEqual(7, partial["required"])

        health = [{"publish_ready": True, "status": "healthy"} for _ in range(20)]
        summary = {"counts": {"lesson_completed": 10, "review_answered": 5}}
        readiness = beta_readiness(health, summary, enrolled=8, active_learners=6, acceptance=partial)
        device_gate = next(item for item in readiness["gates"] if item["id"] == "devices")
        self.assertFalse(device_gate["passed"])
        self.assertFalse(readiness["all_gates_passed"])


if __name__ == "__main__":
    unittest.main()
