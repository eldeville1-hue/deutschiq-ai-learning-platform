import unittest
from datetime import datetime, timedelta
from types import SimpleNamespace

from app.services.tutor_verified_review import prioritize_verified_topics


def event(topic, correct, index, source="reviewed_word_order"):
    return SimpleNamespace(
        id=index,
        event_name="tutor_verified_attempt",
        created_at=datetime(2026, 10, 1) + timedelta(minutes=index),
        properties={"topic": topic, "correct": correct, "source": source},
    )


class TutorVerifiedReviewTests(unittest.TestCase):
    def test_unresolved_errors_ranked_by_count(self):
        events = [
            event("dative_case", False, 1),
            event("word_order", False, 2),
            event("dative_case", False, 3),
        ]
        self.assertEqual(prioritize_verified_topics(events), ["dative_case", "word_order"])

    def test_later_correct_answer_clears_topic(self):
        events = [
            event("dative_case", False, 1),
            event("dative_case", True, 2),
            event("word_order", False, 3),
        ]
        self.assertEqual(prioritize_verified_topics(events), ["word_order"])

    def test_order_does_not_depend_on_query_sort(self):
        events = [event("dative_case", True, 4), event("dative_case", False, 2)]
        self.assertEqual(prioritize_verified_topics(events), [])

    def test_ignores_unverified_and_malformed_events(self):
        events = [
            event("word_order", False, 1, "ai"),
            event("unknown", False, 2),
            event("articles", "false", 3),
            SimpleNamespace(event_name="tutor_answered", properties={}),
        ]
        self.assertEqual(prioritize_verified_topics(events), [])


if __name__ == "__main__":
    unittest.main()
