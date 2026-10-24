import unittest
from app.services.tutor_writing_bank import WRITING_PROMPTS
from app.services.tutor_writing_feedback import writing_length_feedback


class WritingLengthFeedbackTests(unittest.TestCase):
    def test_short_within_and_long(self):
        prompt = WRITING_PROMPTS[0][2]
        for size, phrase in ((3, "shorter"), (90, "within"), (120, "longer")):
            result = writing_length_feedback(prompt, " ".join(["Wort"] * size), "en")
            self.assertIn(phrase, result)
            self.assertIn("not content, grammar", result)

    def test_not_a_writing_prompt(self):
        self.assertIsNone(writing_length_feedback("Ordne die Woerter", "Ich lerne.", "en"))

    def test_all_languages(self):
        for lang in ("ru", "de", "en"):
            result = writing_length_feedback(WRITING_PROMPTS[3][2], " ".join(["Wort"] * 160), lang)
            self.assertIn("160 / 150-200", result)

    def test_empty_text_not_assessed(self):
        self.assertIsNone(writing_length_feedback(WRITING_PROMPTS[0][2], "  ", "en"))
