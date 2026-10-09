import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class OpenAlternativeDiagnosisSafetyTests(unittest.TestCase):
    def test_unlisted_open_answer_with_multiple_references_has_no_speculative_diagnosis(self):
        result = evaluate_structured_answer("Ich habe kein Brot.", {
            "type": "translation",
            "answer": "Ich habe ein Brot.",
            "accepted_answers": ["Ein Brot habe ich."],
            "target_feature": "negation",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertFalse(result["correct"])
        self.assertEqual(result["candidate_error_types"], [])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["score"], 0)

    def test_single_reference_can_keep_tentative_negation_candidate(self):
        result = evaluate_structured_answer("Ich habe kein Brot.", {
            "type": "translation",
            "answer": "Ich habe ein Brot.",
            "target_feature": "negation",
        })
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertIn("negation", result["candidate_error_types"])

    def test_multiple_reference_exact_answer_is_verified(self):
        result = evaluate_structured_answer("Ein Brot habe ich.", {
            "type": "translation",
            "answer": "Ich habe ein Brot.",
            "accepted_answers": ["Ein Brot habe ich."],
        })
        self.assertEqual(result["evaluation_status"], "verified")
        self.assertTrue(result["correct"])


if __name__ == "__main__":
    unittest.main()
