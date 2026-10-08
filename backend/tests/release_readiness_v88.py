"""Local v88 readiness evidence. Missing independent evidence blocks release."""
import json
import sys
from tests.benchmark_evaluation_latency_v88 import measure
from tests.holdout_pipeline_v88 import evaluate_file
from tests.run_evaluation_benchmark import validation_report


def ci_evidence_check(evidence, expected_sha):
    if not isinstance(evidence, dict) or not expected_sha:
        return False
    return (evidence.get("head_sha") == expected_sha
            and evidence.get("status") == "completed"
            and evidence.get("conclusion") == "success"
            and bool(evidence.get("run_id")))



def build_report(holdout_path=None, benchmark=None, linguistic=None, ci_evidence=None, expected_sha=None):
    benchmark = measure() if benchmark is None else benchmark
    linguistic = (evaluate_file(holdout_path) if holdout_path else validation_report([])) if linguistic is None else linguistic
    checks = {
        "deterministic_performance": benchmark.get("deterministic_latency_gate") is True
            and benchmark.get("failure_rate") is not None and benchmark["failure_rate"] < 0.01,
        "independent_linguistic_review": bool(holdout_path)
            and not linguistic.get("ingestion_errors")
            and linguistic.get("release_checks", {}).get("independent_holdout") is True
            and not any(x for x in linguistic.get("failed_gates", []) if not x.startswith("manual:")),
        "ai_assisted_performance": False,
        "xp_safety_ci_signoff": False,
        "mobile_e2e_signoff": False,
        "external_human_signoff": False,
        "production_smoke": False,
    }
    return {
        "version": "v88",
        "ci_evidence": {"matched_successful_run": ci_evidence_check(ci_evidence, expected_sha),
                        "expected_sha": expected_sha,
                        "note": "Run metadata does not establish job-level or mobile E2E signoff."},
        "release_gate": "blocked",
        "checks": checks,
        "failed_gates": sorted(key for key, passed in checks.items() if not passed),
        "benchmark": benchmark,
        "linguistic_validation": linguistic,
        "evidence_scope": "local benchmark and optional external holdout; no CI or signoff attestation",
    }


if __name__ == "__main__":
    try:
        report = build_report(sys.argv[1] if len(sys.argv) == 2 else None)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        report = {"release_gate": "blocked", "failed_gates": ["report_generation"], "error": str(exc)}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(2)
