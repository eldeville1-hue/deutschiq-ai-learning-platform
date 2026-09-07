import unittest
from app.services.learning_engine import mastery_update, next_stability, retention_score, review_interval, session_score
from app.services.skill_graph import blocked_by, prerequisites_met


class LearningEngineTests(unittest.TestCase):
    def test_score_uses_only_given_session(self):
        self.assertEqual(session_score([True, False, True]), 67)
        self.assertEqual(session_score([]), 0)

    def test_mastery_is_bounded_and_confidence_weighted(self):
        self.assertEqual(mastery_update(95, True, "sure"), 100)
        self.assertLess(mastery_update(50, True, "guess"), mastery_update(50, True, "sure"))
        self.assertEqual(mastery_update(3, False, "okay"), 0)

    def test_review_intervals_expand(self):
        self.assertEqual(review_interval(False, 8), 1)
        self.assertEqual(review_interval(True, 1), 1)
        self.assertEqual(review_interval(True, 5), 30)

    def test_confident_error_is_penalized_more_than_guess(self):
        self.assertLess(mastery_update(50, False, "sure"), mastery_update(50, False, "guess"))

    def test_slow_correct_recall_grows_less(self):
        self.assertLess(mastery_update(40, True, "okay", 60_000), mastery_update(40, True, "okay", 5_000))

    def test_retention_decays_when_review_is_overdue(self):
        self.assertEqual(retention_score(70, 7, 0), 70)
        self.assertLess(retention_score(70, 7, 5), 70)

    def test_stability_recovers_and_collapses(self):
        self.assertGreater(next_stability(3, True, "sure"), 3)
        self.assertLess(next_stability(10, False, "sure"), 10)

    def test_skill_graph_blocks_advanced_topic(self):
        self.assertFalse(prerequisites_met("dative_case", {"word_order": 20}))
        self.assertEqual(blocked_by("dative_case", {"word_order": 20}), ["word_order"])


if __name__ == "__main__":
    unittest.main()
