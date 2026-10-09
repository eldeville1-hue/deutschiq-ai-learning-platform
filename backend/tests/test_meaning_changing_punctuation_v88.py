import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class MeaningChangingPunctuationV88Tests(unittest.TestCase):
    def test_missing_vocative_comma_is_not_verified_in_open_task(self):
        result = evaluate_structured_answer("Komm wir essen Opa!", {
            "type": "translation", "answer": "Komm, wir essen, Opa!",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])
        self.assertEqual(result["score"], 0)

    def test_authored_comma_is_accepted(self):
        result = evaluate_structured_answer("Komm, wir essen, Opa!", {
            "type": "translation", "answer": "Komm, wir essen, Opa!",
        })
        self.assertTrue(result["correct"])

    def test_regular_punctuation_variation_stays_accepted(self):
        result = evaluate_structured_answer("Ich lerne Deutsch!", {
            "type": "translation", "answer": "Ich lerne Deutsch.",
        })
        self.assertTrue(result["correct"])


if __name__ == "__main__":
    unittest.main()
