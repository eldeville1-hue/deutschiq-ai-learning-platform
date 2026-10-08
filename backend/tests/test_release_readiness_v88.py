import unittest
from tests.release_readiness_v88 import build_report, ci_evidence_check


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

    def test_ci_evidence_must_match_sha_and_complete_successfully(self):
        expected = "a" * 40
        evidence = {"head_sha": expected, "status": "completed",
                    "conclusion": "success", "run_id": 123}
        self.assertTrue(ci_evidence_check(evidence, expected))
        self.assertFalse(ci_evidence_check(evidence, "b" * 40))
        self.assertFalse(ci_evidence_check(dict(evidence, conclusion="failure"), expected))
        self.assertFalse(ci_evidence_check(None, expected))

    def test_failed_benchmark_is_not_approved(self):
        report = build_report(
            benchmark={"deterministic_latency_gate": False, "failure_rate": 0.03},
            linguistic={"release_checks": {}, "failed_gates": []},
        )
        self.assertFalse(report["checks"]["deterministic_performance"])
        self.assertIn("deterministic_performance", report["failed_gates"])


if __name__ == "__main__":
    unittest.main()
