import unittest
from app.services.tutor_fallback import fallback_answer
from app.services.tutor_writing_scaffold import SCAFFOLDS


class WritingScaffoldTests(unittest.TestCase):
    def test_all_levels_and_languages(self):
        for level in ("B1", "B2"):
            for language in ("ru", "de", "en"):
                response = fallback_answer("writing task", language, level, [])
                self.assertIn(SCAFFOLDS[level][language], response)

    def test_different_scaffolds(self):
        self.assertNotEqual(SCAFFOLDS["B1"]["en"], SCAFFOLDS["B2"]["en"])

    def test_no_automatic_grade_claim(self):
        self.assertIn("not automatically graded", fallback_answer("writing task", "en", "B2", []))
