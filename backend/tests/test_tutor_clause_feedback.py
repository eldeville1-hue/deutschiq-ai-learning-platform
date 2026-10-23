import unittest
from app.services.tutor_verified_practice import verified_retry_feedback, grade_reviewed_word_order
from app.services.tutor_clause_bank import CLAUSE_DRILLS


class ClauseFeedbackTests(unittest.TestCase):
    def test_each_clause_topic_has_distinct_localized_hint(self):
        for topic, term in (
            ("weil_clause", "weil"),
            ("obwohl_clause", "obwohl"),
            ("damit_clause", "damit"),
            ("konjunktiv_ii", "würde"),
        ):
            for language in ("ru", "de", "en"):
                with self.subTest(topic=topic, language=language):
                    feedback = verified_retry_feedback(topic, language)
                    self.assertIn(term, feedback)
                    self.assertIn(" ", feedback)

    def test_all_reviewed_clause_drills_have_feedback(self):
        for _id, _level, topic, expected, words, _variants in CLAUSE_DRILLS:
            result = grade_reviewed_word_order("Exercise: " + words, expected)
            self.assertTrue(result["correct"])
            self.assertEqual(result["topic"], topic)
            self.assertTrue(verified_retry_feedback(topic, "ru"))


if __name__ == "__main__":
    unittest.main()
