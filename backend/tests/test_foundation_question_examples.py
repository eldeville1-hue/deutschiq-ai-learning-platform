"""Editorial regression tests for unambiguous A1 question examples."""
import unittest

from app.content.foundation_curriculum import A1_CURRICULUM


class FoundationQuestionExamplesTests(unittest.TestCase):
    def test_yes_no_question_contrast_is_unambiguously_wrong(self):
        row = next(row for row in A1_CURRICULUM if row[2] == "yes_no_questions")
        self.assertEqual(row[-2], "Wohnst du in Berlin?")
        self.assertEqual(row[-1], "Wohnst in du Berlin?")
        self.assertNotEqual(row[-1], "Du wohnst in Berlin?")


if __name__ == "__main__":
    unittest.main()
