"""Read-only intake summary for external v88 holdout; never grants release approval."""
import json
import sys
from collections import Counter
from pathlib import Path

from tests.holdout_pipeline_v88 import check_holdout, load_holdout

LEVELS = ("A1", "A2", "B1", "B2")
TARGET = 100


def summarize(rows, validator=check_holdout):
    levels = Counter(row.get("cefr") for row in rows)
    statuses = Counter(
        (row.get("human_review") or {}).get("status", "missing")
        if isinstance(row.get("human_review"), dict) else "invalid"
        for row in rows
    )
    errors = validator(rows)
    per_level = {}
    for level in LEVELS:
        subset = [row for row in rows if row.get("cefr") == level]
        status_counts = Counter(
            row.get("human_review", {}).get("status", "missing")
            if isinstance(row.get("human_review"), dict) else "invalid"
            for row in subset
        )
        per_level[level] = {
            "received": levels[level],
            "target": TARGET,
            "remaining": max(0, TARGET - levels[level]),
            "awaiting_linguistic_review": status_counts["pending"],
            "awaiting_independence_verification": status_counts["pending_independence_verification"],
            "claimed_approved": status_counts["approved"],
            "invalid_or_missing_review": sum(
                count for status, count in status_counts.items()
                if status not in ("pending", "pending_independence_verification", "approved")
            ),
        }
    coordinator_actions = []
    for level in LEVELS:
        item = per_level[level]
        if item["remaining"]:
            coordinator_actions.append({"cefr": level, "action": "collect_external_cases",
                                        "count": item["remaining"]})
        if item["awaiting_linguistic_review"]:
            coordinator_actions.append({"cefr": level, "action": "request_blind_linguistic_review",
                                        "count": item["awaiting_linguistic_review"]})
        if item["awaiting_independence_verification"]:
            coordinator_actions.append({"cefr": level, "action": "verify_reviewer_independence_externally",
                                        "count": item["awaiting_independence_verification"]})
        if item["invalid_or_missing_review"]:
            coordinator_actions.append({"cefr": level, "action": "repair_review_metadata",
                                        "count": item["invalid_or_missing_review"]})
    return {
        "coordinator_actions": coordinator_actions,
        "purpose": "external_holdout_intake_only",
        "total": len(rows),
        "levels": per_level,
        "review_status_counts": dict(sorted(statuses.items())),
        "ingestion_error_count": len(errors),
        "ingestion_errors": errors[:50],
        "collection_target_met": all(levels[level] >= TARGET for level in LEVELS),
        "intake_structurally_valid": not errors,
        "independence_externally_verified": False,
        "release_gate": "blocked",
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m tests.holdout_intake_report_v88 HOLDOUT.jsonl")
    try:
        report = summarize(load_holdout(Path(sys.argv[1])))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report = {"release_gate": "blocked", "ingestion_errors": [str(exc)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report.get("ingestion_errors") or not report.get("collection_target_met"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
