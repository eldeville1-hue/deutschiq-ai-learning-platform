"""Regression: retry examples cannot reveal any authored answer key."""
import unittest

from app.services.content_quality import validate_lesson_content


class RetryAnswerKeyValidationTests(unittest.TestCase):
    def lesson(self, sentence):
        return {
            "objective": "Practice", "rule": "Use the target form.",
            "examples": ["Ich lerne Deutsch."], "audio_text": "Ich lerne Deutsch.",
            "common_mistakes": ["Check the form."],
            "exercises": [{
                "type": "fill", "question": "Complete the sentence",
                "answer": "Heute lerne ich Deutsch.",
                "accepted_answers": ["Ich lerne heute Deutsch."],
                "explanation": "Verb in second position.", "skill_id": "word_order",
            }],
            "retry_examples": [{"skill_id": "word_order", "sentence": sentence}],
        }

    def test_primary_answer_is_rejected_even_with_alternatives(self):
        issues = validate_lesson_content(self.lesson("Heute lerne ich Deutsch."))
        self.assertIn("retry:0:duplicate_answer", issues)

    def test_accepted_alternative_is_rejected(self):
        issues = validate_lesson_content(self.lesson("Ich lerne heute Deutsch."))
        self.assertIn("retry:0:duplicate_answer", issues)

    def test_distinct_retry_sentence_is_allowed(self):
        issues = validate_lesson_content(self.lesson("Morgen lerne ich Deutsch."))
        self.assertNotIn("retry:0:duplicate_answer", issues)


if __name__ == "__main__":
    unittest.main()
