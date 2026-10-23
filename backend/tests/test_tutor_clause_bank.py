import unittest
from collections import Counter
from app.services.tutor_clause_bank import CLAUSE_DRILLS
from app.services.tutor_verified_practice import grade_reviewed_word_order
from app.services.tutor_fallback import fallback_answer


class ClauseDrillTests(unittest.TestCase):
    def test_six_per_level_and_unique_prompts(self):
        self.assertEqual(Counter(row[1] for row in CLAUSE_DRILLS), {"B1": 6, "B2": 6})
        self.assertEqual(len({row[4] for row in CLAUSE_DRILLS}), 12)

    def test_all_reviewed_answers(self):
        for identifier, level, topic, expected, chunks, variants in CLAUSE_DRILLS:
            for answer in (expected, *variants):
                with self.subTest(identifier=identifier, answer=answer):
                    result = grade_reviewed_word_order("Exercise: " + chunks, answer)
                    self.assertIs(result["correct"], True)
                    self.assertEqual(result["topic"], topic)

    def test_unknown_answer_is_unverified(self):
        result = grade_reviewed_word_order(
            "Exercise: obwohl ich müde bin / lerne ich weiter",
            "Ich lerne trotzdem weiter.",
        )
        self.assertIsNone(result["correct"])

    def test_b1_and_b2_practice_use_clause_prompts(self):
        for level in ("B1", "B2"):
            response = fallback_answer("Give me a subordinate clause exercise", "en", level, ["word_order"])
            self.assertTrue(any(row[4] in response for row in CLAUSE_DRILLS if row[1] == level))

    def test_next_prompt_changes(self):
        first = fallback_answer("Give me a subordinate clause exercise", "en", "B1", ["word_order"])
        second = fallback_answer("Give me a subordinate clause exercise", "en", "B1", ["word_order"], [first])
        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
