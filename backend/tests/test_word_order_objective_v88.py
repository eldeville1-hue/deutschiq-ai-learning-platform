import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class WordOrderObjectiveV88Tests(unittest.TestCase):
    def test_permutation_without_word_order_objective_is_not_diagnosed(self):
        result = evaluate_structured_answer("Heute lerne ich Deutsch.", {
            "type": "error_repair", "answer": "Ich lerne heute Deutsch.",
        })
        self.assertFalse(result["correct"])
        self.assertNotIn("word_order", [error["type"] for error in result["errors"]])

    def test_explicit_word_order_objective_preserves_diagnosis(self):
        result = evaluate_structured_answer("Heute lerne ich Deutsch.", {
            "type": "reorder", "answer": "Ich lerne heute Deutsch.",
            "target_feature": "word_order",
        })
        self.assertFalse(result["correct"])
        self.assertIn("word_order", [error["type"] for error in result["errors"]])

    def test_unlisted_open_permutation_remains_uncertain_without_xp(self):
        result = evaluate_structured_answer("Heute lerne ich Deutsch.", {
            "type": "translation", "answer": "Ich lerne heute Deutsch.",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertEqual(result["score"], 0)
        self.assertNotIn("word_order", [error["type"] for error in result["errors"]])


if __name__ == "__main__":
    unittest.main()
