import asyncio
import unittest
from unittest.mock import patch

from app.services.production_feedback import evaluate_production


class ExactAdvancedModelAnswerTests(unittest.TestCase):
    def test_b2_authored_model_receives_full_credit_without_ai(self):
        answer = "Da die Nachfrage gestiegen ist, wurden zusätzliche Kurse angeboten."
        exercise = {"type": "production", "answer": answer, "model_answer": answer}
        with patch("app.core.config.settings.OPENAI_API_KEY", ""):
            result = asyncio.run(evaluate_production(answer, exercise, {"cefr": "B2"}, "de"))
        self.assertTrue(result["correct"])
        self.assertEqual(100, result["score"])
        self.assertTrue(all(value == 100 for value in result["dimension_scores"].values()))
        self.assertFalse(result.get("assessment_pending", False))

    def test_unlisted_b2_response_still_requires_review(self):
        exercise = {"type": "production", "answer": "Da die Nachfrage gestiegen ist, wurden zusätzliche Kurse angeboten."}
        with patch("app.core.config.settings.OPENAI_API_KEY", ""):
            result = asyncio.run(evaluate_production(
                "Weil die Nachfrage größer geworden ist, gibt es jetzt mehr Kurse.",
                exercise, {"cefr": "B2"}, "de"))
        self.assertFalse(result["correct"])
        self.assertTrue(result["assessment_pending"])


if __name__ == "__main__":
    unittest.main()
