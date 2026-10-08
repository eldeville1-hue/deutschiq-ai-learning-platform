import unittest
from tests.release_readiness_v88 import build_report


class DevelopmentCoverageTests(unittest.TestCase):
    def report(self, verified=95, count=100):
        profile = {"workload_source": "curated_development_unreviewed", "levels": {
            level: {"sample_count": count, "status_counts": {"verified": verified},
                    "failure_count": 0} for level in ("A1", "A2", "B1", "B2")
        }}
        return build_report(
            benchmark={"deterministic_latency_gate": True, "failure_rate": 0},
            linguistic={"release_checks": {}, "failed_gates": []},
            structured_profile=profile,
        )

    def test_coverage_target_is_not_release_approval(self):
        report = self.report()
        self.assertTrue(report["structured_development_coverage_all_levels"])
        self.assertEqual(report["release_gate"], "blocked")
        self.assertFalse(report["checks"]["independent_linguistic_review"])

    def test_insufficient_coverage_is_visible(self):
        report = self.report(verified=80)
        self.assertFalse(report["structured_development_coverage_all_levels"])
        self.assertEqual(report["structured_development_coverage"]["B2"]["definitive_coverage"], 0.8)

    def test_tiny_sample_cannot_meet_target(self):
        self.assertFalse(self.report(verified=1, count=1)["structured_development_coverage_all_levels"])

    def test_missing_profile_fails_closed(self):
        report = build_report(benchmark={"deterministic_latency_gate": True, "failure_rate": 0},
                              linguistic={"release_checks": {}, "failed_gates": []})
        self.assertFalse(report["structured_development_coverage_all_levels"])


if __name__ == "__main__":
    unittest.main()
