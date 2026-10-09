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


def _semantic_punctuation_conflict(answer: str, reference: str) -> bool:
    """Avoid auto-accepting a missing vocative comma that changes who is eaten."""
    if not isinstance(answer, str) or not isinstance(reference, str):
        return False
    # Only flag the unambiguous high-risk pattern: direct address of a person
    # following a verb with a comma in one version but not the other.
    vocatives = {"opa", "oma", "mama", "papa", "mutter", "vater"}
    tokens = normalize_text(reference).split()
    if len(tokens) < 3 or tokens[-1] not in vocatives:
        return False
    def comma_before_vocative(value: str) -> bool:
        return bool(re.search(r",\\s*" + re.escape(tokens[-1]) + r"\\s*[.!?]*$", value, re.IGNORECASE))
    return normalize_text(answer) == normalize_text(reference) and comma_before_vocative(answer) != comma_before_vocative(reference)


def _accepted_models(exercise: dict) -> list[str]:
    """Return only authored text answers; malformed alternatives cannot grant credit."""
    alternatives = exercise.get("accepted_answers")
    if not isinstance(alternatives, (list, tuple)):
        alternatives = []
    candidates = [exercise.get("answer"), *alternatives]
    return [value for value in candidates if isinstance(value, str) and normalize_text(value)]


def _legacy_evaluate_structured_answer(answer: str, exercise: dict) -> dict:
    accepted = _accepted_models(exercise)
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


