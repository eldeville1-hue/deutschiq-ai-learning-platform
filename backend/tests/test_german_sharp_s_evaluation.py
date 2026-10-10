import unittest

from app.services.answer_intelligence import evaluate_structured_answer, normalize_text


class GermanSharpSEvaluationTests(unittest.TestCase):
    def test_sharp_s_and_double_s_remain_distinct(self):
        self.assertNotEqual(normalize_text("Maße"), normalize_text("Masse"))
        self.assertEqual(normalize_text("MAẞE"), normalize_text("Maße"))

    def test_different_german_words_are_not_accepted_as_equivalent(self):
        exercise = {"type": "fill", "answer": "Maße", "accepted_answers": ["Maße"]}
        result = evaluate_structured_answer("Masse", exercise)
        self.assertFalse(result["correct"])
        self.assertEqual("verified", result["evaluation_status"])

    def test_punctuation_and_capitalization_still_normalize(self):
        exercise = {"type": "fill", "answer": "Die Straße.", "accepted_answers": ["Die Straße."]}
        result = evaluate_structured_answer("die straße!", exercise)
        self.assertTrue(result["correct"])


if __name__ == "__main__":
    unittest.main()
