import unittest
from tests.generate_evaluation_benchmark import build_cases
from tests.run_evaluation_benchmark import run


class EvaluationBenchmarkTests(unittest.TestCase):
    def test_fixture_size_and_level_balance(self):
        rows = build_cases()
        self.assertEqual(len(rows), 480)
        self.assertEqual(len({row["id"] for row in rows}), 480)
        for level in ("A1", "A2", "B1", "B2"):
            self.assertEqual(sum(row["cefr"] == level for row in rows), 120)

    def test_synthetic_labels_do_not_count_as_review(self):
        report = run(build_cases())
        self.assertEqual(report["reviewed"], 0)
        self.assertEqual(report["pending"], 480)
        self.assertEqual(report["release_gate"], "blocked")
        self.assertIsNone(report["levels"]["A1"]["accuracy"])

    def test_reviewed_metrics_are_separate(self):
        rows = build_cases()
        rows[0]["human_review"] = {"status": "approved", "reviewer": "test", "decision": "correct"}
        report = run(rows)
        self.assertEqual(report["reviewed"], 1)
        self.assertEqual(report["pending"], 479)
        self.assertEqual(report["release_gate"], "blocked")


if __name__ == "__main__":
    unittest.main()
