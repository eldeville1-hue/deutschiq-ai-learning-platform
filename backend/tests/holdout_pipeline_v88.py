"""External independent holdout ingestion and fail-closed v88 validation.

No examples or approvals are fabricated. Reviewer independence requires external verification.
Run from backend/: python -m tests.holdout_pipeline_v88 validate HOLDOUT.jsonl
"""
import json
import sys
from pathlib import Path
from difflib import SequenceMatcher

from tests.generate_curated_evaluation_v88 import build_diverse_cases
from tests.run_evaluation_benchmark import validation_report, _fingerprint


REQUIRED = ("id", "cefr", "objective", "exercise", "learner_answer", "source", "split", "human_review")


def load_holdout(path):
    rows = []
    for line_no, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON at line {line_no}: {exc}") from exc
        if not isinstance(row, dict) or any(k not in row for k in REQUIRED):
            raise ValueError(f"Missing required fields at line {line_no}")
        rows.append(row)
    return rows


def check_holdout(holdout, development=None):
    development = build_diverse_cases() if development is None else development
    errors = []
    seen_ids = {r["id"] for r in development}
    seen_content = {(_fingerprint(r["exercise"].get("answer", "")),
                     _fingerprint(r["objective"]), _fingerprint(r["learner_answer"]))
                    for r in development}
    development_answers = [(_fingerprint(r["exercise"].get("answer", "")), r["id"]) for r in development]
    holdout_answers = []
    for index, row in enumerate(holdout):
        identifier = row.get("id", f"row-{index}")
        if not all(k in row for k in REQUIRED):
            errors.append(f"{identifier}:missing_fields")
            continue
        if identifier in seen_ids:
            errors.append(f"{identifier}:duplicate_id")
        seen_ids.add(identifier)
        if row["cefr"] not in ("A1", "A2", "B1", "B2"):
            errors.append(f"{identifier}:invalid_level")
        if row["split"] != "holdout":
            errors.append(f"{identifier}:not_holdout")
        if not isinstance(row["exercise"], dict) or not row["exercise"].get("answer"):
            errors.append(f"{identifier}:invalid_exercise")
            continue
        key = (_fingerprint(row["exercise"]["answer"]),
               _fingerprint(row["objective"]), _fingerprint(row["learner_answer"]))
        if key in seen_content:
            errors.append(f"{identifier}:duplicate_content")
        seen_content.add(key)
        answer = key[0]
        for other_answer, other_id in development_answers + holdout_answers:
            if answer and other_answer and answer != other_answer and (
                    SequenceMatcher(None, answer, other_answer).ratio() >= 0.90):
                errors.append(f"{identifier}:near_duplicate_answer:{other_id}")
        holdout_answers.append((answer, identifier))
        source = str(row.get("source", ""))
        if not source or source.startswith(("synthetic", "curated_author_written")):
            errors.append(f"{identifier}:unverified_source")
        review = row.get("human_review")
        if not isinstance(review, dict):
            errors.append(f"{identifier}:invalid_review")
        elif review.get("status") not in ("pending", "pending_independence_verification", "approved"):
            errors.append(f"{identifier}:invalid_review_status")
        elif review.get("status") == "approved":
            required_review = ("reviewer", "reviewed_at", "protocol_version",
                               "decision", "blind_to_prediction", "independent_of_generation")
            if any(not review.get(field) for field in required_review):
                errors.append(f"{identifier}:approved_review_missing_provenance")
            if review.get("blind_to_prediction") is not True or review.get("independent_of_generation") is not True:
                errors.append(f"{identifier}:review_independence_not_verified")
            if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
                errors.append(f"{identifier}:invalid_reviewer_identity")
            timestamp = review.get("reviewed_at")
            if not isinstance(timestamp, str) or not timestamp.strip():
                errors.append(f"{identifier}:invalid_review_timestamp")
            else:
                from datetime import datetime, timezone
                try:
                    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    if parsed.tzinfo is None or parsed.utcoffset() is None or parsed > datetime.now(timezone.utc):
                        errors.append(f"{identifier}:invalid_review_timestamp")
                except ValueError:
                    errors.append(f"{identifier}:invalid_review_timestamp")
            if not isinstance(review.get("protocol_version"), str) or not review["protocol_version"].strip():
                errors.append(f"{identifier}:invalid_review_protocol")
            if review.get("decision") not in ("correct", "incorrect", "uncertain"):
                errors.append(f"{identifier}:invalid_review_decision")
            if review.get("decision") == "incorrect" and not review.get("error_types"):
                errors.append(f"{identifier}:missing_error_diagnosis")
            if review.get("decision") == "uncertain" and not str(review.get("notes", "")).strip():
                errors.append(f"{identifier}:uncertain_review_without_notes")
    return sorted(set(errors))


def evaluate_file(path):
    holdout = load_holdout(path)
    errors = check_holdout(holdout)
    # Run metrics only on validated input; the release gate remains fail-closed.
    if errors:
        return {"release_gate": "blocked", "holdout_total": len(holdout),
                "ingestion_errors": errors, "failed_gates": ["holdout_ingestion"]}
    pending = [row["id"] for row in holdout if row["human_review"]["status"] != "approved"]
    if pending:
        return {"release_gate": "blocked", "holdout_total": len(holdout),
                "approved_total": len(holdout) - len(pending),
                "pending_review_total": len(pending), "pending_review_examples": pending[:20],
                "ingestion_errors": [], "failed_gates": ["holdout_reviews_incomplete"]}
    report = validation_report(holdout)
    report["ingestion_errors"] = []
    return report


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "validate":
        raise SystemExit("Usage: python -m tests.holdout_pipeline_v88 validate <holdout.jsonl>")
    try:
        report = evaluate_file(sys.argv[2])
    except (ValueError, OSError, KeyError, TypeError) as exc:
        report = {"release_gate": "blocked", "ingestion_errors": [str(exc)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["release_gate"] != "approved":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
