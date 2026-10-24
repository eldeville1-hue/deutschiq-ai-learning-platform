import unittest
from app.services.tutor_writing_bank import WRITING_PROMPTS
from app.services.tutor_writing_feedback import writing_length_feedback


class WritingParagraphFeedbackTests(unittest.TestCase):
    def test_argumentative_single_paragraph_guidance(self):
        result = writing_length_feedback(WRITING_PROMPTS[3][2], " ".join(["Wort"] * 160), "en")
        self.assertIn("separate paragraphs", result)

    def test_paragraph_breaks_recognized(self):
        answer = " ".join(["Wort"] * 80) + "\n\n" + " ".join(["Wort"] * 80)
        result = writing_length_feedback(WRITING_PROMPTS[3][2], answer, "en")
        self.assertIn("Paragraph breaks found", result)
        self.assertNotIn("Consider separate", result)

    def test_email_not_forced_into_essay_structure(self):
        result = writing_length_feedback(WRITING_PROMPTS[0][2], " ".join(["Wort"] * 90), "en")
        self.assertNotIn("separate paragraphs", result)

    def test_localized(self):
        for language in ("ru", "de", "en"):
            result = writing_length_feedback(WRITING_PROMPTS[4][2], " ".join(["Wort"] * 160), language)
            self.assertIn("160 / 150-200", result)
