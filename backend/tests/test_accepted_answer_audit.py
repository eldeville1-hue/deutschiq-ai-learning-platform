import unittest

from app.services.content_quality import accepted_answer_issues


class AcceptedAnswerAuditTests(unittest.TestCase):
    def test_valid_alternative_formulations(self):
        exercise = {"answer": "Ich lerne Deutsch.", "accepted_answers": [
            "Ich lerne Deutsch.", "Deutsch lerne ich."
        ]}
        self.assertEqual([], accepted_answer_issues(exercise))

    def test_punctuation_and_spacing_duplicates(self):
        exercise = {"answer": "Ich lerne Deutsch.", "accepted_answers": [
            "Ich lerne Deutsch.", " ich   lerne deutsch! "
        ]}
        self.assertIn("duplicate_accepted_answers", accepted_answer_issues(exercise))

    def test_model_must_be_in_authored_answer_bank(self):
        exercise = {"answer": "Ich habe gelernt.", "accepted_answers": ["Ich bin gelernt."]}
        self.assertIn("model_answer_not_accepted", accepted_answer_issues(exercise))

    def test_invalid_answer_bank(self):
        for answers in ([], [" "], ["OK", None], "OK"):
            with self.subTest(answers=answers):
                self.assertIn("invalid_accepted_answers", accepted_answer_issues({"accepted_answers": answers}))

    def test_grammatical_form_is_not_silently_normalized(self):
        exercise = {"answer": "Ich sehe den Mann.", "accepted_answers": [
            "Ich sehe den Mann.", "Ich sehe dem Mann."
        ]}
        self.assertEqual([], accepted_answer_issues(exercise))


if __name__ == "__main__":
    unittest.main()
