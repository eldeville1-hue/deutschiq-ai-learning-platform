import unittest

from app.services.production_feedback import local_feedback


class FormalWritingFeedbackTests(unittest.TestCase):
    def setUp(self):
        self.exercise = {
            "type": "production",
            "answer": "Sehr geehrte Frau Klein, ich möchte meinen Termin verschieben. Mit freundlichen Grüßen, Mia Weber.",
            "assessment_criteria": ["formal_greeting", "rescheduling_request", "alternative_time", "formal_closing"],
            "target_patterns": ["Sehr geehrte", "Termin", "Mit freundlichen Grüßen"],
        }

    def test_missing_closing_does_not_pass(self):
        answer = "Sehr geehrte Frau Klein, ich möchte meinen Termin verschieben. Am Dienstag habe ich Zeit."
        result = local_feedback(answer, self.exercise, "", "de", "A2")
        self.assertFalse(result["correct"])
        self.assertIn("formal_closing", result["missing_task_parts"])

    def test_missing_greeting_does_not_pass(self):
        answer = "Ich möchte meinen Termin verschieben. Mit freundlichen Grüßen, Mia Weber."
        result = local_feedback(answer, self.exercise, "", "en", "A2")
        self.assertFalse(result["correct"])
        self.assertIn("formal_greeting", result["missing_task_parts"])

    def test_complete_model_passes_structure_gate(self):
        result = local_feedback(self.exercise["answer"], self.exercise, "", "en", "A2")
        self.assertEqual(result["missing_task_parts"], [])
        self.assertTrue(result["correct"])

    def test_unrelated_production_not_affected(self):
        exercise = dict(self.exercise, assessment_criteria=[])
        result = local_feedback("Ich habe morgen Zeit.", exercise, "", "en", "A2")
        self.assertEqual(result["missing_task_parts"], [])


if __name__ == "__main__":
    unittest.main()
