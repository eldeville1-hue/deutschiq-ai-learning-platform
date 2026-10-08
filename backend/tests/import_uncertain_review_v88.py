"""Create a safe review handoff from the v88 uncertain-case packet.

This validates reviewer CSV rows against the exact selected development cases.
It never approves reviewer independence, changes evaluator logic, or unblocks release.
"""
import json
import sys
from pathlib import Path

from tests.export_uncertain_review_v88 import select_uncertain
from tests.review_evaluation_benchmark import import_reviews, review_progress


def import_uncertain(packet_path, output_path, manifest_path=None, rows=None):
    selected, expected = select_uncertain(rows)
    if manifest_path is not None:
        manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        if (manifest.get("case_ids") != expected["case_ids"]
                or manifest.get("source") != expected["source"]
                or manifest.get("independent_holdout") is not False
                or manifest.get("release_gate") != "blocked"):
            raise ValueError("Review manifest does not match current uncertain development cases")
    output = import_reviews(packet_path, output_path, rows=selected)
    imported = [json.loads(line) for line in Path(output).read_text(encoding="utf-8").splitlines() if line.strip()]
    progress = review_progress(imported)
    progress["source"] = "curated_development_unreviewed"
    progress["independent_holdout"] = False
    progress["release_gate"] = "blocked"
    progress["imported_review_count"] = sum(
        (row.get("human_review") or {}).get("status") == "pending_independence_verification"
        for row in imported
    )
    return progress


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        raise SystemExit("Usage: python -m tests.import_uncertain_review_v88 COMPLETED.csv OUTPUT.jsonl [MANIFEST.json]")
    print(json.dumps(import_uncertain(sys.argv[1], sys.argv[2],
                                       sys.argv[3] if len(sys.argv) == 4 else None),
                     ensure_ascii=False, indent=2))
