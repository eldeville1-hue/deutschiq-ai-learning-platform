"""Compare reviewed v88 development cases with the current structured evaluator.

This is a diagnostic triage report, not a validated accuracy benchmark or release signoff.
Usage: python -m tests.triage_review_disagreements_v88 REVIEWED.jsonl REPORT.json
"""
import json
import sys
from collections import Counter
from pathlib import Path

from app.services.answer_intelligence import evaluate_structured_answer

LEVELS = ("A1", "A2", "B1", "B2")


def triage(rows, evaluator=evaluate_structured_answer):
    findings = []
    counts = Counter()
    reviewed = Counter()
    seen = set()
    for row in rows:
        identifier = row["id"]
        if identifier in seen:
            raise ValueError("Duplicate reviewed case: " + identifier)
        seen.add(identifier)
        level = row.get("cefr")
        if level not in LEVELS:
            raise ValueError("Invalid CEFR level: " + str(level))
        review = row.get("human_review") or {}
        decision = review.get("decision")
        if review.get("status") != "pending_independence_verification":
            continue
        if decision not in {"correct", "incorrect", "uncertain"} or not review.get("reviewer"):
            raise ValueError("Invalid pending reviewer decision: " + identifier)
        error_types = review.get("error_types") or []
        if not isinstance(error_types, list) or any(not isinstance(value, str) or not value.strip() for value in error_types):
            raise ValueError("Invalid reviewer error types: " + identifier)
        if decision == "incorrect" and not error_types:
            raise ValueError("Incorrect review lacks diagnosis: " + identifier)
        if decision == "correct" and error_types:
            raise ValueError("Correct review includes error diagnoses: " + identifier)
        reviewed[level] += 1
        result = evaluator(row["learner_answer"], row["exercise"])
        status = result.get("evaluation_status")
        if status not in {"verified", "uncertain", "needs_review"}:
            raise ValueError("Invalid evaluator status: " + identifier)
        if result.get("correct") and status != "verified":
            raise ValueError("Unverified correct evaluation: " + identifier)
        kind = None
        if decision == "incorrect" and result.get("correct"):
            kind = "potential_false_acceptance"
        elif decision == "correct" and status == "verified" and not result.get("correct"):
            kind = "potential_false_rejection"
        elif decision == "correct" and status != "verified":
            kind = "correct_answer_unverified"
        elif decision == "incorrect" and status != "verified":
            kind = "incorrect_answer_unverified"
        elif decision == "uncertain":
            kind = "reviewer_uncertain"
        elif decision == "incorrect" and status == "verified" and not result.get("correct"):
            reviewer_types = set(review.get("error_types") or [])
            evaluator_types = {error.get("type") for error in result.get("errors", [])
                               if isinstance(error, dict) and error.get("type")}
            if not evaluator_types and result.get("error_type"):
                evaluator_types = {result["error_type"]}
            if reviewer_types and not evaluator_types:
                kind = "missing_evaluator_diagnosis"
            elif reviewer_types and evaluator_types and reviewer_types.isdisjoint(evaluator_types):
                kind = "potential_diagnosis_mismatch"
        if kind:
            counts[(level, kind)] += 1
            findings.append({
                "id": identifier, "cefr": level, "kind": kind,
                "evaluation_status": status, "evaluator_correct": bool(result.get("correct")),
                "reviewer_decision": decision,
                "reviewer_error_types": review.get("error_types", []),
                "evaluator_error_types": sorted({error.get("type") for error in result.get("errors", [])
                                                 if isinstance(error, dict) and error.get("type")}
                                                or ({result["error_type"]} if result.get("error_type") else set())),
            })
    priority = {"potential_false_acceptance": 0, "potential_false_rejection": 1,
                "correct_answer_unverified": 3, "incorrect_answer_unverified": 4,
                "potential_diagnosis_mismatch": 2, "missing_evaluator_diagnosis": 2, "reviewer_uncertain": 5}
    findings.sort(key=lambda item: (priority[item["kind"]], item["cefr"], item["id"]))
    return {
        "version": "v88", "source": "reviewed_development_cases",
        "review_independence_verified": False, "independent_holdout": False,
        "release_gate": "blocked",
        "reviewed_count_by_level": {level: reviewed[level] for level in LEVELS},
        "finding_counts_by_level": {
            level: {kind: value for (lvl, kind), value in sorted(counts.items()) if lvl == level}
            for level in LEVELS
        },
        "findings": findings,
        "note": "Findings are provisional until reviewer identity and independence are verified; no release accuracy is inferred.",
    }


def generate(input_path, output_path):
    rows = [json.loads(line) for line in Path(input_path).read_text(encoding="utf-8").splitlines() if line.strip()]
    report = triage(rows)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python -m tests.triage_review_disagreements_v88 REVIEWED.jsonl REPORT.json")
    result = generate(sys.argv[1], sys.argv[2])
    print(json.dumps({"reviewed_count_by_level": result["reviewed_count_by_level"],
                      "finding_counts_by_level": result["finding_counts_by_level"],
                      "release_gate": result["release_gate"]}, indent=2))
