import unittest

from app.services.content_quality import normalize_lesson_content
from app.services.content_i18n import localize_lesson_content


class GeneratedSpeakingPracticeLocalizationTests(unittest.TestCase):
    def test_generated_repeat_is_localized_without_changing_german_answer(self):
        source = {
            "examples": ["Heute lerne ich Deutsch."],
            "i18n": {
                "ru": {"objective": "Практика"},
                "de": {"objective": "Übung"},
                "en": {"objective": "Practice"},
            },
            "exercises": [{"type": "fill", "question": "Fill", "answer": "Deutsch"}],
        }
        normalized = normalize_lesson_content(source, "Deutsch", "A1")
        repeat = normalized["exercises"][-1]
        self.assertEqual(set(repeat["i18n"]), {"ru", "de", "en"})
        expected = {"ru": "Произнеси", "de": "Sprich", "en": "Say"}
        for lang, start in expected.items():
            with self.subTest(language=lang):
                localized = localize_lesson_content(normalized, lang)
                spoken = localized["exercises"][-1]
                self.assertTrue(spoken["question"].startswith(start))
                self.assertEqual(spoken["answer"], "Heute lerne ich Deutsch.")
                self.assertEqual(spoken["accepted_answers"], ["Heute lerne ich Deutsch."])
                self.assertNotIn("i18n", spoken)


if __name__ == "__main__":
    unittest.main()
