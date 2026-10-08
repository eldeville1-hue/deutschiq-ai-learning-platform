import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.generate_release_report_v88 import generate


class ReleaseArtifactTests(unittest.TestCase):
    def test_report_contains_commit_bound_job_evidence_and_remains_blocked(self):
        sha = "a" * 40
        evidence = {"verified": True, "head_sha": sha, "run_id": 42,
                    "jobs": {name: {"conclusion": "success"}
                             for name in ("backend", "frontend", "e2e-mobile")}}
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "release.json")
            with patch("tests.generate_release_report_v88.collect", return_value=evidence), patch(
                "tests.generate_release_report_v88.build_report",
                return_value={"release_gate": "blocked", "failed_gates": ["external_human_signoff"],
                              "job_evidence": evidence},
            ) as builder:
                report = generate("owner/repo", 42, sha, path)
            builder.assert_called_once_with(job_evidence=evidence, expected_sha=sha)
            self.assertEqual(report["release_gate"], "blocked")
            saved = json.loads(Path(path).read_text(encoding="utf-8"))
            self.assertEqual(saved["ci_run_id"], 42)
            self.assertEqual(saved["job_evidence"]["head_sha"], sha)


if __name__ == "__main__":
    unittest.main()
