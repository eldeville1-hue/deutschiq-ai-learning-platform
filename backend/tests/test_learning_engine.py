import unittest
from app.services.learning_engine import mastery_update, review_interval, session_score


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


if __name__ == "__main__":
    unittest.main()
