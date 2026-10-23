import unittest

from app.services.lesson_coaching import repair_plan


class RepairPlanAnswerPrivacyTests(unittest.TestCase):
    def test_missing_and_extra_words_are_not_given_away(self):
        for language in ("ru", "de", "en", "de-DE"):
            for missing, extra in ((["GEHEIMANTWORT"], []), ([], ["GEHEIMANTWORT"])):
                with self.subTest(language=language, missing=bool(missing)):
                    steps = repair_plan("answer_mismatch", missing, extra, language)
                    self.assertEqual(len(steps), 3)
                    self.assertNotIn("GEHEIMANTWORT", " ".join(steps))
                    self.assertTrue(all(step.strip() for step in steps))


if __name__ == "__main__":
    unittest.main()
