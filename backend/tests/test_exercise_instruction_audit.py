import unittest

from app.services.content_quality import exercise_instruction_audit


class ExerciseInstructionAuditTests(unittest.TestCase):
    def test_flags_missing_question_and_explanation(self):
        content = {"exercises": [{"type": "fill", "question": " ", "answer": "bin"}]}
        self.assertEqual(
            ["exercise:0:missing_question", "exercise:0:missing_explanation"],
            exercise_instruction_audit(content),
        )

    def test_listening_requires_source_or_lesson_audio(self):
        exercise = {"type": "listening_choice", "question": "Listen and choose",
                    "explanation": "Listen for the verb."}
        self.assertIn("exercise:0:missing_listening_source",
                      exercise_instruction_audit({"exercises": [exercise]}))
        self.assertEqual([], exercise_instruction_audit(
            {"audio_text": "Ich gehe nach Hause.", "exercises": [exercise]}))

    def test_valid_exercise_has_no_instruction_issues(self):
        content = {"exercises": [{"type": "fill", "question": "Complete the sentence",
                                   "explanation": "Use the correct verb form."}]}
        self.assertEqual([], exercise_instruction_audit(content))


if __name__ == "__main__":
    unittest.main()
