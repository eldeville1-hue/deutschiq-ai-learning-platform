import unittest
from tests.generate_evaluation_benchmark import build_cases
from tests.run_evaluation_benchmark import run

class EvaluationBenchmarkTests(unittest.TestCase):
    def test_fixture_size_and_level_balance(self):
        rows = build_cases()
        self.assertEqual(len(rows), 480)
        self.assertEqual(len({r["id"] for r in rows}), 480)
        for level in ("A1", "A2", "B1", "B2"):
            self.assertEqual(sum(r["cefr"] == level for r in rows), 120)

    def test_task_family_diversity_and_unverified_open_answers(self):
        rows = build_cases()
        for level in ("A1", "A2", "B1", "B2"):
            families = {r["task_family"] for r in rows if r["cefr"] == level}
            self.assertGreaterEqual(len(families), 6)
            self.assertTrue(any(
                r["provisional_expected"] == "uncertain"
                for r in rows if r["cefr"] == level
            ))
        self.assertTrue(all(r["human_review"]["status"] == "pending" for r in rows))

    def test_synthetic_labels_do_not_count_as_review(self):
        report = run(build_cases())
        self.assertEqual(report["reviewed"], 0)
        self.assertEqual(report["pending"], 480)
        self.assertEqual(report["source_distribution"]["synthetic_level_specific"], 480)
        self.assertEqual(report["review_status_distribution"]["pending"], 480)
        self.assertGreaterEqual(len(report["task_family_distribution"]), 6)
        self.assertEqual(report["release_gate"], "blocked")
        self.assertIsNone(report["levels"]["A1"]["accuracy"])

    def test_reviewed_metrics_are_separate(self):
        rows = build_cases()
        rows[0]["human_review"] = {"reviewed_at": "2026-10-08T12:00:00Z", "protocol_version": "v88-1", "blind_to_prediction": True, "independent_of_generation": True, "status": "approved", "reviewer": "test", "decision": "correct"}
        report = run(rows)
        self.assertEqual(report["reviewed"], 1)
        self.assertEqual(report["pending"], 479)

    def test_deferral_cannot_pass_accuracy_or_coverage(self):
        rows = build_cases()
        for row in rows:
            row["human_review"] = {"reviewed_at": "2026-10-08T12:00:00Z", "protocol_version": "v88-1", "blind_to_prediction": True, "independent_of_generation": True, "status": "approved", "reviewer": "independent", "decision": "correct", "error_types": []}
        def defer(answer, exercise):
            return {"evaluation_status": "uncertain", "correct": False, "errors": []}
        report = run(rows, evaluator=defer)
        self.assertEqual(report["levels"]["A1"]["coverage"], 0)
        self.assertIn("A1:coverage", report["failed_gates"])
        self.assertEqual(report["release_gate"], "blocked")

    def test_perfect_decisions_do_not_hide_missing_diagnoses(self):
        rows = build_cases()
        for row in rows:
            row["human_review"] = {"reviewed_at": "2026-10-08T12:00:00Z", "protocol_version": "v88-1", "blind_to_prediction": True, "independent_of_generation": True, "status": "approved", "reviewer": "independent", "decision": "incorrect", "error_types": ["article"]}
        def omit_errors(answer, exercise):
            return {"evaluation_status": "verified", "correct": False, "errors": []}
        report = run(rows, evaluator=omit_errors)
        self.assertEqual(report["levels"]["A1"]["accuracy"], 1.0)
        self.assertEqual(report["levels"]["A1"]["coverage"], 1.0)
        self.assertIn("A1:diagnosis_recall", report["failed_gates"])
        self.assertEqual(report["release_gate"], "blocked")

if __name__ == "__main__":
    unittest.main()
