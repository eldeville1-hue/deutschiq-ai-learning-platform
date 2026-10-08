"""Measure actual async AI evaluation calls using an injected production adapter.

No fake AI calls are counted. Adapter must implement async evaluate(answer, exercise).
"""
import asyncio
import time
from tests.run_evaluation_benchmark import _percentile


async def measure_ai(rows, evaluator, timeout_seconds=10):
    durations = []
    errors = {}
    for row in rows:
        start = time.perf_counter()
        try:
            await asyncio.wait_for(evaluator(row["learner_answer"], row["exercise"]),
                                   timeout=timeout_seconds)
        except Exception as exc:
            name = type(exc).__name__
            errors[name] = errors.get(name, 0) + 1
        finally:
            durations.append((time.perf_counter() - start) * 1000)
    n = len(durations)
    failures = sum(errors.values())
    p95 = _percentile(durations, 0.95)
    return {
        "measured": bool(n), "sample_count": n,
        "p50_ms": _percentile(durations, 0.5), "p95_ms": p95,
        "failure_count": failures, "failure_rate": round(failures / n, 4) if n else None,
        "error_types": errors, "latency_gate": bool(n and p95 < 2500 and failures / n < 0.01),
        "release_gate": "blocked",
        "note": "An injected real AI adapter and representative workload are required for release evidence.",
    }
