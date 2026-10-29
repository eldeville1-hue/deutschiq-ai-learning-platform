"""Regression coverage for machine-readable offline curriculum build failures."""
import unittest
from unittest.mock import patch

import audit_curriculum


class CurriculumBuildFindingsTests(unittest.TestCase):
    def test_build_exception_is_blocking_and_in_structured_findings(self):
        def broken_builder(*args, **kwargs):
            raise ValueError("deliberate broken lesson")

        with (
            patch.object(audit_curriculum, "CURRICULUM", [(42,)]),
            patch.object(audit_curriculum, "A1_CURRICULUM", []),
            patch.object(audit_curriculum, "A2_CURRICULUM", []),
            patch.object(audit_curriculum, "B1_CURRICULUM", []),
            patch.object(audit_curriculum, "B2_CURRICULUM", []),
            patch.object(audit_curriculum, "build_content", side_effect=ValueError("deliberate broken lesson")),
            patch.object(audit_curriculum, "curriculum_audit_report", return_value={}),
        ):
            report = audit_curriculum.build_report()

        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["total_exercise_issues"], 1)
        self.assertEqual(report["exercise_issues"]["30-day roadmap"][0]["category"], "build")
        finding = report["exercise_findings"][0]
        self.assertEqual(finding["track"], "30-day roadmap")
        self.assertEqual(finding["level"], "A1")
        self.assertEqual(finding["day"], 42)
        self.assertIsNone(finding["exercise_index"])
        self.assertEqual(finding["category"], "build")
        self.assertEqual(finding["severity"], "blocking")
        self.assertIn("ValueError:deliberate broken lesson", finding["evidence"])


if __name__ == "__main__":
    unittest.main()
