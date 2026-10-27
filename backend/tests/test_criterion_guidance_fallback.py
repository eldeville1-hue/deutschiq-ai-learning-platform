import unittest

from app.services.production_feedback import _criterion_improvement


class CriterionGuidanceFallbackTests(unittest.TestCase):
    def test_formal_message_components_have_actionable_guidance_in_each_language(self):
        for key in ('formal_greeting', 'rescheduling_request', 'formal_closing'):
            for language in ('ru', 'de', 'en'):
                with self.subTest(key=key, language=language):
                    guidance = _criterion_improvement([key], language)
                    self.assertIsInstance(guidance, str)
                    self.assertGreater(len(guidance), 15)

    def test_missing_formal_component_has_priority_over_generic_ai_advice(self):
        self.assertEqual(
            _criterion_improvement(['formal_greeting', 'numeric_value_and_period'], 'en'),
            'Start the message with a formal greeting.',
        )
