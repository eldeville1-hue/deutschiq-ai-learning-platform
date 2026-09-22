import unittest
from types import SimpleNamespace

from app.services.assessment_insights import assessment_insights, evidence_gate


def attempt(topic, **scores):
    return SimpleNamespace(topic=topic, assessment={"dimensions": scores})


class AssessmentInsightTests(unittest.TestCase):
    def test_finds_weakest_dimension_and_topic(self):
        rows = [
            attempt("opinion", task_completion=80, grammar=70, vocabulary=76, coherence=42, register=72),
            attempt("opinion", task_completion=85, grammar=75, vocabulary=74, coherence=48, register=70),
            attempt("formal_email", task_completion=78, grammar=65, vocabulary=68, coherence=60, register=55),
        ]
        result = assessment_insights(rows)
        self.assertEqual("coherence", result["weakest_dimension"])
        self.assertEqual("opinion", result["priority_topics"][0]["topic"])

    def test_gate_is_compatible_until_enough_evidence_exists(self):
        rows = [attempt("opinion", task_completion=30, grammar=30, vocabulary=60, coherence=30, register=60)]
        self.assertTrue(evidence_gate(rows)["eligible"])
        self.assertEqual("building_evidence", evidence_gate(rows)["status"])

    def test_gate_catches_hidden_core_gap(self):
        rows = [attempt("opinion", task_completion=90, grammar=80, vocabulary=95, coherence=35, register=95) for _ in range(3)]
        gate = evidence_gate(rows)
        self.assertFalse(gate["eligible"])
        self.assertIn("coherence", gate["gaps"])
