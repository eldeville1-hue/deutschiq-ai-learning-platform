"""Deterministic answer evaluation used when AI feedback is unavailable or unnecessary."""
from difflib import SequenceMatcher
import re
import unicodedata


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold().replace("ß", "ss")
    value = re.sub(r"[^a-z0-9äöü\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def word_diff(answer: str, model: str) -> dict:
    actual, expected = normalize_text(answer).split(), normalize_text(model).split()
    missing = [word for word in expected if word not in actual]
    extra = [word for word in actual if word not in expected]
    return {"missing": missing[:5], "extra": extra[:5]}


def evaluate_structured_answer(answer: str, exercise: dict) -> dict:
    accepted = [str(item) for item in (exercise.get("accepted_answers") or [exercise.get("answer", "")]) if str(item).strip()]
    normalized = normalize_text(answer)
    comparisons = [(model, SequenceMatcher(None, normalized, normalize_text(model)).ratio()) for model in accepted]
    model, similarity = max(comparisons, key=lambda item: item[1], default=("", 0.0))
    exact = normalized == normalize_text(model)
    same_word_count = len(normalized.split()) == len(normalize_text(model).split())
    # A very close answer with the same token count is treated as a harmless
    # spelling variation. Word-order and missing-word mistakes still fail.
    minor_spelling = same_word_count and similarity >= 0.93
    correct = exact or minor_spelling
    diff = word_diff(answer, model)
    error_type = None if correct else (exercise.get("misconception") or ("missing_words" if diff["missing"] else "answer_mismatch"))
    return {"correct": correct, "score": 100 if exact else 90 if minor_spelling else round(similarity * 100), "model": model, "similarity": round(similarity * 100), "missing_words": diff["missing"], "extra_words": diff["extra"], "error_type": error_type}
