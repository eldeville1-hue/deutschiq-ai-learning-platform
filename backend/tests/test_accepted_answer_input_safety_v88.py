import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class AcceptedAnswerInputSafetyTests(unittest.TestCase):
    def test_string_alternatives_cannot_become_character_answers(self):
        result = evaluate_structured_answer("a", {
            "type": "choice", "answer": "Hallo",
            "accepted_answers": "abc",
        })
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "verified")

    def test_malformed_alternatives_without_reference_need_review(self):
        result = evaluate_structured_answer("a", {
            "type": "translation", "accepted_answers": "abc",
        })
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "needs_review")

    def test_non_string_alternatives_do_not_grant_credit(self):
        result = evaluate_structured_answer("123", {
            "type": "choice", "answer": "Hallo",
            "accepted_answers": [123, None, {"answer": "123"}],
        })
        self.assertFalse(result["correct"])

    def test_valid_authored_alternative_still_passes(self):
        result = evaluate_structured_answer("Guten Abend", {
            "type": "translation", "answer": "Hallo",
            "accepted_answers": ["Guten Abend"],
        })
        self.assertTrue(result["correct"])
        self.assertEqual(result["evaluation_status"], "verified")


if __name__ == "__main__":
    unittest.main()
