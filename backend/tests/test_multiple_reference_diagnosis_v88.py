import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class MultipleReferencesDiagnosisV88Tests(unittest.TestCase):
    def test_closed_task_does_not_invent_grammar_error_from_one_reference(self):
        result = evaluate_structured_answer("Ich kaufe kein Brot.", {
            "type": "error_repair",
            "answer": "Ich kaufe das Brot.",
            "accepted_answers": ["Das Brot kaufe ich."],
            "target_feature": "case",
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertFalse(result["correct"])
        self.assertEqual([error["type"] for error in result["errors"]], ["answer_mismatch"])

    def test_single_reference_still_reports_specific_error(self):
        result = evaluate_structured_answer("Ich kaufe den Brot.", {
            "type": "error_repair",
            "answer": "Ich kaufe das Brot.",
            "target_feature": "case",
        })
        self.assertFalse(result["correct"])
        self.assertIn("case", [error["type"] for error in result["errors"]])

    def test_authored_alternative_is_accepted_without_errors(self):
        result = evaluate_structured_answer("Das Brot kaufe ich.", {
            "type": "error_repair",
            "answer": "Ich kaufe das Brot.",
            "accepted_answers": ["Das Brot kaufe ich."],
        })
        self.assertTrue(result["correct"])
        self.assertEqual(result["errors"], [])


if __name__ == "__main__":
    unittest.main()
