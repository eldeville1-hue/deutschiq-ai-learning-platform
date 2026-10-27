import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.services.production_feedback import _ai_feedback, DIMENSIONS


class AIFormalTaskScoreConsistencyTests(unittest.TestCase):
    def test_ai_cannot_report_high_task_completion_for_missing_formal_parts(self):
        answer = 'Ich möchte den Termin verschieben, weil ich arbeiten muss.'
        exercise = {'question': 'Schreiben Sie eine formelle Nachricht.', 'assessment_criteria': ['formal_closing']}
        payload = {
            'criteria_met': {'formal_closing': True},
            'dimension_scores': {key: 95 for key in DIMENSIONS},
            'feedback': 'Die Nachricht ist unvollständig.',
            'improvement': 'Ergänze die Anrede und den Gruß.',
            'corrected_answer': 'Sehr geehrte Frau Klein, ich möchte den Termin verschieben. Mit freundlichen Grüßen.',
        }
        with patch('openai.OpenAI') as client:
            client.return_value.chat.completions.create.return_value = SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))]
            )
            for lang in ('ru', 'de', 'en'):
                with self.subTest(lang=lang):
                    result = _ai_feedback(answer, exercise, {'cefr': 'B2'}, lang)
                    self.assertFalse(result['correct'])
                    self.assertLessEqual(result['dimension_scores']['task_completion'], 50)
                    self.assertIn('formal_greeting', result['missing_task_parts'])
