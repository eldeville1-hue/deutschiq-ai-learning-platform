import unittest

from app.services.lesson_coaching import feedback_focus, learning_profile, repair_plan, success_feedback, supported_retry_exercise


class LessonCoachingTests(unittest.TestCase):
    def test_supported_retry_uses_a_fresh_sentence_and_localized_phone_prompt(self):
        exercise = {"id": "obwohl-guided", "answer": "Obwohl es regnet, gehen wir spazieren.", "accepted_answers": ["Obwohl es regnet, gehen wir spazieren."], "misconception": "verb_not_final"}
        content = {"examples": ["Obwohl es regnet, gehen wir spazieren.", "Obwohl ich müde bin, gehe ich zum Kurs."]}
        retry = supported_retry_exercise(exercise, content, "de")
        self.assertEqual("reorder", retry["type"])
        self.assertEqual("Obwohl ich müde bin, gehe ich zum Kurs", retry["answer"])
        self.assertNotEqual(retry["tokens"], retry["answer"].split())
        self.assertIn("neuen Beispiel", retry["question"])
    def test_struggling_learner_gets_supported_mode(self):
        profile = learning_profile(60, [True, False, False], 0)
        self.assertEqual("supported", profile["mode"])
        self.assertTrue(profile["show_guided_hint"])

    def test_mastered_learner_gets_challenge_mode(self):
        profile = learning_profile(82, [True, True, True], 3)
        self.assertEqual("challenge", profile["mode"])
        self.assertFalse(profile["show_guided_hint"])

    def test_repair_plan_uses_actual_missing_words_and_language(self):
        steps = repair_plan("missing_words", ["habe", "gearbeitet"], [], "de")
        self.assertEqual(3, len(steps))
        self.assertIn("habe", steps[1])
        self.assertIn("Wortstellung", steps[2])

    def test_feedback_focus_names_the_smallest_action_without_revealing_model(self):
        self.assertEqual("Ergänze: habe, gearbeitet.", feedback_focus("missing_words", ["habe", "gearbeitet"], [], "de"))
        self.assertEqual("Remove or replace: is.", feedback_focus("answer_mismatch", [], ["is"], "en"))
        self.assertIn("порядок", feedback_focus("answer_mismatch", [], [], "ru"))

    def test_success_feedback_has_localized_fallback(self):
        self.assertEqual("Die Verbform ist richtig.", success_feedback(" Die Verbform ist richtig. ", "de"))
        self.assertIn("situation", success_feedback("", "en").lower())


if __name__ == "__main__":
    unittest.main()
