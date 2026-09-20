import unittest

from app.services.production_feedback import local_feedback
from app.services.misconception_feedback import misconception_feedback


class ProductionFeedbackTests(unittest.TestCase):
    def test_complete_target_sentence_passes(self):
        result = local_feedback(
            "Heute lerne ich Deutsch.",
            {"target_patterns": ["lerne"], "model_answer": "Heute lerne ich Deutsch."},
            "Das Verb steht auf Position zwei.",
        )
        self.assertTrue(result["correct"])
        self.assertGreaterEqual(result["score"], 70)

    def test_short_fragment_does_not_pass(self):
        result = local_feedback(
            "Ich lerne",
            {"target_patterns": ["lerne"], "model_answer": "Heute lerne ich Deutsch."},
            "Das Verb steht auf Position zwei.",
        )
        self.assertFalse(result["correct"])

    def test_misconception_feedback_is_specific_and_localized(self):
        self.assertIn("глагол", misconception_feedback("verb_not_final", "ru"))
        self.assertIn("Verb", misconception_feedback("verb_not_final", "de"))
        self.assertIn("verb", misconception_feedback("verb_not_final", "en"))
        self.assertNotEqual(
            misconception_feedback("verb_not_final", "en"),
            misconception_feedback("case_ending", "en"),
        )


if __name__ == "__main__":
    unittest.main()
