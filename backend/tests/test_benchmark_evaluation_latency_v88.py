import unittest
from tests.benchmark_evaluation_latency_v88 import measure


class LatencyBenchmarkTests(unittest.TestCase):
    def test_reports_real_failures_and_never_claims_release(self):
        rows = [{"learner_answer": "Hallo", "exercise": {"answer": "Hallo"}}]
        report = measure(rows, evaluator=lambda answer, exercise: {"correct": True})
        self.assertEqual(0, report["failures"])
        self.assertEqual("not_measured", report["ai_assisted_latency"])
        self.assertEqual("blocked", report["release_gate"])

    def test_exception_counts_as_failure(self):
        def broken(answer, exercise):
            raise ValueError("test failure")
        rows = [{"learner_answer": "Hallo", "exercise": {"answer": "Hallo"}}]
        report = measure(rows, evaluator=broken)
        self.assertEqual(1, report["failures"])
        self.assertEqual(1.0, report["failure_rate"])
        self.assertFalse(report["deterministic_latency_gate"])


if __name__ == "__main__":
    unittest.main()
