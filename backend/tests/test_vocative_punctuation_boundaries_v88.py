import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class VocativePunctuationBoundaryV88Tests(unittest.TestCase):
    def test_extra_vocative_comma_is_not_auto_accepted(self):
        result = evaluate_structured_answer("Komm, wir essen, Opa!", {
            "type": "translation", "answer": "Komm, wir essen Opa!",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])
        self.assertEqual(result["score"], 0)

    def test_closed_task_punctuation_conflict_is_not_verified(self):
        result = evaluate_structured_answer("Komm wir essen Opa!", {
            "type": "choice", "answer": "Komm, wir essen, Opa!",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])
        self.assertEqual(result["score"], 0)

    def test_explicitly_authored_variant_can_still_be_accepted(self):
        result = evaluate_structured_answer("Komm wir essen Opa!", {
            "type": "translation", "answer": "Komm, wir essen, Opa!",
            "accepted_answers": ["Komm wir essen Opa!"],
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertTrue(result["correct"])


if __name__ == "__main__":
    unittest.main()
