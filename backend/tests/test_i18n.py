import unittest

from app.services.content_i18n import LESSON_COPY, localize_lesson_content, normalize_language


class InternationalizationTests(unittest.TestCase):
    def test_all_thirty_lessons_have_english_and_german_copy(self):
        self.assertEqual(30, len(LESSON_COPY["en"]))
        self.assertEqual(30, len(LESSON_COPY["de"]))
        for lang in ("en", "de"):
            for day in range(1, 31):
                content = localize_lesson_content({"day": day, "title": "RU", "rule": "RU", "objective": "RU", "communication_goal": "RU", "exercises": [{"answer": "x"}, {"answer": "Hallo."}, {"answer": "x"}, {"answer": "x"}]}, lang)
                self.assertTrue(content["title"])
                self.assertTrue(content["rule"])
                self.assertNotEqual("RU", content["title"])
                self.assertEqual(4, len(content["exercises"]))
                self.assertTrue(all(item.get("question") for item in content["exercises"]))

    def test_language_codes_are_normalized_safely(self):
        self.assertEqual("de", normalize_language("de-DE"))
        self.assertEqual("ru", normalize_language("ru-RU"))
        self.assertEqual("en", normalize_language("fr"))


if __name__ == "__main__":
    unittest.main()
