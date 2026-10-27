import unittest

from app.services.production_feedback import local_feedback


class FormalTaskScoringTests(unittest.TestCase):
    def test_exact_model_missing_formal_parts_cannot_receive_perfect_score(self):
        model = 'Ich möchte den Termin verschieben.'
        result = local_feedback(model, {'answer': model, 'assessment_criteria': ['formal_closing']}, '', lang='de', cefr='B2')
        self.assertFalse(result['correct'])
        self.assertLess(result['score'], 100)
        self.assertLess(result['dimension_scores']['task_completion'], 60)
        self.assertIn('formal_greeting', result['missing_task_parts'])

    def test_complete_authored_model_keeps_full_credit(self):
        model = 'Sehr geehrte Frau Klein, ich möchte den Termin verschieben. Mit freundlichen Grüßen.'
        result = local_feedback(model, {'answer': model, 'assessment_criteria': ['formal_closing']}, '', lang='de', cefr='B2')
        self.assertTrue(result['correct'])
        self.assertEqual(result['score'], 100)