def _classify_aligned_errors(answer: str, model: str, target_feature: str = "", exercise_type: str = "") -> list:
    """High-precision token differences; do not infer grammar from similarity alone."""
    from app.services.evaluation_contract import LinguisticError
    actual = normalize_text(answer).split()
    expected = normalize_text(model).split()
    if len(actual) != len(expected):
        # Only diagnose a missing infinitive marker when its placement is
        # unambiguous; equal word bags alone would lose word-order evidence.
        if target_feature == "infinitive" and len(expected) == len(actual) + 1:
            missing_positions = [
                i for i in range(len(expected))
                if expected[i] == "zu" and expected[:i] + expected[i + 1:] == actual
            ]
            if len(missing_positions) == 1:
                return [LinguisticError(type="infinitive", span=answer, correction=model,
                                        explanation="The infinitive construction requires zu.")]
        return []
    article_forms = {"ein", "eine", "einen", "einem", "einer", "eines", "der", "die", "das", "den", "dem", "des"}
    negations = {"nicht", "kein", "keine", "keinen", "keinem", "keiner", "keines"}
    errors = []
    # A changed ending on kein is not necessarily a change in polarity.
    if target_feature in {"case", "article", "adjective"}:
        negation_forms = {"kein", "keine", "keinen", "keinem", "keiner", "keines"}
        differences = [(a, b) for a, b in zip(actual, expected) if a != b]
        if len(differences) == 1 and all(token in negation_forms for token in differences[0]):
            got, want = differences[0]
            return [LinguisticError(type=target_feature, span=got, correction=want,
                                    explanation="Check the grammatical ending of the negating determiner.")]
    if actual != expected and Counter(actual) == Counter(expected):
        # A permutation is not automatically a grammatical mistake in German.
        # Free word order can be valid, especially in translations and writing.
        if target_feature != "word_order" and exercise_type != "reorder":
            return []
        return [LinguisticError(type="word_order", span=answer, correction=model,
                                explanation="Check the word order required by this exercise.")]
    prepositions = {"auf", "an", "in", "mit", "für", "um", "über", "von", "zu", "nach", "bei", "aus", "durch", "gegen", "ohne"}
    auxiliaries = {"bin", "bist", "ist", "sind", "seid", "habe", "hast", "hat", "haben", "habt"}
    case_pronouns = {"ich", "mich", "mir", "du", "dich", "dir", "er", "ihn", "ihm", "sie", "ihr", "wir", "uns", "euch"}
    for got, want in zip(actual, expected):
        if got == want:
            continue
        if got in negations or want in negations:
            # Different kein-endings retain negative polarity. Without a
            # targeted case/article objective, avoid claiming polarity changed.
            kein_forms = {"kein", "keine", "keinen", "keinem", "keiner", "keines"}
            if got in kein_forms and want in kein_forms:
                kind = target_feature if target_feature in {"case", "article", "adjective"} else "answer_mismatch"
                explanation = ("Check the grammatical ending of the negating determiner."
                               if kind != "answer_mismatch" else
                               "The negating determiner has a different form; polarity is unchanged.")
            else:
                kind = "negation"
                explanation = "Check the negation and its effect on the intended meaning."
        elif got in auxiliaries and want in auxiliaries:
            kind = "conjugation" if target_feature == "conjugation" else "auxiliary"
            explanation = "Check the verb form for the required subject." if kind == "conjugation" else "Check the auxiliary verb."
        elif target_feature == "case" and got in case_pronouns and want in case_pronouns:
            kind = "case"
            explanation = "Check the pronoun case required by the verb or construction."
        elif target_feature == "preposition" and (got in prepositions or want in prepositions):
            kind = "preposition"
            explanation = "Check the preposition required by the construction."
        elif got in prepositions and want in prepositions:
            kind = "preposition"
            explanation = "Check the required preposition."
        elif target_feature == "conjugation" and got == "lesen" and want == "liest":
            kind = "conjugation"
            explanation = "Check the irregular third-person singular verb form."
        elif target_feature == "infinitive" and (
                (got, want) in {
                    ("aufgestanden", "aufstehen"), ("aufstehen", "aufzustehen"),
                    ("einbeziehen", "einzubeziehen")}
                or (want.startswith("zu") and got == want[2:] and len(got) > 3)):
            kind = "infinitive"
            explanation = "Check the infinitive form and placement of zu."
        elif target_feature == "passive" and (got, want) == ("gelöst", "lösen"):
            kind = "passive"
            explanation = "The construction with lässt sich requires an infinitive."
        elif target_feature == "possessive" and got in {
                "mein", "meine", "meinen", "meinem", "meiner", "meines",
                "dein", "deine", "deinen", "deinem", "deiner", "deines"} and want in {
                "mein", "meine", "meinen", "meinem", "meiner", "meines",
                "dein", "deine", "deinen", "deinem", "deiner", "deines"}:
            kind = "possessive"
            explanation = "Check the possessive determiner ending."
        elif target_feature == "case" and got in {
                "dieser", "diese", "dieses", "diesen", "diesem",
                "jener", "jene", "jenes", "jenen", "jenem"} and want in {
                "dieser", "diese", "dieses", "diesen", "diesem",
                "jener", "jene", "jenes", "jenen", "jenem"} and got[:3] == want[:3]:
            kind = "case"
            explanation = "Check the case and gender ending of the demonstrative determiner."
        elif target_feature == "case" and got in article_forms and want in article_forms:
            kind = "case"
            explanation = "Check the required case ending."
        elif target_feature == "preposition" and got in article_forms and want in article_forms:
            kind = "preposition"
            explanation = "Check the case required by the preposition."
        elif target_feature == "comparison" and (
                (got, want) in {("wie", "als"), ("als", "wie")} or
                (want == got + "er" and len(got) > 3)):
            kind = "comparison"
            explanation = "Check the comparative form or comparison particle."
        elif target_feature == "tense" and got != want:
            kind = "tense"
            explanation = "Check the tense required by the sentence."
        elif got in article_forms and want in article_forms:
            kind = target_feature if target_feature in {"case", "relative_pronoun"} else "article"
            explanation = "Check the article and its case or gender ending."
        elif target_feature == "subjunctive" and got != want:
            # A tagged correction is a targeted exercise, not a claim that
            # these verb forms are interchangeable in open-ended writing.
            kind = "subjunctive"
            explanation = "Check the required Konjunktiv verb form."
        elif target_feature == "passive" and got != want and (
                got in auxiliaries or want in auxiliaries or
                got in {"werden", "wird", "wurde", "wurden", "worden", "geworden"} or
                want in {"werden", "wird", "wurde", "wurden", "worden", "geworden"}):
            kind = "passive"
            explanation = "Check the auxiliary or participle in the passive construction."
        elif target_feature == "adjective" and got != want and (
                any(got.endswith(x) and want.endswith(y) and got[:-len(x)] == want[:-len(y)]
                    for x in ("e", "en", "em", "er", "es")
                    for y in ("e", "en", "em", "er", "es") if x != y)):
            kind = "adjective"
            explanation = "Check the adjective ending required by case, gender and article."
        elif target_feature == "participle" and got.endswith("en") and want.endswith("t"):
            kind = "participle"
            explanation = "Check the past participle form."
        elif (target_feature == "conjugation" and got != want
              and ((want.endswith("st") and got == want[:-2])
                   or (want.endswith("t") and got == want[:-1]))):
            kind = "conjugation"
            explanation = "The verb ending does not match the required subject."
        elif (target_feature == "conjugation" and got != want
              and any(got.endswith(a) and want.endswith(b)
                      and got[:-len(a)] == want[:-len(b)]
                      for a in ("en", "e", "st", "t") for b in ("en", "e", "st", "t")
                      if a != b and len(got) > len(a) + 1 and len(want) > len(b) + 1)):
            kind = "conjugation"
            explanation = "The verb ending does not match the required subject."
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
    # The canonical model answer remains valid alongside authored alternatives.
    accepted = _accepted_models(exercise)
    # Only explicitly authored alternatives are verified as equivalent.
    accepted_normalized = {normalize_text(item) for item in accepted}
    exact = bool(normalize_text(answer)) and any(
        normalize_text(answer) == normalize_text(model) and not _semantic_punctuation_conflict(answer, model)
        for model in accepted
    )
    # Spelling tolerance is only a legacy hint, never sufficient evidence
    # for a verified linguistic success: one deleted letter can create a
    # different valid German word (schreiben -> schreien).
    if legacy["correct"] and not exact:
        legacy["correct"] = False
        legacy["error_type"] = "answer_mismatch"
    open_ended = exercise.get("type") in {"translation", "translate", "free_text", "sentence", "writing"}
    empty_submission = not normalize_text(answer)
    # An empty response cannot satisfy a non-empty reference, even for open tasks.
    # This is a task-completion judgment, not a grammatical diagnosis.
    # An unlisted near-match in open writing may change meaning despite high similarity.
    # Only explicitly accepted text is deterministically verified for open tasks.
    status = ("needs_review" if not accepted else
              "verified" if (empty_submission or exact or not open_ended) else "uncertain")
    errors = []
    if status == "verified" and empty_submission:
        errors = [LinguisticError(
            type="empty_answer", span="", correction=legacy["model"],
            explanation="Enter an answer to complete this exercise.",
        )]
    elif status == "verified" and not legacy["correct"]:
        # A mismatch against one reference does not establish a linguistic
        # error when several authored correct forms exist. Keep the decision
        # but avoid attributing grammar faults to an arbitrary alternative.
        if len(accepted_normalized) > 1:
            errors = [LinguisticError(
                type="answer_mismatch", span=answer, correction=legacy["model"],
                explanation="This answer is not among the authored accepted responses.",
            )]
        else:
            errors = _classify_aligned_errors(answer, legacy["model"], exercise.get("target_feature", ""), exercise.get("type", ""))
        if not errors:
            errors = [LinguisticError(
                type=legacy["error_type"] or "answer_mismatch", span=answer,
                correction=legacy["model"],
                explanation="This response does not match the exercise requirement.",
            )]
    elif status == "uncertain":
        # Candidate diagnoses require a unique authored reference; selecting
        # the closest of several valid phrasings is not grammatical evidence.
        candidates = (_classify_aligned_errors(answer, legacy["model"], exercise.get("target_feature", ""), exercise.get("type", ""))
                      if len(accepted_normalized) == 1 else [])
        errors = [item for item in candidates if item.type in {"article", "negation", "auxiliary", "preposition", "conjugation", "infinitive"}]
    result = EvaluationResult(
        grammar_correct=True if exact else None,
        meaning_correct=True if exact else None,
        task_satisfied=(False if empty_submission and accepted else
                        bool(legacy["correct"]) if status == "verified" else None),
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
