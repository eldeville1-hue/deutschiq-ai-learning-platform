import unittest

from app.services.content_i18n import localize_lesson_content


class IndependentExerciseLocalizationTests(unittest.TestCase):
    def test_exercise_translations_apply_without_lesson_metadata(self):
        source = {"day": 45, "title": "Legacy", "exercises": [{
            "type": "repeat", "question": "Повтори", "answer": "Ich lerne Deutsch.",
            "i18n": {"de": {"question": "Sprich nach."}, "en": {"question": "Repeat aloud."}, "ru": {"question": "Повтори вслух."}}
        }]}
        for language, expected in (("ru", "Повтори вслух."), ("de", "Sprich nach."), ("en", "Repeat aloud.")):
            with self.subTest(language=language):
                result = localize_lesson_content(source, language)
                self.assertEqual(result["exercises"][0]["question"], expected)
                self.assertNotIn("i18n", result["exercises"][0])
                self.assertNotIn("_authored_localization", result["exercises"][0])
        self.assertEqual(source["exercises"][0]["question"], "Повтори")

    def test_legacy_day_fallback_does_not_override_authored_question(self):
        source = {"day": 1, "exercises": [
            {"question": "Исходное", "i18n": {"en": {"question": "Use your own example."}}},
            {"question": "Слушай"}
        ]}
        result = localize_lesson_content(source, "en")
        self.assertEqual(result["exercises"][0]["question"], "Use your own example.")
        self.assertEqual(result["exercises"][1]["question"], "Listen and write the sentence in German.")


if __name__ == "__main__":
    unittest.main()
