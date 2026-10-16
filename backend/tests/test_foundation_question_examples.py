"""Editorial regression tests for unambiguous A1 question examples."""
import unittest

from app.content.foundation_curriculum import A1_CURRICULUM, A2_CURRICULUM


class FoundationQuestionExamplesTests(unittest.TestCase):
    def test_dative_accusative_teaches_roles_not_fixed_order(self):
        row = next(row for row in A2_CURRICULUM if row[2] == "dative_accusative")
        self.assertEqual(row[7], "Empfänger im Dativ, Sache im Akkusativ")
        self.assertEqual(row[8], "Der Lehrer erklärt den Schülern die Aufgabe.")

    def test_perfekt_sein_focus_is_not_all_movement_verbs(self):
        row = next(row for row in A2_CURRICULUM if row[2] == "perfect_sein")
        self.assertIn("Ortswechsel", row[7])
        self.assertIn("fahren", row[7])
        self.assertNotEqual(row[7], "sein bei Bewegung")

    def test_yes_no_question_contrast_is_unambiguously_wrong(self):
        row = next(row for row in A1_CURRICULUM if row[2] == "yes_no_questions")
        self.assertEqual(row[-2], "Wohnst du in Berlin?")
        self.assertEqual(row[-1], "Wohnst in du Berlin?")
        self.assertNotEqual(row[-1], "Du wohnst in Berlin?")


if __name__ == "__main__":
    unittest.main()
