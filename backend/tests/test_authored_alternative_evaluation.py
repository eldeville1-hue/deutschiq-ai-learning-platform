import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class AuthoredAlternativeEvaluationTests(unittest.TestCase):
    def test_alternative_is_full_credit_without_spurious_diffs(self):
        exercise = {
            "type": "translate",
            "answer": "Ich lerne jeden Tag Deutsch.",
            "accepted_answers": ["Ich lerne jeden Tag Deutsch.", "Deutsch lerne ich jeden Tag."],
        }
        result = evaluate_structured_answer("Deutsch lerne ich jeden Tag.", exercise)
        self.assertTrue(result["correct"])
        self.assertEqual("verified", result["evaluation_status"])
        self.assertEqual(100, result["score"])
        self.assertEqual("Deutsch lerne ich jeden Tag.", result["model"])
        self.assertEqual([], result["missing_words"])
        self.assertEqual([], result["extra_words"])
        self.assertIsNone(result["error_type"])

    def test_unlisted_open_response_remains_uncertain(self):
        exercise = {"type": "translate", "answer": "Ich sehe den Mann.",
                    "accepted_answers": ["Ich sehe den Mann."]}
        result = evaluate_structured_answer("Ich sehe einen Mann.", exercise)
        self.assertFalse(result["correct"])
        self.assertEqual("uncertain", result["evaluation_status"])

    def test_changed_case_is_not_accepted(self):
        exercise = {"type": "fill", "answer": "den", "accepted_answers": ["den"]}
        result = evaluate_structured_answer("dem", exercise)
        self.assertFalse(result["correct"])


if __name__ == "__main__":
    unittest.main()
