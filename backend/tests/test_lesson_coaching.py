import unittest

from app.services.lesson_coaching import learning_profile, repair_plan, supported_retry_exercise


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


if __name__ == "__main__":
    unittest.main()
