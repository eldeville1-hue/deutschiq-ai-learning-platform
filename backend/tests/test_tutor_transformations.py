import unittest
from app.services.tutor_transformation_bank import TRANSFORMATIONS
from app.services.tutor_verified_practice import grade_reviewed_word_order
from app.services.tutor_fallback import fallback_answer


class TransformationTests(unittest.TestCase):
    def test_unique_sources(self):
        self.assertEqual(len(TRANSFORMATIONS), 6)
        self.assertEqual(len({row[4] for row in TRANSFORMATIONS}), 6)

    def test_reviewed_answers(self):
        for identifier, level, topic, instruction, source, target, alternatives in TRANSFORMATIONS:
            for answer in (target, *alternatives):
                with self.subTest(identifier=identifier, answer=answer):
                    result = grade_reviewed_word_order("Exercise: " + instruction + " " + source, answer)
                    self.assertIs(result["correct"], True)
                    self.assertEqual(result["topic"], topic)

    def test_unreviewed_rephrasing_is_not_marked_wrong(self):
        result = grade_reviewed_word_order(
            "Exercise: Verbinde mit obwohl. Es regnet. Wir gehen spazieren.",
            "Wir gehen trotz des Regens spazieren.",
        )
        self.assertIsNone(result["correct"])

    def test_explicit_b2_transformation_prompt(self):
        for lang in ("ru", "de", "en"):
            response = fallback_answer("B2 transformation exercise", lang, "B2", ["word_order"])
            self.assertIn(TRANSFORMATIONS[0][4], response)

    def test_rotation(self):
        first = fallback_answer("B2 transformation exercise", "en", "B2", [])
        second = fallback_answer("B2 transformation exercise", "en", "B2", [], [first])
        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
