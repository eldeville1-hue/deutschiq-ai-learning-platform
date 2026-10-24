import unittest
from app.services.tutor_writing_bank import WRITING_PROMPTS, WRITING_CRITERIA
from app.services.tutor_fallback import fallback_answer
from app.services.tutor_verified_practice import grade_reviewed_word_order


class WritingPromptTests(unittest.TestCase):
    def test_three_prompts_per_level(self):
        self.assertEqual(sum(row[1] == "B1" for row in WRITING_PROMPTS), 3)
        self.assertEqual(sum(row[1] == "B2" for row in WRITING_PROMPTS), 3)

    def test_localized_prompt_and_self_check(self):
        for level in ("B1", "B2"):
            for language in ("ru", "de", "en"):
                response = fallback_answer("writing task", language, level, [])
                self.assertIn(WRITING_CRITERIA[language], response)
                self.assertTrue(any(row[2] in response for row in WRITING_PROMPTS if row[1] == level))

    def test_rotation(self):
        first = fallback_answer("writing task", "en", "B2", [])
        second = fallback_answer("writing task", "en", "B2", [], [first])
        self.assertNotEqual(first, second)

    def test_open_text_is_not_string_graded(self):
        prompt = fallback_answer("writing task", "en", "B2", [])
        self.assertIsNone(grade_reviewed_word_order(prompt, "Ich bin der Meinung, dass Bildung wichtig ist."))


if __name__ == "__main__":
    unittest.main()
