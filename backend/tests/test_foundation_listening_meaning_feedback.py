import unittest

from app.content.foundation_curriculum import A1_CURRICULUM, A2_CURRICULUM, build_foundation_content
from app.services.content_i18n import localize_lesson_content


class FoundationListeningMeaningFeedbackTests(unittest.TestCase):
    def test_starter_listening_feedback_explains_what_was_heard(self):
        for level, rows in (("A1", A1_CURRICULUM), ("A2", A2_CURRICULUM)):
            for row in rows:
                lesson = build_foundation_content(row, level)
                for language, prefix in (("ru", "Ты услышал:"), ("de", "Du hast gehört:"), ("en", "You heard:")):
                    localized = localize_lesson_content(lesson, language)
                    for task in localized["exercises"]:
                        if task["type"] != "listening_choice" or not task.get("id", "").endswith("-listen"):
                            continue
                        with self.subTest(level=level, topic=row[2], language=language):
                            explanation = task["explanation"]
                            self.assertTrue(explanation.startswith(prefix), explanation)
                            self.assertIn(task["audio_text"], explanation)
                            self.assertIn(task["answer"], explanation)


if __name__ == "__main__":
    unittest.main()
