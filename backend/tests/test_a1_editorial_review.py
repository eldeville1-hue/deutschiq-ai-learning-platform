import unittest

from app.content.foundation_curriculum import A1_CURRICULUM, build_foundation_content
from app.services.answer_intelligence import evaluate_structured_answer, word_diff


class A1EditorialReviewTests(unittest.TestCase):
    def test_all_a1_models_pass_and_grammar_distractors_fail(self):
        for row in A1_CURRICULUM:
            content = build_foundation_content(row, "A1")
            model, wrong = content["examples"][0], content["examples"][2].removeprefix("❌ ")
            for kind in ("reorder", "error_repair", "context_choice"):
                with self.subTest(topic=row[2], kind=kind):
                    exercise = {"answer": model, "type": kind}
                    self.assertTrue(evaluate_structured_answer(model, exercise)["correct"])
                    self.assertFalse(evaluate_structured_answer(wrong, exercise)["correct"])

    def test_close_grammar_errors_are_not_spelling_variants(self):
        cases = [
            ("Ich kaufe einen Kaffee und ein Brötchen.", "Ich kaufe einen Kaffee und einen Brötchen."),
            ("Wir lernen jeden Abend Deutsch.", "Wir lernt jeden Abend Deutsch."),
            ("Der Termin ist am Montag um zehn Uhr.", "Der Termin ist um Montag am zehn Uhr."),
            ("Ich habe keine Fahrkarte.", "Ich habe eine Fahrkarte."),
        ]
        for model, answer in cases:
            with self.subTest(answer=answer):
                self.assertFalse(evaluate_structured_answer(answer, {"answer": model})["correct"])

    def test_explicit_alternatives_remain_accepted(self):
        exercise = {"type": "error_repair", "answer": "Heute lerne ich Deutsch.",
                    "accepted_answers": ["Heute lerne ich Deutsch.", "Ich lerne heute Deutsch."]}
        self.assertTrue(evaluate_structured_answer("Ich lerne heute Deutsch!", exercise)["correct"])

    def test_a1_repair_accepts_natural_alternative_order(self):
        content = build_foundation_content(A1_CURRICULUM[2], "A1")
        repair = next(item for item in content["exercises"] if item["type"] == "error_repair")
        self.assertTrue(evaluate_structured_answer("Ich lerne heute Deutsch.", repair)["correct"])
        self.assertFalse(evaluate_structured_answer("Heute ich lerne Deutsch.", repair)["correct"])

    def test_missing_repeated_word_is_reported(self):
        self.assertEqual(["deutsch"], word_diff("Ich lerne Deutsch", "Ich lerne Deutsch Deutsch")["missing"])

    def test_later_a1_rules_explain_specific_forms_in_all_languages(self):
        for row in A1_CURRICULUM[5:]:
            content = build_foundation_content(row, "A1")
            for language in ("ru", "de", "en"):
                with self.subTest(topic=row[2], language=language):
                    rule = content["i18n"][language]["rule"]
                    self.assertIn(":", rule)
                    self.assertNotIn("personal details may be different", rule)


if __name__ == "__main__":
    unittest.main()
