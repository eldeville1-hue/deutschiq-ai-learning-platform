import asyncio
import unittest
from unittest.mock import patch

from app.services.production_feedback import evaluate_production


class AdvancedWritingReviewTests(unittest.TestCase):
    def test_b2_unlisted_response_is_pending_without_ai(self):
        exercise = {"type": "production", "question": "Explain your opinion.",
                    "model_answer": "Meiner Meinung nach ist das wichtig."}
        with patch("app.core.config.settings.OPENAI_API_KEY", ""):
            result = asyncio.run(evaluate_production(
                "Meiner Meinung nach ist das wichtig, weil es viele Menschen betrifft.",
                exercise, {"cefr": "B2"}, "de"))
        self.assertTrue(result["assessment_pending"])
        self.assertFalse(result["correct"])

    def test_b1_unlisted_response_is_pending_on_ai_failure(self):
        exercise = {"type": "production", "question": "Explain your opinion.",
                    "model_answer": "Ich denke, dass das wichtig ist."}
        with patch("app.core.config.settings.OPENAI_API_KEY", "test-key"):
            with patch("app.services.production_feedback._ai_feedback", side_effect=RuntimeError("unavailable")):
                result = asyncio.run(evaluate_production(
                    "Ich finde das wichtig, weil ich jeden Tag Deutsch lerne.",
                    exercise, {"cefr": "B1"}, "en"))
        self.assertTrue(result["assessment_pending"])
        self.assertFalse(result["correct"])


if __name__ == "__main__":
    unittest.main()
