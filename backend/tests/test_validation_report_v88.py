import unittest
from tests.run_evaluation_benchmark import validation_report
from tests.generate_curated_evaluation_v88 import build_diverse_cases


class ValidationReportTests(unittest.TestCase):
    def test_unreviewed_curated_development_cannot_release(self):
        report = validation_report(build_diverse_cases())
        self.assertEqual(report["release_gate"], "blocked")
        self.assertEqual(report["holdout_total"], 0)
        self.assertIn("independent_holdout_missing", report["failed_gates"])
        for level in ("A1", "A2", "B1", "B2"):
            self.assertIn(f"{level}:independent_holdout_insufficient", report["failed_gates"])

    def test_claimed_review_in_development_split_is_not_holdout(self):
        rows = build_diverse_cases()[:1]
        rows[0]["human_review"] = {
            "status": "approved", "decision": "correct", "reviewer": "test",
            "reviewed_at": "2026-10-08", "protocol_version": "v88-1",
            "independent_of_generation": True, "blind_to_prediction": True,
        }
        report = validation_report(rows)
        self.assertEqual(report["holdout_total"], 0)
        self.assertFalse(report["release_checks"]["human_signoff"])
        self.assertEqual(report["release_gate"], "blocked")

    def test_holdout_without_approved_reviews_does_not_count(self):
        rows = build_diverse_cases()[:1]
        rows[0]["split"] = "holdout"
        report = validation_report(rows)
        self.assertEqual(report["holdout_total"], 1)
        self.assertIn("A1:independent_holdout_insufficient", report["failed_gates"])


if __name__ == "__main__":
    unittest.main()
