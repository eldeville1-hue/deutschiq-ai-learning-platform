import unittest

from tests.release_readiness_v88 import build_report


class StructuredProfileEvidenceIntegrityV88Tests(unittest.TestCase):
    def report_for(self, statuses, count=100, failures=0):
        profile = {"workload_source": "curated_development_unreviewed", "levels": {
            level: {"sample_count": count, "status_counts": dict(statuses), "failure_count": failures}
            for level in ("A1", "A2", "B1", "B2")
        }}
        return build_report(
            benchmark={"deterministic_latency_gate": False, "failure_rate": 1},
            linguistic={"failed_gates": [], "release_checks": {}},
            structured_profile=profile,
        )

    def test_consistent_95_percent_coverage_is_reported_as_development_only(self):
        report = self.report_for({"verified": 95, "uncertain": 5, "needs_review": 0})
        self.assertTrue(report["structured_development_coverage_all_levels"])
        self.assertEqual(report["release_gate"], "blocked")

    def test_missing_status_rows_cannot_claim_coverage(self):
        report = self.report_for({"verified": 95, "uncertain": 0, "needs_review": 0})
        self.assertFalse(report["structured_development_coverage_all_levels"])
        self.assertIsNone(report["structured_development_coverage"]["A1"]["definitive_coverage"])

    def test_negative_or_boolean_status_counts_are_invalid(self):
        for statuses in (
            {"verified": 100, "uncertain": -1, "needs_review": 1},
            {"verified": 100, "uncertain": False, "needs_review": 0},
        ):
            with self.subTest(statuses=statuses):
                report = self.report_for(statuses)
                self.assertFalse(report["structured_development_coverage_all_levels"])

    def test_failed_evaluations_cannot_claim_full_coverage(self):
        report = self.report_for({"verified": 100, "uncertain": 0, "needs_review": 0}, failures=1)
        self.assertFalse(report["structured_development_coverage_all_levels"])


if __name__ == "__main__":
    unittest.main()
