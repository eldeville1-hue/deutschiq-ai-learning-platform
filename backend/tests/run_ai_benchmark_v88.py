"""Benchmark actual production AI scoring, never silently benchmark local fallback.

From backend/: python -m tests.run_ai_benchmark_v88
Requires OPENAI_API_KEY. No keys or learner data are logged.
"""
import asyncio
import json
import os
import sys

from app.services.production_feedback import _ai_feedback
from tests.benchmark_ai_evaluation_v88 import measure_ai
from tests.prepare_ai_workload_v88 import prepare, LEVELS, MIN_PER_LEVEL

CASES = [
    {"learner_answer": "Ich denke, dass Deutsch lernen wichtig ist, weil es mir bei der Arbeit hilft.",
     "exercise": {"type": "production", "question": "Warum lernst du Deutsch?",
                  "model_answer": "Ich lerne Deutsch, weil ich in Deutschland arbeiten möchte."}},
    {"learner_answer": "Meiner Meinung nach ist regelmäßiges Lernen hilfreich, obwohl es manchmal schwierig sein kann.",
     "exercise": {"type": "production", "question": "Beschreibe einen Vorteil und einen Nachteil des Lernens.",
                  "model_answer": "Lernen verbessert die Chancen, kann aber anstrengend sein."}},
]


async def production_adapter(answer, exercise):
    result = await asyncio.to_thread(_ai_feedback, answer, exercise,
                                     {"cefr": exercise.get("benchmark_cefr", "B1"), "objective": "German communication"}, "en")
    if result.get("source") != "ai":
        raise RuntimeError("AI evaluator did not return AI-sourced evidence")
    return result


async def main():
    if not os.environ.get("OPENAI_API_KEY"):
        report = {"measured": False, "release_gate": "blocked",
                  "reason": "OPENAI_API_KEY missing; no real AI measurements"}
    else:
        manifest = prepare()
        if manifest["validation_errors"]:
            report = {"measured": False, "release_gate": "blocked", "validation_errors": manifest["validation_errors"]}
            print(json.dumps(report, indent=2))
            return 2
        rows = []
        for case in manifest["cases"]:
            exercise = dict(case["exercise"], benchmark_cefr=case["cefr"])
            rows.append({"learner_answer": case["learner_answer"], "exercise": exercise})
        report = await measure_ai(rows, production_adapter)
        report["counts_by_level"] = manifest["counts_by_level"]
        report["real_ai_adapter"] = True
        report["workload_source"] = manifest["source"]
        report["representative_release_sample"] = False
        report["release_gate"] = "blocked"
    print(json.dumps(report, indent=2))
    return 2


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
