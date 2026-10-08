import unittest
from tests.release_readiness_v88 import build_report


class AiEvidenceProvenanceTests(unittest.TestCase):
    def report(self, ai):
        return build_report(
            benchmark={"deterministic_latency_gate": True, "failure_rate": 0},
            linguistic={"release_checks": {}, "failed_gates": []},
            ai_benchmark=ai,
        )

    def test_two_case_smoke_benchmark_cannot_approve(self):
        ai = {"measured": True, "real_ai_adapter": True,
              "representative_release_sample": False, "sample_count": 2,
              "p95_ms": 500, "failure_rate": 0}
        self.assertFalse(self.report(ai)["checks"]["ai_assisted_performance"])

    def test_missing_real_adapter_provenance_blocks(self):
        ai = {"measured": True, "representative_release_sample": True,
              "sample_count": 100, "p95_ms": 500, "failure_rate": 0}
        self.assertFalse(self.report(ai)["checks"]["ai_assisted_performance"])

    def test_qualifying_metrics_do_not_override_human_signoff(self):
        ai = {"measured": True, "real_ai_adapter": True,
              "representative_release_sample": True, "sample_count": 100,
              "p95_ms": 500, "failure_rate": 0}
        report = self.report(ai)
        self.assertTrue(report["checks"]["ai_assisted_performance"])
        self.assertEqual(report["release_gate"], "blocked")


if __name__ == "__main__":
    unittest.main()
