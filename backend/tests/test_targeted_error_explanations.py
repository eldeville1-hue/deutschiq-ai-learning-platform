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

    def test_uncertain_free_text_never_exposes_confirmed_errors(self):
        examples = [
            ("Heute lernen wir Deutsch.", "Wir lernen heute Deutsch.", "word_order"),
            ("Ich warte auf dem Bus.", "Ich warte auf den Bus.", "case"),
            ("Obwohl es regnet, gehen wir spazieren.", "Wir gehen spazieren, obwohl es regnet.", "word_order"),
        ]
        for submitted, reference, feature in examples:
            with self.subTest(submitted=submitted):
                result = evaluate_structured_answer(submitted, {
                    "type": "translation", "answer": reference, "target_feature": feature,
                })
                self.assertEqual("uncertain", result["evaluation_status"])
                self.assertFalse(result["correct"])
                self.assertEqual([], result["confirmed_errors"])
                self.assertIsNotNone(result["learner_feedback"])
                self.assertIn("review", result["learner_feedback"].lower())

    def test_verified_choice_explanations_are_targeted_not_generic(self):
        examples = [
            ("Ich habe ein Hund.", "Ich habe einen Hund.", "article"),
            ("Ich warte auf dem Bus.", "Ich warte auf den Bus.", "case"),
            ("Ich interessiere mich an Musik.", "Ich interessiere mich für Musik.", "preposition"),
            ("Ich habe gestern nach Hause gegangen.", "Ich bin gestern nach Hause gegangen.", "auxiliary"),
        ]
        for submitted, reference, feature in examples:
            with self.subTest(feature=feature):
                result = evaluate_structured_answer(submitted, {
                    "type": "choice", "answer": reference, "target_feature": feature,
                })
                self.assertEqual("verified", result["evaluation_status"])
                self.assertFalse(result["correct"])
                self.assertEqual(feature, result["confirmed_errors"][0]["type"])
                self.assertTrue(result["confirmed_errors"][0]["explanation"].strip())
                self.assertIsNone(result["learner_feedback"])

    def test_a1_article(self):
        self.check_category("Ich habe ein Hund.", "Ich habe einen Hund.", "article")

    def test_a2_case(self):
        self.check_category("Ich warte auf dem Bus.", "Ich warte auf den Bus.", "case")

    def test_a2_preposition(self):
        self.check_category("Ich interessiere mich an Musik.", "Ich interessiere mich für Musik.", "preposition")

    def test_preposition_target_with_wrong_article_reports_case(self):
        result = evaluate_structured_answer("Ich warte auf dem Bus.", {
            "type": "choice", "answer": "Ich warte auf den Bus.",
            "target_feature": "preposition",
        })
        self.assertEqual(result["errors"][0]["type"], "case")
        self.assertIn("preposition is unchanged", result["errors"][0]["explanation"].lower())

    def test_a2_auxiliary(self):
        self.check_category("Ich habe gestern nach Hause gegangen.", "Ich bin gestern nach Hause gegangen.", "auxiliary")

    def test_same_auxiliary_family_is_conjugation(self):
        result = evaluate_structured_answer("Du hat Zeit.", {
            "type": "choice", "answer": "Du hast Zeit.",
        })
        self.assertEqual(result["errors"][0]["type"], "conjugation")
        self.assertIn("subject", result["errors"][0]["explanation"].lower())

    def test_different_auxiliary_family_is_auxiliary_selection(self):
        result = evaluate_structured_answer("Ich habe gestern gegangen.", {
            "type": "choice", "answer": "Ich bin gestern gegangen.",
        })
        self.assertEqual(result["errors"][0]["type"], "auxiliary")
        self.assertIn("haben or sein", result["errors"][0]["explanation"])

    def test_present_tense_verb_choice_does_not_claim_perfekt(self):
        result = evaluate_structured_answer("Ich bin Hunger.", {
            "type": "choice", "answer": "Ich habe Hunger.",
        })
        self.assertEqual(result["errors"][0]["type"], "auxiliary")
        self.assertNotIn("Perfekt", result["errors"][0]["explanation"])
        self.assertIn("meaning and construction", result["errors"][0]["explanation"])

    def test_perfekt_participle_keeps_specific_auxiliary_explanation(self):
        result = evaluate_structured_answer("Ich habe gestern gegangen.", {
            "type": "choice", "answer": "Ich bin gestern gegangen.",
        })
        self.assertIn("Perfekt", result["errors"][0]["explanation"])

    def test_unrecognized_difference_does_not_invent_vocabulary_error(self):
        result = evaluate_structured_answer("Ich mag Tee.", {
            "type": "choice", "answer": "Ich mag Kaffee.",
        })
        self.assertFalse(result["correct"])
        self.assertEqual(result["errors"][0]["type"], "answer_mismatch")
        self.assertIn("context", result["errors"][0]["explanation"])

    def test_b1_relative_pronoun(self):
        self.check_category("Das Fahrrad, den ich gekauft habe, ist neu.",
                            "Das Fahrrad, das ich gekauft habe, ist neu.", "relative_pronoun")

    def test_relative_pronoun_explanation_is_specific(self):
        result = evaluate_structured_answer("Das Fahrrad, den ich gekauft habe, ist neu.", {
            "type": "choice", "answer": "Das Fahrrad, das ich gekauft habe, ist neu.",
            "target_feature": "relative_pronoun",
        })
        self.assertIn("relative pronoun", result["errors"][0]["explanation"].lower())
        self.assertNotIn("the noun’s gender", result["errors"][0]["explanation"].lower())

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

    def test_open_translation_permutation_has_no_word_order_diagnosis(self):
        result = evaluate_structured_answer("Heute lernen wir Deutsch.", {
            "type": "translation", "answer": "Wir lernen heute Deutsch.",
            "target_feature": "word_order",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])
        self.assertNotIn("word_order", result["candidate_error_types"])

    def test_targeted_choice_permutation_reports_word_order(self):
        result = evaluate_structured_answer("Ich glaube, dass er kommt heute.", {
            "type": "choice", "answer": "Ich glaube, dass er heute kommt.",
            "target_feature": "word_order",
        })
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
