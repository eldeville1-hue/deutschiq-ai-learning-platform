"""Editorial regression checks for localized authored lesson instructions."""
import unittest

from app.services.content_quality import exercise_instruction_audit


class LessonInstructionQualityGateTests(unittest.TestCase):
    def test_blank_localized_instruction_is_reported_with_exact_exercise(self):
        lesson = {"exercises": [
            {"type": "fill", "question": "Complete the sentence.",
             "explanation": "Check the article.", "answer": "der",
             "i18n": {
                 "ru": {"question": "  ", "explanation": "Проверь артикль."},
                 "de": {"question": "Ergänze den Satz.", "explanation": ""},
                 "en": {"question": "Complete the sentence.", "explanation": "Check the article."},
             }},
        ]}
        self.assertEqual(
            ["exercise:0:empty_ru_question", "exercise:0:empty_de_explanation"],
            exercise_instruction_audit(lesson),
        )

    def test_nonempty_localized_copy_is_not_flagged(self):
        lesson = {"exercises": [
            {"type": "fill", "question": "Complete the sentence.",
             "explanation": "Check the article.", "answer": "der",
             "i18n": {
                 "ru": {"question": "Заполни пропуск.", "explanation": "Проверь артикль."},
                 "de": {"question": "Ergänze den Satz.", "explanation": "Prüfe den Artikel."},
                 "en": {"question": "Complete the sentence.", "explanation": "Check the article."},
             }},
        ]}
        self.assertEqual([], exercise_instruction_audit(lesson))

    def test_absent_optional_translation_is_not_a_false_positive(self):
        lesson = {"exercises": [
            {"type": "fill", "question": "Complete the sentence.",
             "explanation": "Check the article.", "answer": "der",
             "i18n": {"de": {"question": "Ergänze den Satz."}}},
        ]}
        self.assertEqual([], exercise_instruction_audit(lesson))


if __name__ == "__main__":
    unittest.main()
