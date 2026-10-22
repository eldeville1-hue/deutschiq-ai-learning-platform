import unittest

from app.services.lesson_coaching import repair_plan


class AdvancedRepairPlanTests(unittest.TestCase):
    def test_advanced_errors_have_two_targeted_steps_without_answer_leakage(self):
        errors = ("verb_not_final", "wrong_connector", "relative_case", "passive_auxiliary", "modal_form", "infinitive")
        for lang in ("ru", "de", "en"):
            for error in errors:
                with self.subTest(lang=lang, error=error):
                    steps = repair_plan(error, ["GEHEIMWORT"], ["FALSCHWORT"], lang)
                    self.assertEqual(len(steps), 2)
                    self.assertNotIn("GEHEIMWORT", " ".join(steps))
                    self.assertNotIn("FALSCHWORT", " ".join(steps))

    def test_subordinate_clause_repair_mentions_verb_position(self):
        self.assertIn("глагол", repair_plan("verb_not_final", [], [], "ru")[1])
        self.assertIn("Verb", repair_plan("verb_not_final", [], [], "de")[1])
        self.assertIn("verb", repair_plan("verb_not_final", [], [], "en")[1])


if __name__ == "__main__":
    unittest.main()
