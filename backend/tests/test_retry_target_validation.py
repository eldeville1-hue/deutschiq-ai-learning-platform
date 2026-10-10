import unittest

from app.services.content_quality import validate_lesson_content


def lesson_with_retry(sentence, target):
    return {
        "objective": "Practice Dativ", "rule": "Use Dativ", "examples": ["Ich helfe dir."],
        "audio_text": "Ich helfe dir.", "common_mistakes": ["den / dem"],
        "exercises": [{"type": "fill", "question": "Complete", "answer": "dem",
                       "explanation": "Dativ", "skill_id": "dative_case"}],
        "retry_examples": [{"skill_id": "dative_case", "sentence": sentence, "target": target}],
    }


class RetryTargetValidationTests(unittest.TestCase):
    def test_valid_unique_target(self):
        self.assertEqual([], validate_lesson_content(lesson_with_retry("Ich danke meinem Lehrer.", "meinem")))

    def test_rejects_target_missing_from_sentence(self):
        errors = validate_lesson_content(lesson_with_retry("Ich danke meinem Lehrer.", "deinem"))
        self.assertIn("retry:0:target_not_in_sentence", errors)

    def test_rejects_ambiguous_repeated_target(self):
        errors = validate_lesson_content(lesson_with_retry("Ich gebe dem Mann dem Kind ein Buch.", "dem"))
        self.assertIn("retry:0:ambiguous_target", errors)

    def test_rejects_empty_target(self):
        errors = validate_lesson_content(lesson_with_retry("Ich danke meinem Lehrer.", ""))
        self.assertIn("retry:0:invalid_target", errors)

    def test_legacy_retry_without_target_is_allowed(self):
        content = lesson_with_retry("Ich danke meinem Lehrer.", "meinem")
        del content["retry_examples"][0]["target"]
        self.assertEqual([], validate_lesson_content(content))


if __name__ == "__main__":
    unittest.main()
