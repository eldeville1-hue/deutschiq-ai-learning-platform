"""Blind human-review packet for DeutschIQ 88.

Export: python -m tests.review_evaluation_benchmark export
Import: python -m tests.review_evaluation_benchmark import reviews.csv

The exported packet never includes model predictions or provisional labels.
A reviewer must fill decisions and error types personally; this tool never
manufactures approvals or claims reviewer independence.
"""
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from tests.generate_evaluation_benchmark import build_cases
from tests.linguistic_challenge_suite import build_challenges
from tests.generate_curated_evaluation_v88 import build_diverse_cases as build_curated_cases

ROOT = Path(__file__).resolve().parent / "fixtures"
FIELDS = ("id", "cefr", "objective", "exercise_type", "model_answer",
          "learner_answer", "decision", "error_types", "reviewer", "notes")
DECISIONS = {"correct", "incorrect", "uncertain"}

def export_packet(path, rows=None):
    rows = build_cases() if rows is None else rows
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "id": row["id"], "cefr": row["cefr"],
                "objective": row["objective"],
                "exercise_type": row["exercise"].get("type", ""),
                "model_answer": row["exercise"].get("answer", ""),
                "learner_answer": row["learner_answer"],
                "decision": "", "error_types": "", "reviewer": "", "notes": "",
            })
    return path

def import_reviews(packet, output, rows=None):
    rows = build_cases() if rows is None else rows
    indexed = {row["id"]: row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError("Duplicate benchmark IDs")
    with Path(packet).open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not set(FIELDS).issubset(reader.fieldnames or []):
            raise ValueError("Review CSV is missing required columns")
        seen = set()
        for record in reader:
            identifier = record["id"]
            if identifier not in indexed or identifier in seen:
                raise ValueError("Unknown or duplicate review ID: " + identifier)
            seen.add(identifier)
            original = indexed[identifier]
            # Prevent a modified review packet from silently changing the case.
            expected = (original["cefr"], original["objective"],
                        original["exercise"].get("type", ""),
                        original["exercise"].get("answer", ""),
                        original["learner_answer"])
            actual = tuple(record[field] for field in
                           ("cefr", "objective", "exercise_type", "model_answer", "learner_answer"))
            if actual != expected:
                raise ValueError("Benchmark content changed for " + identifier)
            decision = record["decision"].strip().lower()
            reviewer = record["reviewer"].strip()
            if not decision and not reviewer:
                continue
            if decision not in DECISIONS or not reviewer:
                raise ValueError("Incomplete or invalid review: " + identifier)
            error_types = [x.strip() for x in record["error_types"].split(";") if x.strip()]
            if decision == "incorrect" and not error_types:
                raise ValueError("Incorrect review needs at least one diagnosed error: " + identifier)
            if decision == "correct" and error_types:
                raise ValueError("Correct review cannot contain diagnosed errors: " + identifier)
            if decision == "uncertain" and not record["notes"].strip():
                raise ValueError("Uncertain review needs an explanation: " + identifier)
            original["human_review"] = {
                "status": "pending_independence_verification",
                "reviewer": reviewer, "decision": decision,
                "error_types": error_types,
                "notes": record["notes"], "reviewed_at": datetime.now(timezone.utc).isoformat(),
                "protocol_version": "v88-1",
                "blind_to_prediction": True,
                "independent_of_generation": False,
            }
        if seen != set(indexed):
            raise ValueError("Review packet does not cover every benchmark case")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    return output

def main():
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "export":
        print(export_packet(Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "evaluation_v88_review_packet.csv"))
    elif command == "export-curated":
        print(export_packet(Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "evaluation_v88_curated_review_packet.csv", rows=build_curated_cases()))
    elif command == "import-curated" and len(sys.argv) >= 3:
        print(import_reviews(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ROOT / "evaluation_v88_curated_reviewed.jsonl", rows=build_curated_cases()))
    elif command == "export-challenges":
        print(export_packet(Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "evaluation_v88_challenge_review_packet.csv", rows=build_challenges()))
    elif command == "import-challenges" and len(sys.argv) >= 3:
        print(import_reviews(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ROOT / "evaluation_v88_challenge_reviewed.jsonl", rows=build_challenges()))
    elif command == "import" and len(sys.argv) >= 3:
        print(import_reviews(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ROOT / "evaluation_v88_reviewed.jsonl"))
    else:
        raise SystemExit("Usage: python -m tests.review_evaluation_benchmark export [csv] | import <csv> [jsonl] | export-challenges [csv] | import-challenges <csv> [jsonl]")

if __name__ == "__main__":
    main()
