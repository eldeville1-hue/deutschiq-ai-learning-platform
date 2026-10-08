"""DeutschIQ 88 release benchmark: reviewed labels only, fail closed."""
import json
import time
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from app.services.answer_intelligence import evaluate_structured_answer
from tests.generate_evaluation_benchmark import build_cases

LEVELS = ("A1", "A2", "B1", "B2")
ACCURACY_MIN = 0.95
COVERAGE_MIN = 0.95
DIAGNOSIS_PRECISION_MIN = 0.90
DIAGNOSIS_RECALL_MIN = 0.90
MIN_PER_LEVEL = 100
MAX_DETERMINISTIC_P95_MS = 200

def _ratio(a, b):
    return round(a / b, 4) if b else None

def _percentile(values, percentile):
    if not values:
        return None
    values = sorted(values)
    return round(values[max(0, min(len(values) - 1, int((len(values) - 1) * percentile + 0.9999)))], 3)

def _split_key(row):
    return row.get("split", "unassigned")

def _fingerprint(text):
    from app.services.answer_intelligence import normalize_text
    return normalize_text(text)

def run(rows, evaluator=evaluate_structured_answer):
    groups = defaultdict(list)
    pending = 0
    synthetic = Counter()
    duplicates = defaultdict(set)
    leakage = set()
    split_examples = defaultdict(list)
    suspected = []
    for row in rows:
        # No identical model-answer + prompt pair may cross evaluation splits.
        key = (_fingerprint(row["exercise"].get("answer", "")), _fingerprint(row.get("objective", "")))
        split = _split_key(row)
        if duplicates[key] and split not in duplicates[key]:
            leakage.add(key)
        duplicates[key].add(split)
        signature = _fingerprint(row["exercise"].get("answer", ""))
        for other_split, examples in split_examples.items():
            if other_split == split:
                continue
            for prior_id, prior_signature in examples:
                if signature and SequenceMatcher(None, signature, prior_signature).ratio() >= 0.90:
                    suspected.append((prior_id, row.get("id", "")))
        split_examples[split].append((row.get("id", ""), signature))
        if row.get("source", "").startswith("synthetic"):
            expected = row.get("provisional_expected")
            if expected in {"correct", "incorrect"}:
                prediction = evaluator(row["learner_answer"], row["exercise"])
                actual = ("uncertain" if prediction["evaluation_status"] != "verified"
                          else "correct" if prediction["correct"] else "incorrect")
                synthetic[(expected, actual)] += 1
        review = row.get("human_review", {})
        if review.get("status") != "approved" or review.get("decision") not in {"correct", "incorrect", "uncertain"} or not review.get("reviewer"):
            pending += 1
            continue
        start = time.perf_counter()
        result = evaluator(row["learner_answer"], row["exercise"])
        elapsed = (time.perf_counter() - start) * 1000
        predicted = ("uncertain" if result["evaluation_status"] != "verified" else
                     "correct" if result["correct"] else "incorrect")
        expected_errors = set(review.get("error_types") or [])
        predicted_errors = {x["type"] for x in result.get("errors", [])} if predicted == "incorrect" else set()
        groups[row["cefr"]].append((review["decision"], predicted, expected_errors, predicted_errors, elapsed))
    report = {"total": len(rows), "reviewed": sum(map(len, groups.values())),
              "pending": pending, "synthetic_provisional_agreement": _ratio(sum(n for (expected, actual), n in synthetic.items() if expected == actual), sum(synthetic.values())), "synthetic_confusion": {f"{a}->{b}": n for (a, b), n in sorted(synthetic.items())}, "cross_split_leakage": len(leakage), "suspected_near_duplicates": suspected[:100], "levels": {}, "release_gate": "blocked"}
    failures = []
    if pending:
        failures.append("unreviewed_cases")
    if leakage:
        failures.append("cross_split_leakage")
    if suspected:
        failures.append("suspected_cross_split_similarity")
    for level in LEVELS:
        samples = groups[level]
        n = len(samples)
        definitive = sum(pred != "uncertain" for _, pred, _, _, _ in samples)
        matrix = Counter((actual, predicted) for actual, predicted, _, _, _ in samples)
        true_positive = sum(len(expected & predicted) for _, _, expected, predicted, _ in samples)
        false_positive_errors = sum(len(predicted - expected) for _, _, expected, predicted, _ in samples)
        false_negative_errors = sum(len(expected - predicted) for _, _, expected, predicted, _ in samples)
        accuracy = _ratio(sum(a == b for a, b, _, _, _ in samples), n)
        coverage = _ratio(definitive, n)
        precision = _ratio(true_positive, true_positive + false_positive_errors)
        recall = _ratio(true_positive, true_positive + false_negative_errors)
        latency = _percentile([ms for *_, ms in samples], 0.95)
        report["levels"][level] = {
            "reviewed": n, "accuracy": accuracy, "coverage": coverage,
            "false_positive": sum(a != "correct" and b == "correct" for a, b, _, _, _ in samples),
            "false_negative": sum(a == "correct" and b == "incorrect" for a, b, _, _, _ in samples),
            "review_deferrals": n - definitive, "diagnosis_precision": precision,
            "diagnosis_recall": recall, "diagnosis_tp": true_positive,
            "diagnosis_fp": false_positive_errors, "diagnosis_fn": false_negative_errors,
            "deterministic_p95_ms": latency,
            "confusion_matrix": {f"{a}->{b}": count for (a, b), count in sorted(matrix.items())},
        }
        if n < MIN_PER_LEVEL:
            failures.append(f"{level}:insufficient_reviews")
        if accuracy is None or accuracy < ACCURACY_MIN:
            failures.append(f"{level}:accuracy")
        if coverage is None or coverage < COVERAGE_MIN:
            failures.append(f"{level}:coverage")
        if precision is None or precision < DIAGNOSIS_PRECISION_MIN:
            failures.append(f"{level}:diagnosis_precision")
        if recall is None or recall < DIAGNOSIS_RECALL_MIN:
            failures.append(f"{level}:diagnosis_recall")
        if latency is None or latency >= MAX_DETERMINISTIC_P95_MS:
            failures.append(f"{level}:deterministic_latency")
    report["failed_gates"] = failures
    report["validation_type"] = "synthetic_provisional_not_independently_validated"
    report["independent_accuracy_demonstrated"] = False
    # Passing metrics is not a substitute for independent human sign-off,
    # frontend/mobile E2E, AI-assisted latency or a production smoke test.
    report["release_gate"] = "blocked" if failures else "requires_manual_signoff"
    return report

def main():
    fixture = Path(__file__).resolve().parent / "fixtures" / "evaluation_v88_synthetic.jsonl"
    rows = [json.loads(line) for line in fixture.read_text(encoding="utf-8").splitlines()] if fixture.exists() else build_cases()
    report = run(rows)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["release_gate"] == "blocked":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
