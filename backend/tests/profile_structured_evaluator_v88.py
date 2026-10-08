"""Measure v88 structured evaluation status and latency by CEFR level.

Development cases only. Provisional expectations are NOT accuracy labels.
Run from backend/: python -m tests.profile_structured_evaluator_v88 OUTPUT.json
"""
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from app.services.answer_intelligence import evaluate_structured_answer
from tests.generate_curated_evaluation_v88 import build_diverse_cases
from tests.run_evaluation_benchmark import _percentile

LEVELS = ("A1", "A2", "B1", "B2")
STATUSES = ("verified", "uncertain", "needs_review")


def profile(rows=None, evaluator=evaluate_structured_answer):
    rows = build_diverse_cases() if rows is None else rows
    grouped = defaultdict(lambda: {"latencies": [], "statuses": Counter(), "errors": Counter(), "families": defaultdict(Counter), "uncertain_examples": []})
    for row in rows:
        level = row.get("cefr")
        if level not in LEVELS:
            continue
        item = grouped[level]
        start = time.perf_counter()
        try:
            result = evaluator(row["learner_answer"], row["exercise"])
            status = result.get("evaluation_status")
            if status not in STATUSES:
                item["errors"]["invalid_evaluation_status"] += 1
            else:
                item["statuses"][status] += 1
                family = row.get("task_family", row.get("exercise", {}).get("type", "unknown"))
                item["families"][family][status] += 1
                if status != "verified" and len(item["uncertain_examples"]) < 10:
                    item["uncertain_examples"].append({"id": row.get("id"), "task_family": family,
                                                       "status": status})
        except Exception as exc:
            item["errors"][type(exc).__name__] += 1
        finally:
            item["latencies"].append((time.perf_counter() - start) * 1000)
    levels = {}
    for level in LEVELS:
        item = grouped[level]
        count = len(item["latencies"])
        failures = sum(item["errors"].values())
        levels[level] = {
            "sample_count": count,
            "p50_ms": _percentile(item["latencies"], 0.5),
            "p95_ms": _percentile(item["latencies"], 0.95),
            "status_counts": {status: item["statuses"][status] for status in STATUSES},
            "task_family_status_counts": {family: dict(counts) for family, counts in sorted(item["families"].items())},
            "uncertain_examples": item["uncertain_examples"],
            "definitive_coverage": round(item["statuses"]["verified"] / count, 4) if count else None,
            "failure_count": failures,
            "failure_rate": round(failures / count, 4) if count else None,
            "deterministic_latency_gate": bool(count >= 100 and failures == 0
                                               and _percentile(item["latencies"], 0.95) < 200),
        }
    return {
        "version": "v88",
        "evaluator": "answer_intelligence.evaluate_structured_answer",
        "workload_source": "curated_development_unreviewed",
        "independently_reviewed": False,
        "release_gate": "blocked",
        "levels": levels,
    }


def save_report(report, path):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    report = profile()
    if len(sys.argv) > 1:
        save_report(report, sys.argv[1])
    print(json.dumps(report, indent=2))
    raise SystemExit(2 if any(not x["deterministic_latency_gate"] for x in report["levels"].values()) else 0)
