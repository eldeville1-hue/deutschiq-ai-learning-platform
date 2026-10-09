import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class KeinInflectionDiagnosisV88Tests(unittest.TestCase):
    def test_keinen_vs_kein_is_not_a_polarity_change(self):
        result = evaluate_structured_answer("Ich habe keinen Brot.", {
            "type": "error_repair", "answer": "Ich habe kein Brot.",
        })
        self.assertFalse(result["correct"])
        self.assertNotIn("negation", [error["type"] for error in result["errors"]])

    def test_case_objective_keeps_case_diagnosis(self):
        result = evaluate_structured_answer("Ich habe keinen Brot.", {
            "type": "error_repair", "answer": "Ich habe kein Brot.",
            "target_feature": "case",
        })
        self.assertIn("case", [error["type"] for error in result["errors"]])

    def test_added_nicht_is_a_negation_difference(self):
        result = evaluate_structured_answer("Ich habe nicht Brot.", {
            "type": "error_repair", "answer": "Ich habe Brot.",
            "target_feature": "negation",
        })
        self.assertFalse(result["correct"])


if __name__ == "__main__":
    unittest.main()
