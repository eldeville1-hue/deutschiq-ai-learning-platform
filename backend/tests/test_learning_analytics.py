import unittest
from types import SimpleNamespace
from app.services.learning_analytics import learning_analytics, production_alerts


def event(name, user=1, **properties):
    return SimpleNamespace(event_name=name, user_id=user, properties=properties)


class LearningAnalyticsTests(unittest.TestCase):
    def test_learning_evidence_modes_are_not_mixed(self):
        events = [
            event("diagnostic_completed"), event("today_viewed"), event("lesson_started"),
            event("exercise_answered", correct=False, retry=False),
            event("exercise_answered", correct=True, retry=True), event("lesson_completed"),
            event("review_started"), event("review_answered", correct=True), event("review_completed"),
        ]
        result = learning_analytics(events, [], [])
        self.assertEqual([row["users"] for row in result["funnel"]], [1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(result["effectiveness"]["first_try"]["accuracy"], 0)
        self.assertEqual(result["effectiveness"]["supported_retry"]["accuracy"], 100)
        self.assertEqual(result["effectiveness"]["delayed_retrieval"]["accuracy"], 100)

    def test_small_tutor_sample_does_not_create_noise(self):
        summary = {"reliability": {}, "reliability_detail": {"serious_errors": 0}}
        learning = {"tutor": {"answers": 2, "fallback": 2, "fallback_rate": 100}}
        self.assertEqual(production_alerts(summary, learning), [])

    def test_tutor_fallback_alert_requires_meaningful_sample(self):
        summary = {"reliability": {}, "reliability_detail": {"serious_errors": 0}}
        learning = {"tutor": {"answers": 5, "fallback": 2, "fallback_rate": 40}}
        alerts = production_alerts(summary, learning)
        self.assertEqual(alerts[0]["signal"], "tutor_fallback")


if __name__ == "__main__":
    unittest.main()
