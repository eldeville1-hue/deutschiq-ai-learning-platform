import unittest
from app.services.answer_intelligence import evaluate_structured_answer


class StructuredEvaluationV88Tests(unittest.TestCase):
    def test_explicit_alternatives_are_verified(self):
        result = evaluate_structured_answer("Ich hole einen Kaffee.", {
            "type": "translation", "answer": "Ich kaufe einen Kaffee.",
            "accepted_answers": ["Ich kaufe einen Kaffee.", "Ich hole einen Kaffee."],
        })
        self.assertTrue(result["correct"])
        self.assertTrue(result["task_satisfied"])
        self.assertEqual(result["evaluation_status"], "verified")

    def test_unlisted_open_response_is_not_silently_rejected_as_grammar_error(self):
        result = evaluate_structured_answer("Ich besorge einen Kaffee.", {
            "type": "translation", "answer": "Ich kaufe einen Kaffee.",
        })
        self.assertFalse(result["correct"])
        self.assertIsNone(result["grammar_correct"])
        self.assertEqual(result["evaluation_status"], "uncertain")

    def test_multiple_errors_are_recorded_without_false_positive(self):
        result = evaluate_structured_answer("Ich kaufen ein Kaffee", {
            "type": "translation", "answer": "Ich kaufe einen Kaffee",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])
        self.assertEqual([error["type"] for error in result["errors"]], ["conjugation", "article"])

    def test_negation_does_not_satisfy_translation(self):
        result = evaluate_structured_answer("Ich kaufe keinen Kaffee", {
            "type": "translation", "answer": "Ich kaufe einen Kaffee",
        })
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertEqual(result["errors"][0]["type"], "negation")

    def test_missing_model_requires_review(self):
        result = evaluate_structured_answer("Hallo", {"type": "translation"})
        self.assertEqual(result["evaluation_status"], "needs_review")
        self.assertFalse(result["correct"])

    def test_wrong_choice_remains_verified_failure(self):
        result = evaluate_structured_answer("nein", {
            "type": "choice", "answer": "ja",
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertFalse(result["correct"])
        self.assertEqual(result["errors"][0]["span"], "nein")

    def test_article_mistake_is_not_a_spelling_success(self):
        result = evaluate_structured_answer("Ich kaufe ein Kaffee", {
            "type": "translation", "answer": "Ich kaufe einen Kaffee",
        })
        self.assertFalse(result["correct"])


if __name__ == "__main__":
    unittest.main()
