"""Deterministic v88 evaluator latency/failure benchmark, not AI-assisted timing.

Run: python -m tests.benchmark_evaluation_latency_v88
Development examples only; measurements depend on runner hardware.
"""
import json
import time
from collections import Counter
from tests.generate_curated_evaluation_v88 import build_diverse_cases
from tests.run_evaluation_benchmark import _percentile
from app.services.answer_intelligence import evaluate_structured_answer


def measure(rows=None, evaluator=evaluate_structured_answer):
    rows = build_diverse_cases() if rows is None else rows
    latencies = []
    failures = Counter()
    for row in rows:
        start = time.perf_counter()
        try:
            evaluator(row["learner_answer"], row["exercise"])
        except Exception as exc:
            failures[type(exc).__name__] += 1
        finally:
            latencies.append((time.perf_counter() - start) * 1000)
    count = len(rows)
    failed = sum(failures.values())
    return {
        "benchmark": "deterministic_only", "cases": count,
        "p50_ms": _percentile(latencies, 0.50),
        "p95_ms": _percentile(latencies, 0.95),
        "failures": failed, "failure_rate": round(failed / count, 4) if count else None,
        "failure_types": dict(failures),
        "deterministic_latency_gate": bool(count and not failed and _percentile(latencies, 0.95) < 200),
        "ai_assisted_latency": "not_measured",
        "release_gate": "blocked",
    }


if __name__ == "__main__":
    print(json.dumps(measure(), indent=2))
