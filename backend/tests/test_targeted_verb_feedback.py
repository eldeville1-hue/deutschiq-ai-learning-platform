import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class TargetedVerbFeedbackTests(unittest.TestCase):
    def test_perfekt_auxiliary_feedback(self):
        result = evaluate_structured_answer("Ich bin gelernt.", {
            "type": "fill", "answer": "Ich habe gelernt.", "target_feature": "tense",
        })
        self.assertFalse(result["correct"])
        self.assertEqual("auxiliary", result["errors"][0]["type"])
        self.assertIn("haben or sein", result["errors"][0]["explanation"])
        self.assertIn("'habe' instead of 'bin'", result["errors"][0]["explanation"])

    def test_subject_verb_agreement_feedback(self):
        result = evaluate_structured_answer("Du lernt Deutsch.", {
            "type": "fill", "answer": "Du lernst Deutsch.", "target_feature": "conjugation",
        })
        self.assertFalse(result["correct"])
        self.assertEqual("conjugation", result["errors"][0]["type"])
        self.assertIn("'lernst' instead of 'lernt'", result["errors"][0]["explanation"])

    def test_correct_auxiliary_still_passes(self):
        result = evaluate_structured_answer("ich habe gelernt!", {
            "type": "fill", "answer": "Ich habe gelernt.", "target_feature": "tense",
        })
        self.assertTrue(result["correct"])


if __name__ == "__main__":
    unittest.main()
