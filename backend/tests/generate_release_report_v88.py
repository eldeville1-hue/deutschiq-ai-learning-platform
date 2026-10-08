"""Generate consolidated v88 report from actual GitHub Actions job evidence.

Usage: python -m tests.generate_release_report_v88 OWNER/REPO RUN_ID SHA OUTPUT.json
The report is always blocked until independent human review and all gates pass.
"""
import json
import sys
from pathlib import Path
from tests.collect_ci_evidence_v88 import collect
from tests.release_readiness_v88 import build_report


def generate(repo, run_id, sha, output):
    evidence = collect(repo, run_id, sha)
    report = build_report(job_evidence=evidence, expected_sha=sha)
    report["ci_run_id"] = int(run_id)
    report["ci_repository"] = repo
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    try:
        if len(sys.argv) != 5:
            raise ValueError("Usage: OWNER/REPO RUN_ID SHA OUTPUT.json")
        result = generate(*sys.argv[1:])
        print(json.dumps({"output": sys.argv[4], "release_gate": result["release_gate"],
                          "failed_gates": result["failed_gates"]}, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"release_gate": "blocked", "error": str(exc)}))
        raise SystemExit(2)
