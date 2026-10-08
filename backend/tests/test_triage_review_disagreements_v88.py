import unittest

from tests.triage_review_disagreements_v88 import triage


def row(identifier, decision, answer, model="Hallo"):
    return {"id": identifier, "cefr": "A1",
            "learner_answer": answer,
            "exercise": {"type": "translation", "answer": model},
            "human_review": {"status": "pending_independence_verification",
                             "reviewer": "reviewer-1", "decision": decision,
                             "error_types": ["meaning"] if decision == "incorrect" else []}}


class ReviewDisagreementTriageTests(unittest.TestCase):
    def test_prioritizes_potential_false_acceptance(self):
        report = triage([row("uncertain", "correct", "Servus"),
                         row("false_accept", "incorrect", "Hallo")])
        self.assertEqual([x["kind"] for x in report["findings"]],
                         ["potential_false_acceptance", "correct_answer_unverified"])
        self.assertFalse(report["review_independence_verified"])
        self.assertEqual(report["release_gate"], "blocked")

    def test_correct_reference_has_no_disagreement(self):
        report = triage([row("exact", "correct", "Hallo")])
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["reviewed_count_by_level"]["A1"], 1)

    def test_unreviewed_rows_are_not_counted(self):
        item = row("pending", "correct", "Hallo")
        item["human_review"]["status"] = "pending"
        report = triage([item])
        self.assertEqual(report["reviewed_count_by_level"]["A1"], 0)

    def test_duplicate_ids_fail_closed(self):
        item = row("same", "correct", "Hallo")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            triage([item, item])

    def test_missing_reviewer_is_rejected(self):
        item = row("bad", "correct", "Hallo")
        item["human_review"]["reviewer"] = ""
        with self.assertRaisesRegex(ValueError, "Invalid pending"):
            triage([item])


if __name__ == "__main__":
    unittest.main()
