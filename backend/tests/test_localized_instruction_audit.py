"""Regression tests for malformed localized exercise instructions."""
import unittest

from app.services.content_quality import exercise_instruction_audit


class LocalizedInstructionAuditTests(unittest.TestCase):
    def test_malformed_language_payload_is_reported(self):
        content = {"exercises": [{
            "type": "choose", "question": "Wähle.", "explanation": "Begründung.",
            "i18n": {"ru": "not a translation object", "de": None, "en": {"question": ""}},
        }]}
        self.assertEqual(
            exercise_instruction_audit(content),
            [
                "exercise:0:invalid_ru_i18n",
                "exercise:0:invalid_de_i18n",
                "exercise:0:empty_en_question",
            ],
        )

    def test_malformed_i18n_container_is_reported(self):
        content = {"exercises": [{
            "question": "Wähle.", "explanation": "Begründung.", "i18n": [],
        }]}
        self.assertEqual(exercise_instruction_audit(content), ["exercise:0:invalid_i18n"])

    def test_legacy_exercise_without_localization_remains_valid(self):
        content = {"exercises": [{"question": "Wähle.", "explanation": "Begründung."}]}
        self.assertEqual(exercise_instruction_audit(content), [])


if __name__ == "__main__":
    unittest.main()
