import json
import tempfile
import unittest
from pathlib import Path

from tests.profile_structured_evaluator_v88 import profile, save_report


class StructuredProfilerTests(unittest.TestCase):
    def test_reports_each_level_and_keeps_release_blocked(self):
        rows = [
            {"cefr": level, "learner_answer": "Hallo", "exercise": {"answer": "Hallo"}}
            for level in ("A1", "A2", "B1", "B2")
        ]
        report = profile(rows, evaluator=lambda answer, exercise: {
            "evaluation_status": "verified", "correct": True
        })
        self.assertEqual(report["release_gate"], "blocked")
        for level in ("A1", "A2", "B1", "B2"):
            self.assertEqual(report["levels"][level]["status_counts"]["verified"], 1)
            self.assertFalse(report["levels"][level]["deterministic_latency_gate"])

    def test_uncertainty_is_broken_down_by_family(self):
        rows = [{"id": "review-me", "cefr": "B1", "task_family": "translation",
                 "learner_answer": "x", "exercise": {"answer": "y"}}]
        report = profile(rows, evaluator=lambda a, e: {"evaluation_status": "uncertain"})
        level = report["levels"]["B1"]
        self.assertEqual(level["definitive_coverage"], 0.0)
        self.assertEqual(level["task_family_status_counts"]["translation"]["uncertain"], 1)
        self.assertEqual(level["uncertain_examples"][0]["id"], "review-me")

    def test_invalid_status_is_counted_as_failure(self):
        rows = [{"cefr": "A1", "learner_answer": "x", "exercise": {}}]
        report = profile(rows, evaluator=lambda a, e: {"evaluation_status": "made_up"})
        self.assertEqual(report["levels"]["A1"]["failure_count"], 1)

    def test_exceptions_are_counted(self):
        def broken(answer, exercise):
            raise RuntimeError("broken")
        rows = [{"cefr": "B2", "learner_answer": "x", "exercise": {}}]
        report = profile(rows, evaluator=broken)
        self.assertEqual(report["levels"]["B2"]["failure_count"], 1)

    def test_report_is_persisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "reports" / "profile.json")
            save_report({"release_gate": "blocked"}, path)
            self.assertEqual(json.loads(Path(path).read_text())["release_gate"], "blocked")


if __name__ == "__main__":
    unittest.main()
