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

    def test_authored_alternative_with_different_word_order_is_accepted(self):
        result = self.evaluate(
            "Heute lernen wir Deutsch.", "Wir lernen heute Deutsch.",
            accepted_answers=["Heute lernen wir Deutsch."],
            target_feature="word_order",
        )
        self.assertTrue(result["correct"])
        self.assertEqual(result["evaluation_status"], "verified")

    def test_unlisted_word_order_variant_stays_uncertain(self):
        result = self.evaluate(
            "Heute lernen wir Deutsch.", "Wir lernen heute Deutsch.",
            target_feature="word_order",
        )
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertNotIn("word_order", result["candidate_error_types"])

    def test_authored_alternative_does_not_allow_negated_variant(self):
        result = self.evaluate(
            "Ich lerne heute nicht Deutsch.", "Ich lerne heute Deutsch.",
            accepted_answers=["Heute lerne ich Deutsch."],
        )
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "uncertain")

    def test_multiple_authored_answers_do_not_invent_grammar_diagnosis(self):
        result = self.evaluate(
            "Ich fahre morgen nach Berlin.", "Morgen gehe ich nach Berlin.",
            kind="choice", accepted_answers=["Ich gehe morgen nach Berlin."],
        )
        self.assertFalse(result["correct"])
        self.assertEqual(result["errors"][0]["type"], "answer_mismatch")
        self.assertNotEqual(result["errors"][0]["type"], "word_order")

    def test_invalid_authored_alternatives_never_grant_credit(self):
        result = self.evaluate(
            "Ich lerne nicht.", "Ich lerne.",
            accepted_answers=["", None, 123, {"text": "Ich lerne nicht."}],
        )
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "uncertain")

    def test_missing_reference_requires_review(self):
        result = evaluate_structured_answer("Ich lerne Deutsch.", {
            "type": "translation", "answer": "", "accepted_answers": [],
        })
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "needs_review")

    def test_empty_answer_is_incorrect(self):
        result = self.evaluate("", "Ich lerne Deutsch.")
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "verified")

    def test_unlisted_choice_is_not_accepted(self):
        result = self.evaluate("Ich trinke Milch.", "Ich trinke Wasser.", kind="choice")
        self.assertFalse(result["correct"])


if __name__ == "__main__":
    unittest.main()
