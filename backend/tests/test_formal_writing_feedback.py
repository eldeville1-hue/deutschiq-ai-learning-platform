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

    def test_missing_closing_gets_specific_repair_hint(self):
        answer = "Sehr geehrte Frau Klein, ich möchte meinen Termin verschieben."
        result = local_feedback(answer, self.exercise, "", "ru", "A2")
        self.assertFalse(result["correct"])
        self.assertIn("Mit freundlichen Grüßen", result["improvement"])

    def test_missing_greeting_does_not_pass(self):
        answer = "Ich möchte meinen Termin verschieben. Mit freundlichen Grüßen, Mia Weber."
        result = local_feedback(answer, self.exercise, "", "en", "A2")
        self.assertFalse(result["correct"])
        self.assertIn("formal_greeting", result["missing_task_parts"])

    def test_complete_model_passes_structure_gate(self):
        result = local_feedback(self.exercise["answer"], self.exercise, "", "en", "A2")
        self.assertEqual(result["missing_task_parts"], [])
        self.assertTrue(result["correct"])

    def test_ai_grading_cannot_override_missing_formal_closing(self):
        from unittest.mock import MagicMock, patch
        from app.services.production_feedback import _ai_feedback
        from app.core.config import settings
        response = MagicMock()
        response.choices[0].message.content = (
            '{"dimension_scores":{"task_completion":100,"grammar":100,'
            '"vocabulary":100,"coherence":100,"register":100},'
            '"feedback":"Good","improvement":"None","corrected_answer":"OK"}'
        )
        client = MagicMock()
        client.chat.completions.create.return_value = response
        with patch("openai.OpenAI", return_value=client):
            result = _ai_feedback(
                "Sehr geehrte Frau Klein, ich möchte meinen Termin verschieben.",
                self.exercise, {"cefr": "A2"}, "en",
            )
        self.assertFalse(result["correct"])
        self.assertIn("formal_closing", result["missing_task_parts"])
        sent = client.chat.completions.create.call_args.kwargs["messages"][1]["content"]
        self.assertIn("alternative_time", sent)

    def test_unrelated_production_not_affected(self):
        exercise = dict(self.exercise, assessment_criteria=[])
        result = local_feedback("Ich habe morgen Zeit.", exercise, "", "en", "A2")
        self.assertEqual(result["missing_task_parts"], [])


if __name__ == "__main__":
    unittest.main()
