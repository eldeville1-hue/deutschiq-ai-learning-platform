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

    def test_funnel_conversion_counts_same_learners_not_unrelated_population(self):
        events = [
            event("diagnostic_completed", user=1),
            event("diagnostic_completed", user=2),
            event("today_viewed", user=2),
            event("today_viewed", user=3),
            event("today_viewed", user=4),
            event("lesson_started", user=3),
            event("lesson_started", user=5),
        ]
        funnel = learning_analytics(events, [], [])["funnel"]
        self.assertEqual(funnel[1]["users"], 3)
        self.assertEqual(funnel[1]["from_previous"], 50)
        self.assertEqual(funnel[2]["users"], 2)
        self.assertEqual(funnel[2]["from_previous"], 33)
        self.assertEqual(funnel[3]["from_previous"], 0)
        self.assertIsNone(funnel[4]["from_previous"])

    def test_string_false_is_not_counted_as_correct_or_retry(self):
        events = [
            event("exercise_answered", correct="false", retry="false"),
            event("exercise_answered", correct="true", retry="true"),
            event("review_answered", correct="false"),
            event("mission_repair_completed", repaired="false"),
            event("mission_repair_completed", repaired="true"),
        ]
        effectiveness = learning_analytics(events, [], [])["effectiveness"]
        self.assertEqual(effectiveness["first_try"], {"answers": 1, "accuracy": 0})
        self.assertEqual(effectiveness["supported_retry"], {"answers": 1, "accuracy": 100})
        self.assertEqual(effectiveness["delayed_retrieval"], {"answers": 1, "accuracy": 0})
        self.assertEqual(effectiveness["mission_repair"], {"attempts": 2, "success_rate": 50})

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
