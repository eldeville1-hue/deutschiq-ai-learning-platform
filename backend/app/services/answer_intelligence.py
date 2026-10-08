"""Deterministic answer evaluation used when AI feedback is unavailable or unnecessary."""
from difflib import SequenceMatcher
from collections import Counter
import re
import unicodedata


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold().replace("ß", "ss")
    # Listening options are localized. Preserve Unicode letters, including
    # Cyrillic, so distinct Russian answers cannot collapse to empty strings.
    value = re.sub(r"[\W_]+", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def word_diff(answer: str, model: str) -> dict:
    actual, expected = normalize_text(answer).split(), normalize_text(model).split()
    missing = list((Counter(expected) - Counter(actual)).elements())
    extra = list((Counter(actual) - Counter(expected)).elements())
    return {"missing": missing[:5], "extra": extra[:5]}


def _legacy_evaluate_structured_answer(answer: str, exercise: dict) -> dict:
    accepted = [str(item) for item in (exercise.get("accepted_answers") or [exercise.get("answer", "")]) if str(item).strip()]
    normalized = normalize_text(answer)
    comparisons = [(model, SequenceMatcher(None, normalized, normalize_text(model)).ratio()) for model in accepted]
    model, similarity = max(comparisons, key=lambda item: item[1], default=("", 0.0))
    exact = bool(normalized) and normalized == normalize_text(model)
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


def _classify_aligned_errors(answer: str, model: str, target_feature: str = "") -> list:
    """High-precision token differences; do not infer grammar from similarity alone."""
    from app.services.evaluation_contract import LinguisticError
    actual = normalize_text(answer).split()
    expected = normalize_text(model).split()
    if len(actual) != len(expected):
        if target_feature == "infinitive" and expected.count("zu") == actual.count("zu") + 1 and Counter(expected) - Counter(actual) == Counter({"zu": 1}) and not (Counter(actual) - Counter(expected)):
            return [LinguisticError(type="infinitive", span=answer, correction=model, explanation="The infinitive construction requires zu.")]
        return []
    article_forms = {"ein", "eine", "einen", "einem", "einer", "eines", "der", "die", "das", "den", "dem", "des"}
    negations = {"nicht", "kein", "keine", "keinen", "keinem", "keiner", "keines"}
    errors = []
    if actual != expected and Counter(actual) == Counter(expected):
        return [LinguisticError(type="word_order", span=answer, correction=model,
                                explanation="Check the required word order.")]
    prepositions = {"auf", "an", "in", "mit", "für", "um", "über", "von", "zu", "nach", "bei", "aus", "durch", "gegen", "ohne"}
    auxiliaries = {"bin", "bist", "ist", "sind", "seid", "habe", "hast", "hat", "haben", "habt"}
    for got, want in zip(actual, expected):
        if got == want:
            continue
        if got in negations or want in negations:
            kind = "negation"
            explanation = "The negation changes the meaning or required form."
        elif got in auxiliaries and want in auxiliaries:
            kind = "auxiliary"
            explanation = "Check the auxiliary verb."
        elif got in prepositions and want in prepositions:
            kind = "preposition"
            explanation = "Check the required preposition."
        elif got in article_forms and want in article_forms:
            kind = target_feature if target_feature in {"case", "relative_pronoun"} else "article"
            explanation = "Check the article and its case or gender ending."
        elif target_feature == "participle" and got.endswith("en") and want.endswith("t"):
            kind = "participle"
            explanation = "Check the past participle form."
        elif got.endswith("en") and want.endswith("e") and got[:-2] == want[:-1]:
            kind = "conjugation"
            explanation = "The verb ending does not match the required subject."
        else:
            kind = "vocabulary"
            explanation = "This word differs from the expected wording; verify its meaning."
        errors.append(LinguisticError(type=kind, span=got, correction=want, explanation=explanation))
    return errors


def evaluate_structured_answer(answer: str, exercise: dict) -> dict:
    """Conservative objective-aware comparison; unsupported open responses need review."""
    from app.services.evaluation_contract import EvaluationResult, LinguisticError
    legacy = _legacy_evaluate_structured_answer(answer, exercise)
    accepted = [str(x) for x in (exercise.get("accepted_answers") or [exercise.get("answer", "")]) if str(x).strip()]
    exact = bool(normalize_text(answer)) and any(normalize_text(answer) == normalize_text(x) for x in accepted)
    # Authored alternatives are the only safe deterministic equivalences.
    # Do not infer semantic equivalence from string similarity.
    closed_types = {"reorder", "error_repair", "analogy_choice", "context_choice", "listening_choice", "choice"}
    accepted_normalized = {normalize_text(item) for item in accepted}
    exact = bool(normalize_text(answer)) and normalize_text(answer) in accepted_normalized
    # A swapped article/negation can look like a minor typo in a long sentence.
    # Require every spelling tolerance to be non-semantic.
    if legacy["correct"] and not exact:
        model_words = normalize_text(legacy["model"]).split()
        answer_words = normalize_text(answer).split()
        semantic_tokens = {"nicht", "kein", "keine", "keinen", "keinem", "keiner", "keines",
                           "ein", "eine", "einen", "einem", "einer", "eines",
                           "der", "die", "das", "den", "dem", "des"}
        changes = [(a, b) for a, b in zip(answer_words, model_words) if a != b]
        if any(a in semantic_tokens or b in semantic_tokens for a, b in changes):
            legacy["correct"] = False
            legacy["error_type"] = "answer_mismatch"
    open_ended = exercise.get("type") in {"translation", "translate", "free_text", "sentence", "writing"}
    status = ("needs_review" if not accepted else "verified" if legacy["correct"] or not open_ended else "uncertain")
    errors = []
    if legacy["correct"] and not exact:
        errors = [LinguisticError(
            type="spelling", span=answer, correction=legacy["model"],
            explanation="Check the spelling against the model answer.",
        )]
    elif status == "verified" and not legacy["correct"]:
        errors = _classify_aligned_errors(answer, legacy["model"], exercise.get("target_feature", ""))
        if not errors:
            errors = [LinguisticError(
                type=legacy["error_type"] or "answer_mismatch", span=answer,
                correction=legacy["model"],
                explanation="This response does not match the exercise requirement.",
            )]
    elif status == "uncertain":
        # These are candidate differences, not confirmed linguistic mistakes.
        candidates = _classify_aligned_errors(answer, legacy["model"], exercise.get("target_feature", ""))
        errors = [item for item in candidates if item.type in {"article", "negation", "auxiliary", "preposition", "conjugation"}]
    result = EvaluationResult(
        grammar_correct=True if exact else None,
        meaning_correct=True if exact else None,
        task_satisfied=bool(legacy["correct"]) if status == "verified" else None,
        correct=bool(legacy["correct"]) and status == "verified",
        evaluation_status=status,
        errors=errors,
        error_type=errors[0].type if errors else None,
    )
    return {
        **legacy, **result.to_dict(),
        "score": legacy["score"] if status == "verified" else 0,
        "legacy_error_type": legacy["error_type"],
        "review_reason": ("open_answer_not_proven_equivalent_or_incorrect" if status == "uncertain" else
                          "missing_reference_answer" if status == "needs_review" else None),
        "candidate_error_types": ([item.type for item in errors] if status == "uncertain" else []),
    }
