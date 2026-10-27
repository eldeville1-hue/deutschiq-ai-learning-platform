import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.services.production_feedback import _ai_feedback


class AIFeedbackPayloadValidationTests(unittest.TestCase):
    def test_non_object_payloads_are_rejected(self):
        exercise = {'question': 'Schreibe eine Nachricht.'}
        for payload in ([], None, 'incorrect', 12, {'dimension_scores': []}, {'dimension_scores': None}):
            with self.subTest(payload=payload), patch('openai.OpenAI') as client:
                client.return_value.chat.completions.create.return_value = SimpleNamespace(
                    choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))]
                )
                with self.assertRaises(ValueError):
                    _ai_feedback('Ich schreibe eine Nachricht.', exercise, {'cefr': 'B1'}, 'de')
