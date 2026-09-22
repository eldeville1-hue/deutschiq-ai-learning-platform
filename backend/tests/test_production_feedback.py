import unittest

from app.services.production_feedback import local_feedback
from app.services.misconception_feedback import misconception_feedback
from app.services.answer_intelligence import evaluate_structured_answer, normalize_text


class ProductionFeedbackTests(unittest.TestCase):
    def test_structured_answers_ignore_punctuation_and_accept_minor_spelling(self):
        exercise = {"answer": "Ich habe gestern gearbeitet.", "accepted_answers": ["Ich habe gestern gearbeitet."]}
        self.assertTrue(evaluate_structured_answer("ich habe gestern gearbeitet!", exercise)["correct"])
        self.assertTrue(evaluate_structured_answer("Ich habe gestern gearbeitt.", exercise)["correct"])
        self.assertFalse(evaluate_structured_answer("Gestern ich habe gearbeitet.", exercise)["correct"])
        self.assertEqual("strasse", normalize_text("Straße"))

    def test_structured_feedback_reports_missing_words(self):
        result = evaluate_structured_answer("Ich gestern gearbeitet", {"answer": "Ich habe gestern gearbeitet"})
        self.assertFalse(result["correct"])
        self.assertIn("habe", result["missing_words"])
    def test_complete_target_sentence_passes(self):
        result = local_feedback(
            "Heute lerne ich Deutsch.",
            {"target_patterns": ["lerne"], "model_answer": "Heute lerne ich Deutsch."},
            "Das Verb steht auf Position zwei.",
        )
        self.assertTrue(result["correct"])
        self.assertGreaterEqual(result["score"], 70)
        self.assertEqual(
            {"task_completion", "grammar", "vocabulary", "coherence", "register"},
            set(result["dimension_scores"]),
        )

    def test_independent_wording_can_pass_without_model_match(self):
        result = local_feedback(
            "Obwohl es heute stark regnet, fahre ich trotzdem mit dem Fahrrad zur Arbeit.",
            {"target_patterns": ["obwohl"], "model_answer": "Obwohl es regnet, gehe ich spazieren."},
            "Im obwohl-Satz steht das Verb am Ende.", "de", "B1",
        )
        self.assertTrue(result["correct"])
        self.assertEqual(result["corrected_answer"], "Obwohl es heute stark regnet, fahre ich trotzdem mit dem Fahrrad zur Arbeit.")

    def test_same_short_answer_is_judged_more_strictly_at_b2(self):
        exercise = {"target_patterns": ["weil"], "model_answer": "Ich stimme zu, weil der Vorschlag sinnvoll ist."}
        self.assertTrue(local_feedback("Ich stimme zu, weil der Vorschlag sinnvoll ist.", exercise, "x", "de", "A2")["correct"])
        self.assertFalse(local_feedback("Ich stimme zu, weil der Vorschlag sinnvoll ist.", exercise, "x", "de", "B2")["correct"])

    def test_off_topic_english_answer_does_not_pass(self):
        result = local_feedback("This is a long but unrelated English answer for the task.", {"target_patterns": ["obwohl"], "model_answer": "Obwohl es regnet, gehe ich."}, "x", "en", "B1")
        self.assertFalse(result["correct"])
        self.assertEqual("off_topic", result["error_type"])

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
