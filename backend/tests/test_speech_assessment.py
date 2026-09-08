import unittest

from app.services.speech_assessment import assess_speech_match, normalize_speech


class SpeechAssessmentTests(unittest.TestCase):
    def test_normalizes_german_spelling_and_punctuation(self):
        self.assertEqual(normalize_speech("Ich weiß es!"), "ich weiss es")

    def test_exact_match_is_clear(self):
        result = assess_speech_match("Ich lerne heute Deutsch", "Ich lerne heute Deutsch.")
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["label"], "clear_match")

    def test_missing_words_are_reported(self):
        result = assess_speech_match("Ich lerne", "Ich lerne heute Deutsch")
        self.assertIn("heute", result["missing_words"])


if __name__ == "__main__":
    unittest.main()
