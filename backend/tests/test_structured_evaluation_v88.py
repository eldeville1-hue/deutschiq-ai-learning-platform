import unittest
from app.services.answer_intelligence import evaluate_structured_answer


class StructuredEvaluationV88Tests(unittest.TestCase):
    def test_unlisted_near_match_in_open_answer_needs_review(self):
        exercise = {"type": "translation", "answer": "Ich besuche meine Freundin morgen."}
        result = evaluate_structured_answer("Ich besuche meine Freundin morgn.", exercise)
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["errors"], [])

    def test_explicitly_accepted_near_match_remains_verified(self):
        response = "Ich besuche meine Freundin morgn."
        result = evaluate_structured_answer(response, {
            "type": "translation", "answer": "Ich besuche meine Freundin morgen.",
            "accepted_answers": ["Ich besuche meine Freundin morgen.", response],
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertTrue(result["correct"])

    def test_tagged_missing_zu_is_tentative_for_open_translation(self):
        result = evaluate_structured_answer("Ich habe vor, morgen arbeiten.", {
            "type": "translation", "answer": "Ich habe vor, morgen zu arbeiten.",
            "target_feature": "infinitive",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertIn("infinitive", result["candidate_error_types"])
        self.assertFalse(result["correct"])

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

    def test_explicit_case_target_classifies_case(self):
        result = evaluate_structured_answer("Ich warte auf dem Bus.", {
            "type": "choice", "answer": "Ich warte auf den Bus.",
            "target_feature": "case",
        })
        self.assertEqual(result["errors"][0]["type"], "case")

    def test_explicit_relative_pronoun_target(self):
        result = evaluate_structured_answer("Das Fahrrad, den ich gekauft habe, ist neu.", {
            "type": "error_repair",
            "answer": "Das Fahrrad, das ich gekauft habe, ist neu.",
            "target_feature": "relative_pronoun",
        })
        self.assertEqual(result["errors"][0]["type"], "relative_pronoun")

    def test_explicit_participle_target(self):
        result = evaluate_structured_answer("Ich habe meine Freundin besuchen.", {
            "type": "error_repair",
            "answer": "Ich habe meine Freundin besucht.",
            "target_feature": "participle",
        })
        self.assertEqual(result["errors"][0]["type"], "participle")

    def test_negating_determiner_case_is_not_polarity_error(self):
        result = evaluate_structured_answer("Ich habe keine Auto.", {
            "type": "error_repair", "answer": "Ich habe kein Auto.",
            "target_feature": "case",
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertFalse(result["correct"])
        self.assertEqual(result["errors"][0]["type"], "case")

    def test_untagged_negating_determiner_remains_conservative(self):
        result = evaluate_structured_answer("Ich habe keine Auto.", {
            "type": "translation", "answer": "Ich habe kein Auto.",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])

    def test_tagged_subjunctive_feedback(self):
        result = evaluate_structured_answer("Ich wurde lieber bleiben.", {
            "type": "error_repair", "answer": "Ich würde lieber bleiben.",
            "target_feature": "subjunctive",
        })
        self.assertEqual(result["errors"][0]["type"], "subjunctive")

    def test_tagged_passive_feedback(self):
        result = evaluate_structured_answer("Die Wohnung werden renoviert.", {
            "type": "error_repair", "answer": "Die Wohnung wird renoviert.",
            "target_feature": "passive",
        })
        self.assertEqual(result["errors"][0]["type"], "passive")

    def test_tagged_adjective_feedback(self):
        result = evaluate_structured_answer("Ich kaufe einen rote Apfel.", {
            "type": "error_repair", "answer": "Ich kaufe einen roten Apfel.",
            "target_feature": "adjective",
        })
        self.assertEqual(result["errors"][0]["type"], "adjective")

    def test_missing_zu_in_infinitive_feedback(self):
        result = evaluate_structured_answer("Ich habe vergessen, die Tür schließen.", {
            "type": "error_repair", "answer": "Ich habe vergessen, die Tür zu schließen.",
            "target_feature": "infinitive",
        })
        self.assertEqual(result["errors"][0]["type"], "infinitive")

    def test_tagged_case_pronoun_feedback(self):
        result = evaluate_structured_answer("Kannst du mich helfen?", {
            "type": "error_repair", "answer": "Kannst du mir helfen?",
            "target_feature": "case",
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertEqual(result["errors"][0]["type"], "case")

    def test_tagged_preposition_feedback(self):
        result = evaluate_structured_answer("Ich wohne für zwei Jahre hier.", {
            "type": "error_repair", "answer": "Ich wohne seit zwei Jahre hier.",
            "target_feature": "preposition",
        })
        self.assertEqual(result["errors"][0]["type"], "preposition")

    def test_tagged_auxiliary_conjugation_feedback(self):
        result = evaluate_structured_answer("Sie haben einen Hund.", {
            "type": "error_repair", "answer": "Sie hat einen Hund.",
            "target_feature": "conjugation",
        })
        self.assertEqual(result["errors"][0]["type"], "conjugation")

    def test_tagged_second_person_conjugation(self):
        result = evaluate_structured_answer("Du lern Deutsch.", {
            "type": "error_repair", "answer": "Du lernst Deutsch.",
            "target_feature": "conjugation",
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertEqual(result["errors"][0]["type"], "conjugation")

    def test_open_conjugation_remains_uncertain(self):
        result = evaluate_structured_answer("Du lern Deutsch.", {
            "type": "translation", "answer": "Du lernst Deutsch.",
            "target_feature": "conjugation",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])

    def test_unannotated_case_remains_conservative(self):
        result = evaluate_structured_answer("Ich warte auf dem Bus.", {
            "type": "choice", "answer": "Ich warte auf den Bus.",
        })
        self.assertEqual(result["errors"][0]["type"], "article")

    def test_tagged_missing_zu_is_infinitive_error(self):
        result = evaluate_structured_answer("Die Massnahme trägt dazu bei, Energie sparen.", {
            "type": "error_repair",
            "answer": "Die Massnahme trägt dazu bei, Energie zu sparen.",
            "target_feature": "infinitive",
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertEqual(result["errors"][0]["type"], "infinitive")

    def test_uncertain_answer_exposes_review_reason_without_awarding_credit(self):
        result = evaluate_structured_answer("Sie lebt in Berlin.", {
            "type": "sentence", "answer": "Sie wohnt in Berlin.",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertEqual(result["review_reason"], "open_answer_not_proven_equivalent_or_incorrect")
        self.assertEqual(result["candidate_error_types"], [])
        self.assertEqual(result["score"], 0)
        self.assertFalse(result["correct"])

    def test_candidate_errors_remain_tentative(self):
        result = evaluate_structured_answer("Ich habe gestern nach Hause gegangen.", {
            "type": "translation", "answer": "Ich bin gestern nach Hause gegangen.",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertIn("auxiliary", result["candidate_error_types"])
        self.assertFalse(result["correct"])

    def test_missing_reference_has_review_reason(self):
        result = evaluate_structured_answer("Hallo", {"type": "free_text"})
        self.assertEqual(result["evaluation_status"], "needs_review")
        self.assertEqual(result["review_reason"], "missing_reference_answer")

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
