import unittest

from tests.holdout_pipeline_v88 import check_holdout


def approved_case(decision="incorrect", diagnoses=None):
    return {
        "id": "external-B2-diagnosis-001",
        "cefr": "B2",
        "objective": "Evaluate subordinate clause structure",
        "exercise": {"type": "translation", "answer": "Obwohl es regnete, gingen wir spazieren."},
        "learner_answer": "Obwohl es regnete, wir gingen spazieren.",
        "source": "external_teacher_casebook",
        "split": "holdout",
        "human_review": {
            "status": "approved", "reviewer": "External reviewer",
            "reviewed_at": "2026-10-08T14:00:00+02:00",
            "protocol_version": "v88", "blind_to_prediction": True,
            "independent_of_generation": True, "decision": decision,
            "error_types": ["word_order"] if diagnoses is None else diagnoses,
        },
    }


class HoldoutDiagnosisSafetyV88Tests(unittest.TestCase):
    def test_invalid_error_type_containers_are_rejected(self):
        for diagnoses in ("word_order", [None], [""], [42], {"type": "word_order"}):
            with self.subTest(diagnoses=diagnoses):
                errors = check_holdout([approved_case(diagnoses=diagnoses)], development=[])
                self.assertIn("external-B2-diagnosis-001:invalid_error_diagnoses", errors)

    def test_correct_decision_cannot_include_errors(self):
        errors = check_holdout([approved_case(decision="correct", diagnoses=["word_order"])], development=[])
        self.assertIn("external-B2-diagnosis-001:contradictory_error_diagnoses", errors)

    def test_valid_incorrect_diagnosis_is_accepted_structurally(self):
        errors = check_holdout([approved_case()], development=[])
        self.assertNotIn("external-B2-diagnosis-001:invalid_error_diagnoses", errors)


if __name__ == "__main__":
    unittest.main()
