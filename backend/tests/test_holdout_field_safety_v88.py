import unittest

from tests.holdout_pipeline_v88 import check_holdout


def case():
    return {
        "id": "external-B1-invalid-field", "cefr": "B1",
        "objective": "External grammar task",
        "exercise": {"type": "translation", "answer": "Ich habe heute viel gelernt."},
        "learner_answer": "Ich habe heute gelernt.",
        "source": "external_teacher_casebook", "split": "holdout",
        "human_review": {"status": "pending"},
    }


class HoldoutFieldSafetyV88Tests(unittest.TestCase):
    def test_invalid_id_fails_closed(self):
        row = case()
        row["id"] = None
        self.assertIn("row-0:invalid_id", check_holdout([row], development=[]))

    def test_invalid_objective_fails_closed(self):
        row = case()
        row["objective"] = {"text": "invalid"}
        self.assertIn("external-B1-invalid-field:invalid_objective", check_holdout([row], development=[]))

    def test_invalid_learner_answer_fails_closed(self):
        row = case()
        row["learner_answer"] = ["invalid"]
        self.assertIn("external-B1-invalid-field:invalid_learner_answer", check_holdout([row], development=[]))

    def test_invalid_reference_answer_fails_closed(self):
        row = case()
        row["exercise"]["answer"] = 42
        self.assertIn("external-B1-invalid-field:invalid_exercise", check_holdout([row], development=[]))


if __name__ == "__main__":
    unittest.main()
