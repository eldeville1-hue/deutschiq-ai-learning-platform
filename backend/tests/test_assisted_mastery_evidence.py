"""Mastery evidence must not treat a corrected second attempt as independent recall."""
import unittest

from app.services.learning_engine import adaptive_mastery_update, mastery_evidence_modes


class AssistedEvidenceTests(unittest.TestCase):
    def test_first_attempt_is_independent(self):
        self.assertEqual((False, False), mastery_evidence_modes(0, False, "lesson"))
        self.assertEqual((False, True), mastery_evidence_modes(0, False, "review"))

    def test_repeat_original_task_is_assisted_even_without_retry_flag(self):
        self.assertEqual((True, False), mastery_evidence_modes(1, False, "lesson"))
        self.assertEqual((True, False), mastery_evidence_modes(1, False, "review"))

    def test_guided_retry_is_assisted_even_without_prior_attempts(self):
        self.assertEqual((True, False), mastery_evidence_modes(0, True, "lesson"))
        self.assertEqual((True, False), mastery_evidence_modes(0, True, "review"))

    def test_assisted_correct_answer_gains_less_than_independent(self):
        baseline = 40.0
        kwargs = {"current": baseline, "correct": True, "confidence": "sure", "response_ms": 2000}
        independent = adaptive_mastery_update(**kwargs, retry=False)
        assisted = adaptive_mastery_update(**kwargs, retry=True)
        self.assertLessEqual(assisted, independent)
        self.assertGreaterEqual(assisted, baseline)


if __name__ == "__main__":
    unittest.main()
