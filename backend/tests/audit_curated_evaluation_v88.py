"""Fail-closed structural audit of unreviewed DeutschIQ v88 curated fixtures.

This is a consistency checker, not a German-language expert or independent review.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path
from app.services.answer_intelligence import normalize_text, evaluate_structured_answer
from tests.generate_curated_evaluation_v88 import build_diverse_cases

LEVELS = ("A1", "A2", "B1", "B2")
VARIANTS = ("model", "accepted_paraphrase", "targeted_error", "empty", "unlisted_extension")

def audit(rows=None):
    rows = build_diverse_cases() if rows is None else rows
    problems = []
    seen_ids = set()
    seen_keys = set()
    by_level = Counter()
    by_family = Counter()
    provisional_confusion = Counter()
    error_candidates = Counter()
    for row in rows:
        identifier = row.get("id", "")
        if not identifier or identifier in seen_ids:
            problems.append({"id": identifier, "issue": "missing_or_duplicate_id"})
        seen_ids.add(identifier)
        level = row.get("cefr")
        if level not in LEVELS:
            problems.append({"id": identifier, "issue": "unknown_cefr"})
        by_level[level] += 1
        exercise = row.get("exercise") or {}
        family = row.get("task_family")
        by_family[family] += 1
        if family != exercise.get("type"):
            problems.append({"id": identifier, "issue": "task_family_type_mismatch"})
        prompt = (row.get("objective") or "").strip()
        if not prompt or prompt != exercise.get("question"):
            problems.append({"id": identifier, "issue": "missing_or_mismatched_prompt"})
        model = exercise.get("answer") or ""
        accepted = exercise.get("accepted_answers") or []
        if not normalize_text(model) or not accepted or normalize_text(model) not in {normalize_text(x) for x in accepted}:
            problems.append({"id": identifier, "issue": "missing_reference_or_accepted_model"})
        if len({normalize_text(x) for x in accepted}) != len(accepted):
            problems.append({"id": identifier, "issue": "duplicate_accepted_answer"})
        answer = row.get("learner_answer", "")
        key = (level, family, normalize_text(prompt), normalize_text(answer))
        if key in seen_keys:
            problems.append({"id": identifier, "issue": "duplicate_prompt_answer"})
        seen_keys.add(key)
        review = row.get("human_review") or {}
        if review.get("status") != "pending":
            problems.append({"id": identifier, "issue": "curated_fixture_must_remain_unreviewed"})
        if row.get("split") != "development":
            problems.append({"id": identifier, "issue": "curated_fixture_must_not_be_holdout"})
        expected = row.get("provisional_expected")
        if expected not in {"correct", "incorrect", "uncertain"}:
            problems.append({"id": identifier, "issue": "invalid_provisional_label"})
        normalized_answer = normalize_text(answer)
        if expected == "correct" and normalized_answer not in {normalize_text(x) for x in accepted}:
            problems.append({"id": identifier, "issue": "correct_not_in_accepted_answers"})
        if expected == "incorrect" and normalized_answer in {normalize_text(x) for x in accepted}:
            problems.append({"id": identifier, "issue": "incorrect_is_accepted_answer"})
        if family == "error_repair" and not row.get("provisional_error_type"):
            problems.append({"id": identifier, "issue": "repair_missing_error_category"})
        if row.get("source") != "curated_author_written_unreviewed":
            problems.append({"id": identifier, "issue": "incorrect_provenance"})
        result = evaluate_structured_answer(answer, exercise)
        actual = "uncertain" if result["evaluation_status"] != "verified" else ("correct" if result["correct"] else "incorrect")
        provisional_confusion[f"{expected}->{actual}"] += 1
        if expected == "incorrect":
            error_candidates[(level, row.get("provisional_error_type") or "unspecified", actual)] += 1
    return {
        "total": len(rows),
        "levels": dict(sorted(by_level.items())),
        "families": dict(sorted(by_family.items())),
        "structural_issues": problems,
        "structural_issue_count": len(problems),
        "provisional_confusion": dict(sorted(provisional_confusion.items())),
        "provisional_error_outcomes": [
            {"cefr": level, "provisional_error_type": category, "predicted": prediction, "count": count}
            for (level, category, prediction), count in sorted(error_candidates.items())
        ],
        "human_reviewed": 0,
        "independently_validated": False,
        "release_gate": "blocked",
        "disclaimer": "Structural checks and provisional labels are not independent linguistic validation.",
    }

def triage(rows=None, evaluator=evaluate_structured_answer):
    """Rank provisional disagreements for review; never treat labels as ground truth."""
    rows = build_diverse_cases() if rows is None else rows
    priorities = {"potential_false_accept": 0, "potential_false_reject": 1,
                  "potential_misdiagnosis": 2, "deferred_incorrect": 3, "deferred_correct": 4}
    cases = []
    for row in rows:
        result = evaluator(row["learner_answer"], row["exercise"])
        predicted = ("uncertain" if result.get("evaluation_status") != "verified"
                     else "correct" if result.get("correct") else "incorrect")
        expected = row.get("provisional_expected")
        kind = None
        if expected == "incorrect" and predicted == "correct":
            kind = "potential_false_accept"
        elif expected == "correct" and predicted == "incorrect":
            kind = "potential_false_reject"
        elif expected == "incorrect" and predicted == "uncertain":
            kind = "deferred_incorrect"
        elif expected == "correct" and predicted == "uncertain":
            kind = "deferred_correct"
        elif expected == "incorrect" and predicted == "incorrect":
            types = {e.get("type") for e in result.get("errors", []) if isinstance(e, dict)}
            if row.get("provisional_error_type") and row["provisional_error_type"] not in types:
                kind = "potential_misdiagnosis"
        if kind:
            cases.append({"id": row["id"], "issue": kind, "priority": priorities[kind],
                          "cefr": row["cefr"], "task_family": row["task_family"],
                          "error_category": row.get("provisional_error_type") or "unspecified",
                          "expected_provisional": expected, "predicted": predicted,
                          "prompt": row["objective"], "learner_answer": row["learner_answer"],
                          "reference_answer": row["exercise"]["answer"],
                          "predicted_error_types": sorted({e.get("type") for e in result.get("errors", []) if isinstance(e, dict) and e.get("type")}),
                          "evaluation_status": result.get("evaluation_status"),
                          "review_required": True})
    cases.sort(key=lambda item: (item["priority"], item["cefr"], item["id"]))
    grouped = Counter((case["cefr"], case["error_category"], case["issue"]) for case in cases)
    return {"total": len(rows), "triaged": len(cases),
            "by_level_category": [{"cefr": level, "category": category, "issue": issue, "count": count}
                                  for (level, category, issue), count in sorted(grouped.items())],
            "by_issue": dict(sorted(Counter(case["issue"] for case in cases).items())),
            "cases": cases, "independently_validated": False, "release_gate": "blocked"}


def compare_triage(current, baseline):
    """Compare two same-case-set reports; do not infer linguistic accuracy."""
    current_cases = {case["id"]: case for case in current["cases"]}
    baseline_cases = {case["id"]: case for case in baseline["cases"]}
    current_total = current.get("total")
    if current_total != baseline.get("total"):
        raise ValueError("Benchmark sizes differ; comparison would be misleading")
    changed = []
    for identifier in sorted(set(current_cases) | set(baseline_cases)):
        before = baseline_cases.get(identifier)
        after = current_cases.get(identifier)
        if before != after:
            changed.append({"id": identifier,
                            "before_issue": before["issue"] if before else None,
                            "after_issue": after["issue"] if after else None,
                            "cefr": (after or before)["cefr"],
                            "category": (after or before)["error_category"]})
    return {"cases_compared": current_total, "changed": changed,
            "changed_count": len(changed), "independently_validated": False,
            "warning": "Differences are against provisional labels, not verified accuracy."}


def main():
    report = audit()
    triage_report = triage()
    triage_path = Path(__file__).resolve().parent / "fixtures" / "evaluation_v88_triage.json"
    triage_path.parent.mkdir(parents=True, exist_ok=True)
    triage_path.write_text(json.dumps(triage_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    path = Path(__file__).resolve().parent / "fixtures" / "evaluation_v88_curated_audit.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in {"provisional_error_outcomes", "structural_issues"}}, indent=2))
    print(json.dumps({"triaged": triage_report["triaged"], "by_issue": triage_report["by_issue"], "by_level_category": triage_report["by_level_category"]}, ensure_ascii=False, indent=2))
    if report["structural_issue_count"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
