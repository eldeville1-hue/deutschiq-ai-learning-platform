"""Prevent invalid multiple-choice exercises from passing curriculum validation."""
import unittest

from app.services.content_quality import validate_lesson_content


def lesson(exercise):
    return {
        "objective": "Choose the correct form.",
        "rule": "Match subject and verb.",
        "examples": ["Er ist hier."],
        "audio_text": "Er ist hier.",
        "common_mistakes": ["Er sind hier is wrong."],
        "exercises": [{
            "type": "choose",
            "question": "Er ___ hier.",
            "answer": "ist",
            "explanation": "Er takes ist.",
            **exercise,
        }],
    }


class ChoiceQualityGateTests(unittest.TestCase):
    def test_valid_options(self):
        self.assertEqual(validate_lesson_content(lesson({"options": ["ist", "sind"]})), [])

    def test_missing_correct_option(self):
        self.assertIn("exercise:0:correct_answer_not_in_options",
                      validate_lesson_content(lesson({"options": ["bin", "sind"]})))

    def test_duplicate_options(self):
        self.assertIn("exercise:0:duplicate_or_empty_options",
                      validate_lesson_content(lesson({"options": ["ist", " IST "]})))

    def test_too_few_options(self):
        self.assertIn("exercise:0:insufficient_options",
                      validate_lesson_content(lesson({"options": ["ist"]})))

    def test_authored_accepted_alternative(self):
        self.assertEqual(validate_lesson_content(lesson({
            "answer": "ist", "accepted_answers": ["ist", "is"],
            "options": ["is", "are"],
        })), [])


if __name__ == "__main__":
    unittest.main()
