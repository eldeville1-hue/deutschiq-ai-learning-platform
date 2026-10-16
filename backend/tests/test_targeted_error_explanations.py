"""Targeted explanation checks for German learner mistakes.

These fixtures test narrow, explicitly authored grammatical contrasts;
they do not validate arbitrary free-form language understanding.
"""
import unittest
from app.services.answer_intelligence import evaluate_structured_answer


class TargetedExplanationTests(unittest.TestCase):
    def check_category(self, answer, reference, category, *, kind="choice"):
        result = evaluate_structured_answer(answer, {
            "type": kind, "answer": reference, "target_feature": category,
        })
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertTrue(result["errors"])
        self.assertEqual(result["errors"][0]["type"], category)
        self.assertTrue(result["errors"][0]["explanation"])

    def test_a1_article(self):
        self.check_category("Ich habe ein Hund.", "Ich habe einen Hund.", "article")

    def test_a2_case(self):
        self.check_category("Ich warte auf dem Bus.", "Ich warte auf den Bus.", "case")

    def test_a2_preposition(self):
        self.check_category("Ich interessiere mich an Musik.", "Ich interessiere mich für Musik.", "preposition")

    def test_a2_auxiliary(self):
        self.check_category("Ich habe gestern nach Hause gegangen.", "Ich bin gestern nach Hause gegangen.", "auxiliary")

    def test_b1_relative_pronoun(self):
        self.check_category("Das Fahrrad, den ich gekauft habe, ist neu.",
                            "Das Fahrrad, das ich gekauft habe, ist neu.", "relative_pronoun")

    def test_relative_pronoun_explanation_is_specific(self):
        result = evaluate_structured_answer("Das Fahrrad, den ich gekauft habe, ist neu.", {
            "type": "choice", "answer": "Das Fahrrad, das ich gekauft habe, ist neu.",
            "target_feature": "relative_pronoun",
        })
        self.assertIn("relative pronoun", result["errors"][0]["explanation"].lower())
        self.assertNotIn("noun’s gender", result["errors"][0]["explanation"])

    def test_b2_infinitive(self):
        self.check_category("Die Maßnahme trägt dazu bei, Energie sparen.",
                            "Die Maßnahme trägt dazu bei, Energie zu sparen.", "infinitive")

    def test_b1_word_order(self):
        result = evaluate_structured_answer("Ich glaube, dass er kommt heute.", {
            "type": "choice", "answer": "Ich glaube, dass er heute kommt.",
            "target_feature": "word_order",
        })
        self.assertFalse(result["correct"])
        self.assertEqual(result["errors"][0]["type"], "word_order")

    def test_free_writing_does_not_claim_verified_grammar_error(self):
        result = evaluate_structured_answer("Ich warte auf dem Bus.", {
            "type": "translation", "answer": "Ich warte auf den Bus.",
            "target_feature": "case",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])


if __name__ == "__main__":
    unittest.main()
