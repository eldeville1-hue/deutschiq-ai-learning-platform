"""Deterministic answer evaluation used when AI feedback is unavailable or unnecessary."""
from difflib import SequenceMatcher
from collections import Counter
import re
import unicodedata


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold().replace("ß", "ss")
    value = re.sub(r"[^a-z0-9äöü\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def word_diff(answer: str, model: str) -> dict:
    actual, expected = normalize_text(answer).split(), normalize_text(model).split()
    missing = list((Counter(expected) - Counter(actual)).elements())
    extra = list((Counter(actual) - Counter(expected)).elements())
    return {"missing": missing[:5], "extra": extra[:5]}


def evaluate_structured_answer(answer: str, exercise: dict) -> dict:
    accepted = [str(item) for item in (exercise.get("accepted_answers") or [exercise.get("answer", "")]) if str(item).strip()]
    normalized = normalize_text(answer)
    comparisons = [(model, SequenceMatcher(None, normalized, normalize_text(model)).ratio()) for model in accepted]
    model, similarity = max(comparisons, key=lambda item: item[1], default=("", 0.0))
    exact = normalized == normalize_text(model)
    actual_words, model_words = normalized.split(), normalize_text(model).split()
    changed = [(actual, expected) for actual, expected in zip(actual_words, model_words) if actual != expected]
    # Selection and token-building tasks have no typing errors. For typed
    # answers, allow one omitted internal letter in a long word. A global
    # similarity threshold alone also accepts changed articles and verb forms.
    minor_spelling = (
        exercise.get("type") not in {"reorder", "error_repair", "analogy_choice", "context_choice", "listening_choice", "choice"}
        and len(actual_words) == len(model_words)
        and len(changed) == 1
        and similarity >= 0.93
        and all(len(expected) >= 7 and len(actual) == len(expected) - 1
                and any(actual == expected[:index] + expected[index + 1:]
                        for index in range(2, len(expected) - 1))
                for actual, expected in changed)
    )
    correct = exact or minor_spelling
    diff = word_diff(answer, model)
    error_type = None if correct else (exercise.get("misconception") or ("missing_words" if diff["missing"] else "answer_mismatch"))
    return {"correct": correct, "score": 100 if exact else 90 if minor_spelling else round(similarity * 100), "model": model, "similarity": round(similarity * 100), "missing_words": diff["missing"], "extra_words": diff["extra"], "error_type": error_type}
