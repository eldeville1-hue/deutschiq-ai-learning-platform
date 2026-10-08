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
                                     {"cefr": "B1", "objective": "German communication"}, "en")
    if result.get("source") != "ai":
        raise RuntimeError("AI evaluator did not return AI-sourced evidence")
    return result


async def main():
    if not os.environ.get("OPENAI_API_KEY"):
        report = {"measured": False, "release_gate": "blocked",
                  "reason": "OPENAI_API_KEY missing; no real AI measurements"}
    else:
        report = await measure_ai(CASES, production_adapter)
        report["representative_release_sample"] = False
        report["release_gate"] = "blocked"
    print(json.dumps(report, indent=2))
    return 2


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
