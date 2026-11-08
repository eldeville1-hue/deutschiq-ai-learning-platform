import unittest
from datetime import datetime, timedelta, timezone
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

    def test_funnel_excludes_events_that_precede_prior_stage(self):
        t = datetime(2026, 11, 8, tzinfo=timezone.utc)
        events = [
            event("diagnostic_completed", user=1),
            event("diagnostic_completed", user=2),
            event("today_viewed", user=1),
            event("today_viewed", user=2),
        ]
        events[0].created_at = t
        events[1].created_at = t
        events[2].created_at = t - timedelta(minutes=1)
        events[3].created_at = t + timedelta(minutes=1)
        funnel = learning_analytics(events, [], [])["funnel"]
        self.assertEqual(funnel[1]["users"], 2)
        self.assertEqual(funnel[1]["from_previous"], 50)

    def test_funnel_accepts_later_repeat_after_early_visit(self):
        t = datetime(2026, 11, 8, tzinfo=timezone.utc)
        events = [
            event("diagnostic_completed"),
            event("today_viewed"),
            event("today_viewed"),
        ]
        for item, stamp in zip(events, [t, t - timedelta(minutes=1), t + timedelta(minutes=1)]):
            item.created_at = stamp
        self.assertEqual(learning_analytics(events, [], [])["funnel"][1]["from_previous"], 100)

    def test_same_timestamp_does_not_prove_funnel_progress(self):
        t = datetime(2026, 11, 8, tzinfo=timezone.utc)
        events = [event("diagnostic_completed"), event("today_viewed")]
        for item in events:
            item.created_at = t
        self.assertEqual(learning_analytics(events, [], [])["funnel"][1]["from_previous"], 0)

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

    def test_delayed_topic_followup_requires_24_hours_and_one_followup_per_topic(self):
        t = datetime(2026, 11, 8, tzinfo=timezone.utc)
        def attempt(user, topic, hours, correct):
            return SimpleNamespace(user_id=user, topic=topic, created_at=t + timedelta(hours=hours), correct=correct)
        attempts = [
            attempt(1, "obwohl", 0, True),
            attempt(1, "obwohl", 2, True),
            attempt(1, "obwohl", 25, False),
            attempt(1, "obwohl", 50, True),
            attempt(2, "obwohl", 0, False),
            attempt(2, "obwohl", 24, True),
            attempt(3, "weil", 0, True),
            attempt(3, "weil", 23, True),
        ]
        result = learning_analytics([], attempts, [])["effectiveness"]["delayed_topic_followup"]
        self.assertEqual(result, {"cohorts": 2, "accuracy": 50, "minimum_gap_hours": 24})

    def test_delayed_topic_followup_without_followups_is_undefined(self):
        attempts = [SimpleNamespace(user_id=1, topic="weil", created_at=datetime(2026, 11, 8, tzinfo=timezone.utc), correct=True)]
        self.assertEqual(learning_analytics([], attempts, [])["effectiveness"]["delayed_topic_followup"]["accuracy"], None)

    def test_delayed_topic_windows_use_first_qualifying_attempt(self):
        t = datetime(2026, 11, 8, tzinfo=timezone.utc)
        def attempt(user, days, correct):
            return SimpleNamespace(user_id=user, topic="weil", created_at=t + timedelta(days=days), correct=correct)
        attempts = [
            attempt(1, 0, True), attempt(1, 1, False),
            attempt(1, 3, True), attempt(1, 7, False), attempt(1, 8, True),
            attempt(2, 0, False), attempt(2, 1, True),
            attempt(2, 4, False),
        ]
        windows = learning_analytics([], attempts, [], as_of=t + timedelta(days=9))["effectiveness"]["delayed_topic_windows"]
        self.assertEqual(windows["1"], {"eligible_cohorts": 2, "awaiting_maturity": 0, "cohorts": 2, "accuracy": 50})
        self.assertEqual(windows["3"], {"eligible_cohorts": 2, "awaiting_maturity": 0, "cohorts": 2, "accuracy": 50})
        self.assertEqual(windows["7"], {"eligible_cohorts": 2, "awaiting_maturity": 0, "cohorts": 1, "accuracy": 0})

    def test_delayed_topic_windows_without_eligible_followups(self):
        t = datetime(2026, 11, 8, tzinfo=timezone.utc)
        attempts = [SimpleNamespace(user_id=1, topic="weil", created_at=t, correct=True)]
        windows = learning_analytics([], attempts, [], as_of=t + timedelta(hours=12))["effectiveness"]["delayed_topic_windows"]
        self.assertTrue(all(value == {"eligible_cohorts": 0, "awaiting_maturity": 1, "cohorts": 0, "accuracy": None} for value in windows.values()))

    def test_delayed_topic_windows_distinguish_missing_followup_from_immature_cohort(self):
        t = datetime(2026, 11, 1, tzinfo=timezone.utc)
        attempts = [
            SimpleNamespace(user_id=1, topic="weil", created_at=t, correct=True),
            SimpleNamespace(user_id=2, topic="weil", created_at=t + timedelta(days=6), correct=False),
        ]
        windows = learning_analytics([], attempts, [], as_of=t + timedelta(days=8))["effectiveness"]["delayed_topic_windows"]
        self.assertEqual(windows["3"], {"eligible_cohorts": 1, "awaiting_maturity": 1, "cohorts": 0, "accuracy": None})
        self.assertEqual(windows["7"], {"eligible_cohorts": 1, "awaiting_maturity": 1, "cohorts": 0, "accuracy": None})

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
