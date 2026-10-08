"""Prepare a privacy-safe, balanced A1-B2 AI benchmark manifest.

Development-only inputs: never claim independent review or real model timings.
Run from backend/: python -m tests.prepare_ai_workload_v88 OUTPUT.json
"""
import json
import sys
from collections import Counter
from pathlib import Path
from tests.generate_curated_evaluation_v88 import build_cases

LEVELS = ("A1", "A2", "B1", "B2")
MIN_PER_LEVEL = 25


def prepare(rows=None):
    rows = build_cases() if rows is None else rows
    selected = []
    counts = Counter()
    for row in rows:
        level = row.get("cefr")
        if level not in LEVELS or counts[level] >= MIN_PER_LEVEL:
            continue
        exercise = row.get("exercise") or {}
        answer = row.get("learner_answer")
        question = exercise.get("question") or row.get("objective")
        reference = exercise.get("answer") or exercise.get("model_answer")
        if not all(isinstance(value, str) and value.strip()
                   for value in (answer, question, reference)):
            continue
        selected.append({
            "id": str(row.get("id", "")),
            "cefr": level,
            "learner_answer": answer,
            "exercise": {
                "type": exercise.get("type", "translation"),
                "question": question,
                "model_answer": reference,
            },
        })
        counts[level] += 1
    errors = [f"insufficient_{level}:{counts[level]}/{MIN_PER_LEVEL}"
              for level in LEVELS if counts[level] < MIN_PER_LEVEL]
    return {
        "version": "v88",
        "source": "curated_development_unreviewed",
        "contains_real_user_data": False,
        "independently_reviewed": False,
        "representative_release_sample": False,
        "sample_count": len(selected),
        "counts_by_level": dict(counts),
        "validation_errors": errors,
        "cases": selected,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m tests.prepare_ai_workload_v88 OUTPUT.json")
    manifest = prepare()
    Path(sys.argv[1]).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in manifest.items() if key != "cases"}, indent=2))
    raise SystemExit(2 if manifest["validation_errors"] else 0)
