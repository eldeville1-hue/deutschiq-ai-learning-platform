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



def build_report(holdout_path=None, benchmark=None, linguistic=None, ci_evidence=None, expected_sha=None, job_evidence=None, ai_benchmark=None):
    benchmark = measure() if benchmark is None else benchmark
    linguistic = (evaluate_file(holdout_path) if holdout_path else validation_report([])) if linguistic is None else linguistic
    from tests.collect_ci_evidence_v88 import REQUIRED_JOBS
    job_verified = isinstance(job_evidence, dict) and job_evidence.get("verified") is True and job_evidence.get("head_sha") == expected_sha and bool(expected_sha)
    jobs = job_evidence.get("jobs", {}) if job_verified else {}
    ai_ok = isinstance(ai_benchmark, dict) and ai_benchmark.get("measured") is True and ai_benchmark.get("p95_ms") is not None and ai_benchmark["p95_ms"] < 2500 and ai_benchmark.get("failure_rate") is not None and ai_benchmark["failure_rate"] < 0.01
    checks = {
        "deterministic_performance": benchmark.get("deterministic_latency_gate") is True
            and benchmark.get("failure_rate") is not None and benchmark["failure_rate"] < 0.01,
        "independent_linguistic_review": bool(holdout_path)
            and not linguistic.get("ingestion_errors")
            and linguistic.get("release_checks", {}).get("independent_holdout") is True
            and not any(x for x in linguistic.get("failed_gates", []) if not x.startswith("manual:")),
        "ai_assisted_performance": ai_ok,
        "xp_safety_ci_signoff": job_verified and jobs.get("backend", {}).get("conclusion") == "success",
        "mobile_e2e_signoff": job_verified and jobs.get("e2e-mobile", {}).get("conclusion") == "success",
        "frontend_ci_signoff": job_verified and jobs.get("frontend", {}).get("conclusion") == "success",
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
        "ai_benchmark": ai_benchmark,
        "job_evidence": job_evidence,
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
