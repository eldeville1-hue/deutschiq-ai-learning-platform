import unittest

from app.services.lesson_coaching import learning_profile, repair_plan


class LessonCoachingTests(unittest.TestCase):
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
