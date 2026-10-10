import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import audit_curriculum


class CurriculumAuditCliTests(unittest.TestCase):
    def test_clean_report_succeeds(self):
        with patch.object(audit_curriculum, "curriculum_audit_report", return_value={"A1": [], "B2": []}):
            report = audit_curriculum.build_report()
            self.assertEqual("passed", report["status"])
            self.assertEqual(0, report["total_issues"])

    def test_failed_report_exits_nonzero_and_writes_json(self):
        problems = {"A1": [{"day": 3, "issues": ["missing:objective", "missing:rule"]}], "B2": []}
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "reports" / "audit.json"
            with patch.object(audit_curriculum, "curriculum_audit_report", return_value=problems):
                result = audit_curriculum.main(["--output", str(target)])
            self.assertEqual(1, result)
            saved = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual("failed", saved["status"])
            self.assertEqual(2, saved["total_issues"])
            self.assertEqual(1, saved["affected_lessons"])
            self.assertEqual(3, saved["tracks"]["A1"][0]["day"])


if __name__ == "__main__":
    unittest.main()
