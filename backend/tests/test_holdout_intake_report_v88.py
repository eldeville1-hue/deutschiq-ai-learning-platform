import unittest

from tests.holdout_intake_report_v88 import summarize


class HoldoutIntakeReportV88Tests(unittest.TestCase):
    def test_empty_collection_remains_blocked(self):
        report = summarize([], validator=lambda rows: [])
        self.assertEqual(report["levels"]["A1"]["remaining"], 100)
        self.assertFalse(report["collection_target_met"])
        self.assertEqual(report["release_gate"], "blocked")

    def test_four_level_collection_does_not_approve_release(self):
        rows = [
            {"cefr": level, "human_review": {"status": "pending"}}
            for level in ("A1", "A2", "B1", "B2") for _ in range(100)
        ]
        report = summarize(rows, validator=lambda rows: [])
        self.assertTrue(report["collection_target_met"])
        self.assertEqual(report["review_status_counts"]["pending"], 400)
        self.assertFalse(report["independence_externally_verified"])
        self.assertEqual(report["release_gate"], "blocked")

    def test_review_workload_by_level_and_stage(self):
        rows = [
            {"cefr": "B1", "human_review": {"status": "pending"}},
            {"cefr": "B1", "human_review": {"status": "pending_independence_verification"}},
            {"cefr": "B1", "human_review": {"status": "approved"}},
            {"cefr": "A2", "human_review": {"status": "unknown"}},
        ]
        report = summarize(rows, validator=lambda rows: [])
        self.assertEqual(report["levels"]["B1"]["awaiting_linguistic_review"], 1)
        self.assertEqual(report["levels"]["B1"]["awaiting_independence_verification"], 1)
        self.assertEqual(report["levels"]["B1"]["claimed_approved"], 1)
        self.assertEqual(report["levels"]["A2"]["invalid_or_missing_review"], 1)
        self.assertEqual(report["release_gate"], "blocked")

    def test_coordinator_queue_does_not_treat_claimed_approvals_as_verified(self):
        rows = [
            {"cefr": "A1", "human_review": {"status": "pending"}},
            {"cefr": "A1", "human_review": {"status": "pending_independence_verification"}},
            {"cefr": "A1", "human_review": {"status": "approved"}},
        ]
        report = summarize(rows, validator=lambda rows: [])
        actions = {(item["cefr"], item["action"]): item["count"]
                   for item in report["coordinator_actions"]}
        self.assertEqual(actions[("A1", "collect_external_cases")], 97)
        self.assertEqual(actions[("A1", "request_blind_linguistic_review")], 1)
        self.assertEqual(actions[("A1", "verify_reviewer_independence_externally")], 1)
        self.assertFalse(report["independence_externally_verified"])
        self.assertEqual(report["release_gate"], "blocked")

    def test_ingestion_errors_are_visible(self):
        report = summarize([{"cefr": "A1", "human_review": {"status": "pending"}}],
                           validator=lambda rows: ["case-1:duplicate_content"])
        self.assertEqual(report["ingestion_error_count"], 1)
        self.assertFalse(report["intake_structurally_valid"])


if __name__ == "__main__":
    unittest.main()
