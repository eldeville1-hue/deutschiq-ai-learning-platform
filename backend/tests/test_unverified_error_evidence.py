import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class UnverifiedErrorEvidenceTests(unittest.TestCase):
    def test_open_response_does_not_expose_hypotheses_as_errors(self):
        exercise = {"type": "translation", "answer": "Ich sehe den Mann.",
                    "target_feature": "case"}
        result = evaluate_structured_answer("Ich sehe dem Mann.", exercise)
        self.assertEqual("uncertain", result["evaluation_status"])
        self.assertFalse(result["correct"])
        self.assertEqual([], result["errors"])
        self.assertIsNone(result["error_type"])
        self.assertIn("case", result["candidate_error_types"])

    def test_objective_task_still_returns_verified_errors(self):
        exercise = {"type": "fill", "answer": "den", "target_feature": "case"}
        result = evaluate_structured_answer("dem", exercise)
        self.assertEqual("verified", result["evaluation_status"])
        self.assertFalse(result["correct"])
        self.assertTrue(result["errors"])


if __name__ == "__main__":
    unittest.main()
