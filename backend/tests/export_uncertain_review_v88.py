"""Export a blind, targeted review packet for uncertain v88 development cases.

This is a triage aid, NOT an independent holdout or release approval.
Run: python -m tests.export_uncertain_review_v88 OUTPUT.csv MANIFEST.json
"""
import json
import hashlib
import sys
from collections import Counter
from pathlib import Path

from app.services.answer_intelligence import evaluate_structured_answer
from tests.generate_curated_evaluation_v88 import build_diverse_cases
from tests.review_evaluation_benchmark import export_packet


def select_uncertain(rows=None, evaluator=evaluate_structured_answer):
    rows = build_diverse_cases() if rows is None else rows
    selected = []
    seen = set()
    counts = Counter()
    for row in rows:
        identifier = row["id"]
        if identifier in seen:
            raise ValueError("Duplicate case ID: " + identifier)
        seen.add(identifier)
        result = evaluator(row["learner_answer"], row["exercise"])
        status = result.get("evaluation_status")
        if status not in {"verified", "uncertain", "needs_review"}:
            raise ValueError("Invalid evaluator status for " + identifier)
        if status != "verified":
            selected.append(row)
            counts[row["cefr"]] += 1
    canonical = [{key: row.get(key) for key in ("id", "cefr", "objective", "learner_answer")} | {"exercise": row["exercise"]} for row in selected]
    fingerprint = hashlib.sha256(json.dumps(canonical, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
    return selected, {
        "version": "v88",
        "purpose": "blind_development_uncertainty_triage",
        "source": "curated_development_unreviewed",
        "independent_holdout": False,
        "reviewer_independence_verified": False,
        "release_gate": "blocked",
        "total": len(selected),
        "case_content_sha256": fingerprint,
        "counts_by_level": {level: counts[level] for level in ("A1", "A2", "B1", "B2")},
        "case_ids": [row["id"] for row in selected],
        "note": "CSV excludes evaluator predictions and provisional labels. Reviews are not independent holdout evidence.",
    }


def write_packet(csv_path, manifest_path, rows=None, evaluator=evaluate_structured_answer):
    selected, manifest = select_uncertain(rows, evaluator)
    export_packet(csv_path, rows=selected)
    path = Path(manifest_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python -m tests.export_uncertain_review_v88 OUTPUT.csv MANIFEST.json")
    print(json.dumps(write_packet(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=2))
