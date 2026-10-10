import unittest

from app.content.a2_editorial import A2_GRAMMAR_RULES, A2_LISTENING_MEANINGS, A2_REPAIR_ALTERNATIVES
from app.content.foundation_curriculum import A1_CURRICULUM, A2_CURRICULUM, A2_MISSION_BLUEPRINTS, build_foundation_content
from app.services.answer_intelligence import evaluate_structured_answer, normalize_text
from app.services.content_i18n import localize_lesson_content


class A2EditorialReviewTests(unittest.TestCase):
    def test_localized_listening_distractors_fail_across_both_foundation_tracks(self):
        for level, curriculum in (("A1", A1_CURRICULUM), ("A2", A2_CURRICULUM)):
            for row in curriculum:
                for lang in ("ru", "de", "en"):
                    content = localize_lesson_content(build_foundation_content(row, level), lang)
                    exercise = next(e for e in content["exercises"] if e["type"] == "listening_choice")
                    for option in exercise["options"]:
                        with self.subTest(level=level, topic=row[2], language=lang, option=option):
                            self.assertEqual(option == exercise["answer"], evaluate_structured_answer(option, exercise)["correct"])

    def test_unicode_answers_are_preserved_and_empty_answers_never_pass(self):
        self.assertEqual("приветствие и имя", normalize_text("Приветствие и имя!"))
        self.assertEqual("große straße", normalize_text("Große Straße!"))
        for answer in ("", "!!!"):
            self.assertFalse(evaluate_structured_answer(answer, {"answer": ""})["correct"])

    def test_all_twenty_recorded_models_have_specific_rules_and_meanings(self):
        topics = {row[2] for row in A2_CURRICULUM}
        self.assertEqual(topics, set(A2_GRAMMAR_RULES))
        self.assertEqual(topics, set(A2_LISTENING_MEANINGS))
        for row in A2_CURRICULUM:
            content = build_foundation_content(row, "A2")
            self.assertEqual(row[8], content["audio_text"])
            for index, lang in enumerate(("ru", "de", "en")):
                with self.subTest(topic=row[2], language=lang):
                    localized = localize_lesson_content(content, lang)
                    listening = next(e for e in localized["exercises"] if e["type"] == "listening_choice")
                    self.assertEqual(A2_GRAMMAR_RULES[row[2]][index], localized["rule"])
                    self.assertEqual(A2_LISTENING_MEANINGS[row[2]][index], listening["answer"])
                    self.assertEqual(row[8], listening["audio_text"])
                    for option in listening["options"]:
                        self.assertEqual(option == listening["answer"], evaluate_structured_answer(option, listening)["correct"])

    def test_context_choices_use_the_actual_mission_instead_of_unrelated_recording(self):
        for row in A2_CURRICULUM:
            content = build_foundation_content(row, "A2")
            blueprint = A2_MISSION_BLUEPRINTS[row[2]]
            expected = ("\n".join(turn[3] for turn in blueprint["turns"])
                        if row[2] == "formal_message_a2" else blueprint["turns"][0][3])
            for exercise in content["exercises"]:
                if exercise["type"] not in {"context_choice", "analogy_choice"}:
                    continue
                with self.subTest(topic=row[2], kind=exercise["type"]):
                    self.assertEqual(expected, exercise["answer"])
                    for option in exercise["options"]:
                        self.assertEqual(option == expected, evaluate_structured_answer(option, exercise)["correct"])

    def test_all_grammar_models_pass_and_deliberate_errors_fail(self):
        for row in A2_CURRICULUM:
            with self.subTest(topic=row[2]):
                exercise = {"type": "error_repair", "answer": row[8]}
                self.assertTrue(evaluate_structured_answer(row[8], exercise)["correct"])
                self.assertFalse(evaluate_structured_answer(row[9], exercise)["correct"])

    def test_natural_repairs_are_accepted_for_every_repair_lesson(self):
        for row in A2_CURRICULUM:
            content = build_foundation_content(row, "A2")
            for exercise in content["exercises"]:
                if exercise["type"] != "error_repair":
                    continue
                for answer in A2_REPAIR_ALTERNATIVES.get(row[2], []):
                    with self.subTest(topic=row[2], answer=answer):
                        self.assertTrue(evaluate_structured_answer(answer, exercise)["correct"])

    def test_formal_message_gold_answer_includes_the_requested_closing(self):
        content = build_foundation_content(A2_CURRICULUM[16], "A2")
        for lang in ("ru", "de", "en"):
            localized = localize_lesson_content(content, lang)
            dialogue = next(e for e in localized["exercises"] if e["type"] == "dialogue")
            self.assertIn("Sehr geehrte Frau Klein", dialogue["model_answer"])
            self.assertIn("Könnten Sie", dialogue["model_answer"])
            self.assertTrue(dialogue["model_answer"].endswith("Mit freundlichen Grüßen\nAlex Weber"))
            self.assertIn("Mit freundlichen Grüßen", dialogue["conversation_turns"][-1]["model"])

    def test_final_context_addresses_lateness_not_relocation(self):
        content = build_foundation_content(A2_CURRICULUM[-1], "A2")
        choice = next(e for e in content["exercises"] if e["type"] == "analogy_choice")
        self.assertEqual("Entschuldigung. Mein Zug ist ausgefallen.", choice["answer"])
        self.assertNotIn("umgezogen", choice["answer"])


if __name__ == "__main__":
    unittest.main()
