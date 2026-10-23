import unittest
from collections import Counter
from app.services.tutor_exercise_bank import DRILLS
from app.services.tutor_verified_practice import grade_reviewed_word_order
from app.services.tutor_fallback import fallback_answer


class TutorExerciseBankTests(unittest.TestCase):
    def test_six_drills_per_level(self):
        self.assertEqual(Counter(row[1] for row in DRILLS), {"A1": 6, "A2": 6, "B1": 6, "B2": 6})
        self.assertEqual(len({row[0] for row in DRILLS}), len(DRILLS))
        self.assertEqual(len({row[4] for row in DRILLS}), len(DRILLS))

    def test_all_authored_answers_are_verified(self):
        for identifier, level, topic, expected, words, alternatives in DRILLS:
            for answer in (expected, *alternatives):
                with self.subTest(identifier=identifier, answer=answer):
                    result = grade_reviewed_word_order("Exercise: " + words, answer)
                    self.assertIsNotNone(result)
                    self.assertIs(result["correct"], True)
                    self.assertEqual(result["topic"], topic)

    def test_unreviewed_variants_are_not_automatically_marked_wrong(self):
        result = grade_reviewed_word_order(
            "Exercise: morgen / ich / Deutsch / lerne", "Deutsch lerne ich morgen."
        )
        self.assertIsNone(result["correct"])

    def test_level_specific_offline_practice(self):
        for level in ("A1", "A2", "B1", "B2"):
            answer = fallback_answer("Give me an exercise", "en", level, ["word_order"])
            self.assertIn(level + " practice", answer)
            self.assertTrue(any(row[4] in answer for row in DRILLS if row[1] == level))

    def test_offline_rotation_avoids_immediate_repeat(self):
        first = fallback_answer("Give me an exercise", "en", "A1", ["word_order"])
        second = fallback_answer("Give me an exercise", "en", "A1", ["word_order"], [first])
        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
