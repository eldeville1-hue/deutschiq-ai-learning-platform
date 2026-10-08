"""Benchmark runner. Human-reviewed accuracy is NEVER inferred from synthetic labels.

From backend/: python -m tests.run_evaluation_benchmark
"""
import json
from collections import Counter, defaultdict
from pathlib import Path
from app.services.answer_intelligence import evaluate_structured_answer
from tests.generate_evaluation_benchmark import build_cases

def run(rows):
    groups = defaultdict(list)
    pending = 0
    for row in rows:
        review = row.get("human_review", {})
        if review.get("status") != "approved" or review.get("decision") not in {"correct", "incorrect", "uncertain"}:
            pending += 1
            continue
        result = evaluate_structured_answer(row["learner_answer"], row["exercise"])
        predicted = ("uncertain" if result["evaluation_status"] != "verified" else
                     "correct" if result["correct"] else "incorrect")
        groups[row["cefr"]].append((review["decision"], predicted))
    report = {"total": len(rows), "reviewed": sum(map(len, groups.values())), "pending": pending, "levels": {}}
    for level in ("A1", "A2", "B1", "B2"):
        pairs = groups[level]
        matrix = Counter((actual, predicted) for actual, predicted in pairs)
        n = len(pairs)
        report["levels"][level] = {
            "reviewed": n,
            "accuracy": round(sum(a == b for a, b in pairs) / n, 4) if n else None,
            "false_positive": sum(a != "correct" and b == "correct" for a, b in pairs),
            "false_negative": sum(a == "correct" and b == "incorrect" for a, b in pairs),
            "review_deferrals": sum(b == "uncertain" for _, b in pairs),
            "confusion_matrix": {f"{a}->{b}": count for (a, b), count in sorted(matrix.items())},
        }
    report["release_gate"] = "blocked" if pending or any(report["levels"][level]["reviewed"] < 100 for level in report["levels"]) else "requires_manual_signoff"
    return report

def main():
    fixture = Path(__file__).resolve().parent / "fixtures" / "evaluation_v88_synthetic.jsonl"
    rows = [json.loads(line) for line in fixture.read_text(encoding="utf-8").splitlines()] if fixture.exists() else build_cases()
    report = run(rows)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["release_gate"] == "blocked":
        print("RELEASE BLOCKED: human-reviewed dataset insufficient.")
        raise SystemExit(2)

if __name__ == "__main__":
    main()
