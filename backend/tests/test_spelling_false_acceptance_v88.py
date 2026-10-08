import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class SpellingFalseAcceptanceV88Tests(unittest.TestCase):
    def test_different_valid_word_not_awarded_in_closed_task(self):
        result = evaluate_structured_answer(
            "Ich will schreien", {"type": "error_repair", "answer": "Ich will schreiben"})
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "verified")

    def test_internal_letter_omission_does_not_earn_verified_success(self):
        result = evaluate_structured_answer(
            "Wir schrieben heute", {"type": "fill_blank", "answer": "Wir schreiben heute"})
        self.assertFalse(result["correct"])
        self.assertEqual(result["score"], 100 if result["correct"] else result["score"])
        self.assertEqual(result["evaluation_status"], "verified")

    def test_open_ended_unlisted_spelling_is_uncertain(self):
        result = evaluate_structured_answer(
            "Wir schrieben heute", {"type": "translation", "answer": "Wir schreiben heute"})
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertEqual(result["score"], 0)

    def test_explicit_accepted_alternative_still_passes(self):
        result = evaluate_structured_answer(
            "Guten Abend", {"type": "translation", "answer": "Hallo",
                             "accepted_answers": ["Hallo", "Guten Abend"]})
        self.assertTrue(result["correct"])
        self.assertEqual(result["evaluation_status"], "verified")


if __name__ == "__main__":
    unittest.main()
