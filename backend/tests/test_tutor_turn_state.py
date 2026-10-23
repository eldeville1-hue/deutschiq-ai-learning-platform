import unittest
from app.services.tutor_turn_state import classify_tutor_turn, practice_turn_instruction


class TutorTurnStateTests(unittest.TestCase):
    def test_short_answer_after_exercise_is_attempt(self):
        self.assertEqual(classify_tutor_turn("Übung: Ordne die Wörter.", "Wegen des Regens bleiben wir zu Hause."), "attempt")

    def test_explicit_request_is_not_graded(self):
        self.assertEqual(classify_tutor_turn("Übung: Ordne die Wörter.", "Объясни Genitiv"), "new_request")

    def test_non_exercise_turn_is_conversation(self):
        self.assertEqual(classify_tutor_turn("Genitiv follows wegen in formal German.", "Danke!"), "conversation")

    def test_question_is_not_automatically_attempt(self):
        self.assertEqual(classify_tutor_turn("Exercise: put these words in order.", "Can you explain this?"), "new_request")

    def test_attempt_guidance_does_not_claim_mastery(self):
        guidance = practice_turn_instruction("attempt")
        self.assertIn("Assess the response", guidance)
        self.assertIn("Do not award XP", guidance)


if __name__ == "__main__":
    unittest.main()
