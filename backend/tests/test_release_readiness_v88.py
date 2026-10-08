import unittest
from tests.release_readiness_v88 import build_report


class ReleaseReadinessTests(unittest.TestCase):
    def test_missing_review_and_ci_block_release(self):
        report = build_report(
            benchmark={"deterministic_latency_gate": True, "failure_rate": 0.0},
            linguistic={"release_checks": {}, "failed_gates": []},
        )
        self.assertEqual(report["release_gate"], "blocked")
        self.assertTrue(report["checks"]["deterministic_performance"])
        self.assertFalse(report["checks"]["independent_linguistic_review"])
        self.assertFalse(report["checks"]["xp_safety_ci_signoff"])
        self.assertIn("external_human_signoff", report["failed_gates"])

    def test_failed_benchmark_is_not_approved(self):
        report = build_report(
            benchmark={"deterministic_latency_gate": False, "failure_rate": 0.03},
            linguistic={"release_checks": {}, "failed_gates": []},
        )
        self.assertFalse(report["checks"]["deterministic_performance"])
        self.assertIn("deterministic_performance", report["failed_gates"])


if __name__ == "__main__":
    unittest.main()
