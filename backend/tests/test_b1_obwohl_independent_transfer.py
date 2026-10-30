"""Reference B1 lesson: independent obwohl choice must measure transfer."""
import unittest

from app.content.b1_curriculum import B1_CURRICULUM, build_b1_content
from app.services.content_quality import exercise_answer_audit, exercise_instruction_audit


class B1ObwohlIndependentTransferTests(unittest.TestCase):
    def test_choice_uses_a_new_context_and_valid_distractors(self):
        row = next(row for row in B1_CURRICULUM if row[2] == "subordinate_clauses")
        lesson = build_b1_content(row)
        guided = next(item for item in lesson["exercises"] if item["id"] == "subordinate_clauses-guided")
        choice = next(item for item in lesson["exercises"] if item["id"] == "subordinate_clauses-choice")

        self.assertEqual(choice["stage"], "independent")
        self.assertEqual(choice["type"], "context_choice")
        self.assertEqual(choice["answer"], "Obwohl ich müde bin, gehe ich zum Kurs.")
        self.assertNotEqual(choice["answer"].rstrip("."), guided["answer"].rstrip("."))
        self.assertNotIn(choice["answer"], guided["accepted_answers"])
        self.assertEqual(len(choice["options"]), 3)
        self.assertEqual(choice["options"].count(choice["answer"]), 1)
        self.assertTrue(any("Obwohl ich müde bin, ich gehe" in item for item in choice["options"]))
        self.assertTrue(any(item.startswith("Weil") for item in choice["options"]))
        for lang in ("ru", "de", "en"):
            self.assertTrue(choice["i18n"][lang]["question"].strip())
            self.assertTrue(choice["i18n"][lang]["explanation"].strip())
        self.assertEqual(exercise_answer_audit(lesson), [])
        self.assertEqual(exercise_instruction_audit(lesson), [])


if __name__ == "__main__":
    unittest.main()
