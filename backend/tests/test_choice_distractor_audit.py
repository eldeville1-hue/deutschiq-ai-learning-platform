import unittest

from app.services.content_quality import exercise_answer_audit


class ChoiceDistractorAuditTests(unittest.TestCase):
    def test_flags_choice_with_only_accepted_options(self):
        lesson = {"exercises": [{
            "type": "choose", "question": "Choose the correct sentence",
            "answer": "Ich lerne Deutsch.",
            "accepted_answers": ["Ich lerne Deutsch.", "Heute lerne ich Deutsch."],
            "options": ["Ich lerne Deutsch.", "Heute lerne ich Deutsch."],
        }]}
        self.assertIn("exercise:0:no_incorrect_distractor", exercise_answer_audit(lesson))

    def test_valid_choice_with_wrong_distractor_is_not_flagged(self):
        lesson = {"exercises": [{
            "type": "choose", "answer": "Ich lerne Deutsch.",
            "accepted_answers": ["Ich lerne Deutsch."],
            "options": ["Ich lerne Deutsch.", "Ich Deutsch lerne."],
        }]}
        self.assertEqual(exercise_answer_audit(lesson), [])

    def test_legacy_non_choice_tasks_unaffected(self):
        lesson = {"exercises": [{"type": "fill", "answer": "lerne"}]}
        self.assertEqual(exercise_answer_audit(lesson), [])


if __name__ == "__main__":
    unittest.main()
