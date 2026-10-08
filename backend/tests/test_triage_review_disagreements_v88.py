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

    def test_verified_incorrect_diagnosis_disagreement_is_reported(self):
        item = row("diagnosis", "incorrect", "Ich gehen", model="Ich gehe")
        def evaluator(answer, exercise):
            return {"evaluation_status": "verified", "correct": False,
                    "errors": [{"type": "conjugation", "span": "gehen"}]}
        report = triage([item], evaluator=evaluator)
        self.assertEqual(report["findings"][0]["kind"], "potential_diagnosis_mismatch")
        self.assertEqual(report["findings"][0]["evaluator_error_types"], ["conjugation"])
        self.assertEqual(report["release_gate"], "blocked")

    def test_missing_evaluator_diagnosis_is_reported(self):
        item = row("no_diagnosis", "incorrect", "Ich gehen", model="Ich gehe")
        def evaluator(answer, exercise):
            return {"evaluation_status": "verified", "correct": False, "errors": []}
        report = triage([item], evaluator=evaluator)
        self.assertEqual(report["findings"][0]["kind"], "missing_evaluator_diagnosis")
        self.assertEqual(report["findings"][0]["evaluator_error_types"], [])
        self.assertEqual(report["release_gate"], "blocked")

    def test_matching_diagnosis_is_not_reported(self):
        item = row("matching", "incorrect", "Ich gehen", model="Ich gehe")
        def evaluator(answer, exercise):
            return {"evaluation_status": "verified", "correct": False,
                    "errors": [{"type": "meaning"}]}
        self.assertEqual(triage([item], evaluator=evaluator)["findings"], [])

    def test_forged_approval_is_rejected(self):
        item = row("forged", "correct", "Hallo")
        item["human_review"]["status"] = "approved"
        with self.assertRaisesRegex(ValueError, "Unexpected reviewer approval"):
            triage([item])

    def test_incorrect_review_without_diagnosis_is_rejected(self):
        item = row("no-diagnosis", "incorrect", "Hallo")
        item["human_review"]["error_types"] = []
        with self.assertRaisesRegex(ValueError, "lacks diagnosis"):
            triage([item])

    def test_correct_review_with_diagnosis_is_rejected(self):
        item = row("contradiction", "correct", "Hallo")
        item["human_review"]["error_types"] = ["meaning"]
        with self.assertRaisesRegex(ValueError, "includes error diagnoses"):
            triage([item])

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
