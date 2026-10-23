import asyncio
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.services.production_feedback import _ai_feedback, evaluate_production


class ActionableWritingFeedbackTests(unittest.TestCase):
    def test_missing_diagnosis_or_next_step_is_not_verified(self):
        exercise = {"type": "production", "question": "Begründe deine Meinung.",
                    "answer": "Ich denke, dass das sinnvoll ist."}
        scores = {name: 30 for name in
                  ("task_completion", "grammar", "vocabulary", "coherence", "register")}
        for omitted in ("feedback", "improvement"):
            with self.subTest(omitted=omitted):
                payload = {"dimension_scores": scores, "feedback": "Check word order.",
                           "improvement": "Move the conjugated verb to the end."}
                payload.pop(omitted)
                with patch("openai.OpenAI") as client:
                    client.return_value.chat.completions.create.return_value = SimpleNamespace(
                        choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))]
                    )
                    with patch("app.core.config.settings.OPENAI_API_KEY", "test-key"):
                        result = asyncio.run(evaluate_production(
                            "Ich denke das gut.", exercise, {"cefr": "B2"}, "en"))
                self.assertFalse(result["correct"])
                self.assertTrue(result["assessment_pending"])

    def test_complete_actionable_feedback_is_accepted(self):
        exercise = {"question": "Begründe deine Meinung.", "answer": "Ich denke, dass das sinnvoll ist."}
        payload = {"dimension_scores": {name: 30 for name in
                   ("task_completion", "grammar", "vocabulary", "coherence", "register")},
                   "feedback": "The subordinate clause is missing.",
                   "improvement": "Add dass and put the conjugated verb at the end."}
        with patch("openai.OpenAI") as client:
            client.return_value.chat.completions.create.return_value = SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))]
            )
            result = _ai_feedback("Ich denke das gut.", exercise, {"cefr": "B2"}, "en")
        self.assertFalse(result["correct"])
        self.assertEqual("The subordinate clause is missing.", result["feedback"])
        self.assertIn("dass", result["improvement"])


if __name__ == "__main__":
    unittest.main()
