import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class TargetedArticleFeedbackTests(unittest.TestCase):
    def test_case_feedback_names_expected_and_submitted_forms(self):
        result = evaluate_structured_answer("Ich helfe den Mann.", {
            "type": "fill", "answer": "Ich helfe dem Mann.", "target_feature": "case",
        })
        self.assertFalse(result["correct"])
        self.assertEqual("case", result["errors"][0]["type"])
        self.assertIn("'dem' instead of 'den'", result["errors"][0]["explanation"])

    def test_article_feedback_explains_grammar_dimensions(self):
        result = evaluate_structured_answer("Ich sehe der Hund.", {
            "type": "fill", "answer": "Ich sehe den Hund.", "target_feature": "article",
        })
        self.assertFalse(result["correct"])
        self.assertEqual("article", result["errors"][0]["type"])
        self.assertIn("gender, number and grammatical case", result["errors"][0]["explanation"])

    def test_correct_form_still_receives_credit(self):
        result = evaluate_structured_answer("ich helfe dem mann!", {
            "type": "fill", "answer": "Ich helfe dem Mann.", "target_feature": "case",
        })
        self.assertTrue(result["correct"])


if __name__ == "__main__":
    unittest.main()
