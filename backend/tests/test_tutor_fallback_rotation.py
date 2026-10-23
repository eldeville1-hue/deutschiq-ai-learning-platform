import unittest
from app.services.tutor_fallback import fallback_answer


class TutorFallbackRotationTests(unittest.TestCase):
    def test_generic_practice_avoids_recently_used_drill(self):
        first = fallback_answer("Give me an exercise", "en", "B1", ["genitive_prepositions"])
        second = fallback_answer("Give me an exercise", "en", "B1", ["genitive_prepositions"], [first])
        self.assertIn("wegen / des Regens", first)
        self.assertNotIn("wegen / des Regens", second)
        self.assertIn("Put these words in order", second)

    def test_explicit_topic_still_wins(self):
        first = fallback_answer("Give me a genitive exercise", "en", "B1", ["genitive_prepositions"])
        second = fallback_answer("Give me a genitive exercise", "en", "B1", ["genitive_prepositions"], [first])
        self.assertIn("wegen / des Regens", second)


if __name__ == "__main__":
    unittest.main()
