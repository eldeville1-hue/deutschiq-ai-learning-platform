import unittest
from app.services.tutor_writing_bank import WRITING_PROMPTS
from app.services.tutor_writing_feedback import writing_length_feedback


class EmailGreetingTests(unittest.TestCase):
    def test_missing_greeting_flagged(self):
        prompt = WRITING_PROMPTS[0][2]
        result = writing_length_feedback(prompt, " ".join(["Ich"] * 90), "en")
        self.assertIn("greeting may be missing", result)

    def test_greeting_recognized(self):
        prompt = WRITING_PROMPTS[0][2]
        result = writing_length_feedback(prompt, "Sehr geehrte Damen und Herren, " + " ".join(["Wort"] * 85), "en")
        self.assertNotIn("greeting may be missing", result)

    def test_no_greeting_requirement_for_essay(self):
        prompt = WRITING_PROMPTS[3][2]
        result = writing_length_feedback(prompt, " ".join(["Wort"] * 160), "en")
        self.assertNotIn("greeting may be missing", result)

    def test_localized_missing_greeting(self):
        prompt = WRITING_PROMPTS[5][2]
        for lang, fragment in (("ru", "обращения"), ("de", "Anrede"), ("en", "greeting")):
            self.assertIn(fragment, writing_length_feedback(prompt, " ".join(["Wort"] * 150), lang))
