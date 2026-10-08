import unittest
from app.services.answer_intelligence import evaluate_structured_answer


class StructuredEvaluationV88Tests(unittest.TestCase):
    def test_explicit_alternatives_are_verified(self):
        result = evaluate_structured_answer("Ich hole einen Kaffee.", {
            "type": "translation", "answer": "Ich kaufe einen Kaffee.",
            "accepted_answers": ["Ich kaufe einen Kaffee.", "Ich hole einen Kaffee."],
        })
        self.assertTrue(result["correct"])
        self.assertTrue(result["task_satisfied"])
        self.assertEqual(result["evaluation_status"], "verified")

    def test_unlisted_open_response_is_not_silently_rejected_as_grammar_error(self):
        result = evaluate_structured_answer("Ich besorge einen Kaffee.", {
            "type": "translation", "answer": "Ich kaufe einen Kaffee.",
        })
        self.assertFalse(result["correct"])
        self.assertIsNone(result["grammar_correct"])
        self.assertEqual(result["evaluation_status"], "uncertain")

    def test_multiple_errors_are_recorded_without_false_positive(self):
        result = evaluate_structured_answer("Ich kaufen ein Kaffee", {
            "type": "translation", "answer": "Ich kaufe einen Kaffee",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])
        self.assertEqual([error["type"] for error in result["errors"]], ["conjugation", "article"])

    def test_negation_does_not_satisfy_translation(self):
        result = evaluate_structured_answer("Ich kaufe keinen Kaffee", {
            "type": "translation", "answer": "Ich kaufe einen Kaffee",
        })
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertEqual(result["errors"][0]["type"], "negation")

    def test_b1_perfect_auxiliary_requires_review(self):
        result = evaluate_structured_answer("Ich bin gestern einen Film gesehen.", {
            "type": "translation", "answer": "Ich habe gestern einen Film gesehen.",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])

    def test_b2_subordinate_clause_word_order_requires_review(self):
        result = evaluate_structured_answer("Obwohl es regnet, ich gehe spazieren.", {
            "type": "writing", "answer": "Obwohl es regnet, gehe ich spazieren.",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])

    def test_explicit_b2_alternative_is_accepted(self):
        result = evaluate_structured_answer("Trotz des Regens gehe ich spazieren.", {
            "type": "writing", "answer": "Obwohl es regnet, gehe ich spazieren.",
            "accepted_answers": [
                "Obwohl es regnet, gehe ich spazieren.",
                "Trotz des Regens gehe ich spazieren.",
            ],
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertTrue(result["correct"])

    def test_auxiliary_candidate_is_identified_without_forcing_rejection(self):
        result = evaluate_structured_answer("Wir haben nach Hamburg gefahren.", {
            "type": "translation", "answer": "Wir sind nach Hamburg gefahren.",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertIn("auxiliary", [item["type"] for item in result["errors"]])

    def test_preposition_candidate_is_identified_without_forcing_rejection(self):
        result = evaluate_structured_answer("Ich interessiere mich an Musik.", {
            "type": "translation", "answer": "Ich interessiere mich für Musik.",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertIn("preposition", [item["type"] for item in result["errors"]])

    def test_unlisted_paraphrase_has_no_speculative_vocabulary_error(self):
        result = evaluate_structured_answer("Sie lebt in Berlin.", {
            "type": "sentence", "answer": "Sie wohnt in Berlin.",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertEqual(result["errors"], [])

    def test_closed_reorder_detects_word_order_difference(self):
        result = evaluate_structured_answer("Heute lernen wir Deutsch.", {
            "type": "reorder", "answer": "Wir lernen heute Deutsch.",
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertEqual(result["errors"][0]["type"], "word_order")

    def test_missing_model_requires_review(self):
        result = evaluate_structured_answer("Hallo", {"type": "translation"})
        self.assertEqual(result["evaluation_status"], "needs_review")
        self.assertFalse(result["correct"])

    def test_wrong_choice_remains_verified_failure(self):
        result = evaluate_structured_answer("nein", {
            "type": "choice", "answer": "ja",
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertFalse(result["correct"])
        self.assertEqual(result["errors"][0]["span"], "nein")

    def test_article_mistake_is_not_a_spelling_success(self):
        result = evaluate_structured_answer("Ich kaufe ein Kaffee", {
            "type": "translation", "answer": "Ich kaufe einen Kaffee",
        })
        self.assertFalse(result["correct"])


if __name__ == "__main__":
    unittest.main()
