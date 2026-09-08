import unittest
from app.services.content_quality import normalize_lesson_content, validate_lesson_content

class VoiceCurriculumTests(unittest.TestCase):
    def test_every_lesson_gets_a_repeat_step(self):
        content = normalize_lesson_content({"examples": ["Ich lerne Deutsch."], "exercises": []}, "word_order", "A1")
        repeat = [item for item in content["exercises"] if item["type"] == "repeat"]
        self.assertEqual(len(repeat), 1)
        self.assertEqual(repeat[0]["answer"], "Ich lerne Deutsch.")
        self.assertEqual(validate_lesson_content(content), [])

    def test_existing_repeat_step_is_not_duplicated(self):
        content = normalize_lesson_content({"examples": ["Hallo."], "exercises": [{"type": "repeat", "question": "Sprich", "answer": "Hallo.", "explanation": "Noch einmal"}]}, "greeting", "A1")
        self.assertEqual(sum(item["type"] == "repeat" for item in content["exercises"]), 1)

if __name__ == "__main__":
    unittest.main()
