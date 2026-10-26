import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class ReorderAlternativeReviewTests(unittest.TestCase):
    def test_alternative_word_order_needs_review(self):
        exercise = {"type": "reorder", "answer": "Ich lerne heute Deutsch."}
        result = evaluate_structured_answer("Heute lerne ich Deutsch.", exercise)
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])
        self.assertEqual(result["confirmed_errors"], [])

    def test_exact_reorder_is_verified(self):
        exercise = {"type": "reorder", "answer": "Ich lerne heute Deutsch."}
        result = evaluate_structured_answer("Ich lerne heute Deutsch.", exercise)
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertTrue(result["correct"])

    def test_different_tokens_still_rejected(self):
        exercise = {"type": "reorder", "answer": "Ich lerne heute Deutsch."}
        result = evaluate_structured_answer("Ich lerne morgen Deutsch.", exercise)
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertFalse(result["correct"])


if __name__ == "__main__":
    unittest.main()
