import unittest

from app.services.evaluation_contract import (
    EvaluationResult, LinguisticError, evidence_from_evaluation,
)


class EvaluationContractTests(unittest.TestCase):
    def test_grammar_and_task_success_are_distinct(self):
        result = EvaluationResult(
            grammar_correct=True, meaning_correct=False, task_satisfied=False,
            correct=False, evaluation_status="verified",
            errors=[LinguisticError("negation", "keinen", "einen", "Negation changes the requested meaning.")],
            error_type="negation",
        )
        self.assertTrue(result.grammar_correct)
        self.assertFalse(result.correct)
        self.assertEqual(result.to_dict()["errors"][0]["span"], "keinen")

    def test_multiple_errors_keep_primary_compatibility(self):
        errors = [
            LinguisticError("conjugation", "kaufen", "kaufe", "First person singular requires kaufe."),
            LinguisticError("case", "ein Kaffee", "einen Kaffee", "The object takes accusative."),
        ]
        result = EvaluationResult(False, True, False, False, "verified", errors=errors, error_type="conjugation")
        self.assertEqual(len(result.to_dict()["errors"]), 2)

    def test_uncertain_answer_cannot_pass(self):
        with self.assertRaises(ValueError):
            EvaluationResult(None, None, None, True, "uncertain")
        with self.assertRaises(ValueError):
            EvaluationResult(None, None, None, True, "needs_review")

    def test_verified_success_requires_task_satisfaction(self):
        with self.assertRaises(ValueError):
            EvaluationResult(True, True, False, True, "verified")

    def test_evidence_preserves_independent_and_assisted_distinction(self):
        independent = EvaluationResult(True, True, True, True, "verified")
        assisted = EvaluationResult(True, True, True, True, "verified", assistance_level="guided_retry")
        self.assertTrue(evidence_from_evaluation(independent, skill="accusative", attempt_number=1)["independent_verified_success"])
        self.assertFalse(evidence_from_evaluation(assisted, skill="accusative", attempt_number=2)["independent_verified_success"])


if __name__ == "__main__":
    unittest.main()
