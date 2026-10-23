import unittest

from app.services.lesson_coaching import repair_plan


class RepairPlanRegionalLocaleTests(unittest.TestCase):
    def test_regional_locale_uses_correct_language(self):
        for language, regional in (("ru", "ru-RU"), ("de", "de-DE"), ("en", "en-US")):
            for error in ("relative_case", "verb_not_final", "article", "missing_words"):
                with self.subTest(regional=regional, error=error):
                    self.assertEqual(
                        repair_plan(error, ["ein"], [], language),
                        repair_plan(error, ["ein"], [], regional),
                    )

    def test_unknown_locale_falls_back_to_english(self):
        self.assertEqual(repair_plan("article", [], [], "fr-FR"), repair_plan("article", [], [], "en"))


if __name__ == "__main__":
    unittest.main()
