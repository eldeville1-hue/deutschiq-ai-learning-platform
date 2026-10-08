import asyncio
import unittest
from unittest.mock import patch

from tests.run_ai_benchmark_v88 import production_adapter
from tests.release_readiness_v88 import build_report


class RealAiAdapterTests(unittest.TestCase):
    def test_real_adapter_rejects_local_fallback(self):
        with patch("tests.run_ai_benchmark_v88._ai_feedback",
                   return_value={"source": "local", "correct": True}):
            with self.assertRaises(RuntimeError):
                asyncio.run(production_adapter("Hallo", {"question": "Greet"}))

    def test_real_adapter_accepts_ai_source(self):
        with patch("tests.run_ai_benchmark_v88._ai_feedback",
                   return_value={"source": "ai", "correct": True}):
            result = asyncio.run(production_adapter("Hallo", {"question": "Greet"}))
        self.assertEqual(result["source"], "ai")

    def test_ai_metrics_without_signoff_still_block_release(self):
        report = build_report(
            benchmark={"deterministic_latency_gate": True, "failure_rate": 0},
            linguistic={"release_checks": {}, "failed_gates": []},
            ai_benchmark={"measured": True, "p95_ms": 800, "failure_rate": 0, "sample_count": 100, "representative_release_sample": True, "real_ai_adapter": True},
        )
        self.assertTrue(report["checks"]["ai_assisted_performance"])
        self.assertEqual(report["release_gate"], "blocked")


if __name__ == "__main__":
    unittest.main()
