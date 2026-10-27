import unittest

from app.services.production_feedback import local_feedback


class ModelCopyScoringTests(unittest.TestCase):
    def test_exact_model_copy_does_not_receive_perfect_dimension_scores(self):
        model = 'Ich lerne Deutsch, weil ich in Deutschland studieren möchte.'
        result = local_feedback(model, {'answer': model}, '', lang='de', cefr='B2')
        self.assertLess(result['score'], 100)
        self.assertTrue(any(value < 100 for value in result['dimension_scores'].values()))

    def test_model_copy_cannot_bypass_minimum_response_length(self):
        model = 'Hallo.'
        result = local_feedback(model, {'answer': model}, '', lang='en', cefr='B2')
        self.assertFalse(result['correct'])
        self.assertEqual(result['error_type'], 'response_too_short')
