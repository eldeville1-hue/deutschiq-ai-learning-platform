import unittest
from tests.linguistic_challenge_suite import audit, build_challenges

class LinguisticChallengeSuiteTests(unittest.TestCase):
    def test_balanced_levels_and_case_identity(self):
        rows = build_challenges()
        self.assertEqual(len(rows), 40)
        self.assertEqual(len({row["id"] for row in rows}), 40)
        for level in ("A1", "A2", "B1", "B2"):
            self.assertEqual(sum(row["cefr"] == level for row in rows), 10)
        self.assertTrue(all(row["human_review"]["status"] == "pending" for row in rows))

    def test_known_alternatives_are_explicitly_listed(self):
        rows = build_challenges()
        for index in (6, 17, 23):
            row = rows[index]
            self.assertIn(row["learner_answer"], row["exercise"]["accepted_answers"])

    def test_task_families_have_distinct_instructions(self):
        rows = build_challenges()
        by_family = {}
        for row in rows:
            by_family.setdefault(row["task_family"], row["exercise"]["question"])
        for family, question in by_family.items():
            self.assertTrue(question)
            self.assertNotIn("Express the target meaning in German:", question)
        self.assertNotEqual(by_family["translation"].split(". Reference:")[0],
                            by_family["error_repair"].split(". Reference:")[0])

    def test_audit_reports_disagreements_without_claiming_release_quality(self):
        report = audit()
        self.assertEqual(report["cases"], 40)
        self.assertFalse(report["release_evidence"])
        self.assertEqual(report["human_reviewed"], 0)
        self.assertEqual(sum(report["provisional_confusion"].values()), 40)
        self.assertIn("diagnosis_comparison", report)
        self.assertTrue(all("decision_disagreement" in item for item in report["disagreements"]))

    def test_audit_detects_false_acceptance(self):
        def always_accept(answer, exercise):
            return {"evaluation_status": "verified", "correct": True, "errors": []}
        report = audit(evaluator=always_accept)
        self.assertGreater(report["disagreement_count"], 0)
        self.assertTrue(any(x["provisional_expected"] == "incorrect"
                            for x in report["disagreements"]))

if __name__ == "__main__":
    unittest.main()
