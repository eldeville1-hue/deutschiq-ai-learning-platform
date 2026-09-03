import unittest
from app.services.content_quality import normalize_lesson_content, validate_lesson_content


class ContentQualityTests(unittest.TestCase):
    def test_normalizer_supplies_learning_sequence(self):
        content = normalize_lesson_content({"rule":"x", "examples":["Ich lerne."]}, "word_order", "A2")
        self.assertEqual(content["audio_text"], "Ich lerne.")
        self.assertIn("objective", content)

    def test_validator_rejects_uncheckable_exercise(self):
        content = normalize_lesson_content({"rule":"x", "examples":["x"], "exercises":[{"type":"fill", "question":"q"}]}, "x", "A1")
        errors = validate_lesson_content(content)
        self.assertIn("exercise:0:missing_answer", errors)

    def test_legacy_listening_lesson_is_migrated(self):
        content = normalize_lesson_content(
            {
                "examples": ["Danke, gut!"],
                "common_mistakes": [],
                "exercises": [
                    {"type": "listen", "question": "Was hörst du?", "answer": "Danke, gut!"}
                ],
            },
            "Аудирование: приветствие",
            "A1",
        )
        self.assertEqual(content["exercises"][0]["type"], "listening")
        self.assertTrue(content["common_mistakes"])
        self.assertEqual([], validate_lesson_content(content))


if __name__ == "__main__":
    unittest.main()
