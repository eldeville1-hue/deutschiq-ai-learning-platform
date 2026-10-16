"""Safety regressions for German answer evaluation across CEFR levels.

These are authored counterexamples, not an independently validated benchmark.
"""
import unittest
from app.services.answer_intelligence import evaluate_structured_answer


class AnswerEvaluationSafetyTests(unittest.TestCase):
    def evaluate(self, answer, reference, kind="translation", **extra):
        return evaluate_structured_answer(answer, {"type": kind, "answer": reference, **extra})

    def test_a1_negation_not_accepted_as_paraphrase(self):
        result = self.evaluate("Ich habe keinen Hund.", "Ich habe einen Hund.")
        self.assertFalse(result["correct"])
        self.assertNotEqual(result["evaluation_status"], "verified")

    def test_a2_wrong_perfect_auxiliary_not_auto_accepted(self):
        result = self.evaluate("Ich habe nach Hamburg gefahren.", "Ich bin nach Hamburg gefahren.")
        self.assertFalse(result["correct"])

    def test_b1_correct_authored_paraphrase_is_accepted(self):
        result = self.evaluate("Hätte ich Zeit, würde ich mitkommen.",
                               "Wenn ich Zeit hätte, würde ich mitkommen.",
                               accepted_answers=["Hätte ich Zeit, würde ich mitkommen."])
        self.assertTrue(result["correct"])
        self.assertEqual(result["evaluation_status"], "verified")

    def test_b2_unlisted_paraphrase_requires_review(self):
        result = self.evaluate("Die Entscheidung wurde trotz erheblicher Zweifel getroffen.",
                               "Obwohl erhebliche Zweifel bestanden, wurde die Entscheidung getroffen.")
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "uncertain")

    def test_spelling_similarity_does_not_verify_different_verb(self):
        result = self.evaluate("Wir schreien heute.", "Wir schreiben heute.")
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "uncertain")

    def test_empty_answer_is_incorrect(self):
        result = self.evaluate("", "Ich lerne Deutsch.")
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "verified")

    def test_unlisted_choice_is_not_accepted(self):
        result = self.evaluate("Ich trinke Milch.", "Ich trinke Wasser.", kind="choice")
        self.assertFalse(result["correct"])


if __name__ == "__main__":
    unittest.main()
