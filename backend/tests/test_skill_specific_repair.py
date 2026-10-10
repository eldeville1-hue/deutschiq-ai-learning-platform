import unittest

from app.services.lesson_coaching import repair_plan


class SkillSpecificRepairTests(unittest.TestCase):
    def test_case_repair_does_not_distract_with_word_order(self):
        steps = repair_plan("case", ["dem"], ["den"], "en")
        self.assertEqual(2, len(steps))
        self.assertIn("case", steps[0])
        self.assertIn("article or pronoun", steps[1])
        self.assertNotIn("word order", " ".join(steps).lower())

    def test_perfekt_auxiliary_repair_is_localized(self):
        self.assertIn("haben oder sein", repair_plan("auxiliary", [], [], "de")[0])
        self.assertIn("haben или sein", repair_plan("auxiliary", [], [], "ru")[0])

    def test_unknown_errors_retain_general_guidance(self):
        steps = repair_plan("answer_mismatch", [], [], "en")
        self.assertEqual(3, len(steps))
        self.assertIn("word order", steps[-1])


if __name__ == "__main__":
    unittest.main()
