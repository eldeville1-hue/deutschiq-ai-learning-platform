import asyncio
import json
import re
from typing import Any

from app.services.answer_intelligence import normalize_text, word_diff

DIMENSIONS = ("task_completion", "grammar", "vocabulary", "coherence", "register")
WEIGHTS = {"task_completion": 0.30, "grammar": 0.25, "vocabulary": 0.15, "coherence": 0.15, "register": 0.15}
PASS_MARKS = {"A1": 65, "A2": 65, "B1": 70, "B2": 75, "C1": 80}
MIN_WORDS = {"A1": 4, "A2": 5, "B1": 7, "B2": 10, "C1": 12}
GERMAN_SIGNALS = {"ich", "du", "er", "sie", "wir", "ihr", "ist", "sind", "bin", "habe", "hat", "wird", "weil", "obwohl", "dass", "wenn", "als", "aber", "und", "oder", "nicht", "mit", "für", "der", "die", "das", "ein", "eine", "meiner", "daher", "jedoch", "zwar", "dennoch", "sollte", "könnte"}
COHERENCE_SIGNALS = {"weil", "obwohl", "aber", "deshalb", "daher", "dennoch", "jedoch", "einerseits", "andererseits", "zunächst", "anschließend", "schließlich", "sodass"}
FORMAL_SIGNALS = {"sie", "ihnen", "bitte", "daher", "jedoch", "dennoch", "insgesamt", "hinsichtlich", "aufgrund", "meines", "erachtens"}


def _words(value: str) -> list[str]:
    return re.findall(r"[a-zäöüß]+", value.lower())


def _clamp(value: Any) -> int:
    try:
        return max(0, min(100, round(float(value))))
    except (TypeError, ValueError):
        return 0


def _overall(scores: dict[str, int]) -> int:
    return round(sum(scores[name] * WEIGHTS[name] for name in DIMENSIONS))


def _copy(lang: str) -> dict[str, str]:
    language = lang if lang in ("ru", "de", "en") else "en"
    return {
        "short": {"ru": "Ответ слишком короткий для этой задачи.", "de": "Die Antwort ist für diese Aufgabe zu kurz.", "en": "The response is too short for this task."}[language],
        "off_topic": {"ru": "Ответ не выполняет немецкую коммуникативную задачу.", "de": "Die Antwort erfüllt die deutsche Kommunikationsaufgabe nicht.", "en": "The response does not address the German communication task."}[language],
        "passed": {"ru": "Задача выполнена: ответ понятный и самостоятельный.", "de": "Aufgabe erfüllt: Die Antwort ist verständlich und eigenständig.", "en": "Task completed: the response is clear and independent."}[language],
        "structure": {"ru": "Используй целевую структуру яснее.", "de": "Nutze die Zielstruktur deutlicher.", "en": "Use the target structure more clearly."}[language],
        "expand": {"ru": "Добавь причину, связь или конкретную деталь.", "de": "Ergänze einen Grund, eine Verknüpfung oder ein konkretes Detail.", "en": "Add a reason, connection, or concrete detail."}[language],
        "grammar": {"ru": "Проверь порядок слов, форму глагола и окончания.", "de": "Prüfe Wortstellung, Verbform und Endungen.", "en": "Check word order, verb form, and endings."}[language],
        "register": {"ru": "Сделай формулировку точнее и уместнее для ситуации.", "de": "Formuliere präziser und situationsgerechter.", "en": "Make the wording more precise and appropriate to the situation."}[language],
    }


def _local_scores(answer: str, exercise: dict, cefr: str) -> tuple[dict[str, int], str | None]:
    words = _words(answer)
    word_set = set(words)
    normalized = normalize_text(answer)
    patterns = [normalize_text(str(item)) for item in exercise.get("target_patterns", []) if str(item).strip()]
    hits = sum(1 for item in patterns if item in normalized)
    pattern_ratio = hits / len(patterns) if patterns else 1.0
    minimum = MIN_WORDS.get(cefr, 7)
    german_signal = bool(word_set & GERMAN_SIGNALS) or bool(re.search(r"[äöüß]", answer.lower()))
    sentence_complete = len(words) >= minimum and bool(re.search(r"[.!?]\s*$", answer.strip()))
    capitalized = bool(answer.strip()[:1].isupper())
    connector = bool(word_set & COHERENCE_SIGNALS)
    formal = bool(word_set & FORMAL_SIGNALS)
    lexical_range = len(set(words)) / max(len(words), 1)
    scores = {
        "task_completion": _clamp((65 + 35 * pattern_ratio) if german_signal and len(words) >= minimum else (35 if german_signal else 5)),
        "grammar": _clamp(35 + (30 if capitalized else 0) + (35 if sentence_complete else 10 if len(words) >= minimum else 0)),
        "vocabulary": _clamp(35 + min(40, len(set(words)) * 4) + (20 if lexical_range >= 0.65 else 5)),
        "coherence": _clamp(40 + (35 if connector else 10) + (25 if len(words) >= minimum + 4 else 5)),
        "register": _clamp(55 + (30 if formal else 10) + (15 if capitalized else 0)),
    }
    reason = "off_topic" if not german_signal else "response_too_short" if len(words) < minimum else None
    return scores, reason


def local_feedback(answer: str, exercise: dict, rule: str, lang: str = "en", cefr: str = "A1") -> dict[str, Any]:
    cefr = str(cefr or "A1").upper()
    scores, blocking_error = _local_scores(answer, exercise, cefr)
    model = exercise.get("model_answer") or exercise.get("answer", "")
    if cefr in {"A1", "A2", "B1"} and model and normalize_text(answer) == normalize_text(str(model)):
        scores = {name: 100 for name in DIMENSIONS}
        blocking_error = None
    score = _overall(scores)
    threshold = PASS_MARKS.get(cefr, 70)
    passed = blocking_error is None and score >= threshold and scores["task_completion"] >= 60 and scores["grammar"] >= 50
    copy = _copy(lang)
    weakest = min(DIMENSIONS, key=lambda name: scores[name])
    improvement_key = {"task_completion": "structure", "grammar": "grammar", "vocabulary": "expand", "coherence": "expand", "register": "register"}[weakest]
    blocking_copy = {"response_too_short": "short", "off_topic": "off_topic"}.get(blocking_error)
    feedback = copy["passed"] if passed else copy[blocking_copy or improvement_key]
    improvement = copy[improvement_key]
    if not passed and weakest == "task_completion" and rule:
        improvement = f"{improvement} {rule}"
    corrected = answer.strip() if passed else model
    diff = word_diff(answer, model)
    return {
        "correct": passed, "score": score, "dimension_scores": scores,
        "feedback": feedback, "improvement": improvement, "corrected_answer": corrected,
        "source": "local", "error_type": None if passed else (blocking_error or exercise.get("misconception") or f"weak_{weakest}"),
        "missing_words": [] if passed else diff["missing"], "extra_words": [] if passed else diff["extra"],
        "cefr_standard": cefr, "pass_mark": threshold,
    }


def _ai_feedback(answer: str, exercise: dict, lesson_content: dict, lang: str) -> dict[str, Any]:
    from openai import OpenAI
    from app.core.config import settings

    cefr = str(lesson_content.get("cefr", "A2")).upper()
    client = OpenAI(api_key=settings.OPENAI_API_KEY, timeout=8.0, max_retries=0)
    prompt = {"cefr": cefr, "pass_mark": PASS_MARKS.get(cefr, 70), "objective": lesson_content.get("objective", ""), "rule": lesson_content.get("rule", ""), "task": exercise.get("question", ""), "target_patterns": exercise.get("target_patterns", []), "assessment_rubric": lesson_content.get("assessment_rubric", []), "model_answer": exercise.get("model_answer") or exercise.get("answer", ""), "learner_answer": answer}
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL, temperature=0.1, max_tokens=420, response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": (
                "Evaluate an independent German learner response at the stated CEFR. Do not require the model wording. Reject off-topic answers and fragments. "
                "Score task_completion, grammar, vocabulary, coherence, and register from 0-100. Give one brief diagnosis and exactly one actionable improvement. "
                f"Write feedback in { {'ru':'Russian','de':'German','en':'English'}.get(lang, 'English') }. Return JSON only: "
                '{"dimension_scores":{"task_completion":0,"grammar":0,"vocabulary":0,"coherence":0,"register":0},"feedback":"brief diagnosis","improvement":"one next step","corrected_answer":"natural German correction","error_type":"brief category or null"}.'
            )},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
    )
    result = json.loads(response.choices[0].message.content or "{}")
    raw_scores = result.get("dimension_scores") or {}
    if not all(name in raw_scores for name in DIMENSIONS):
        raise ValueError("AI assessment omitted rubric dimensions")
    scores = {name: _clamp(raw_scores[name]) for name in DIMENSIONS}
    score = _overall(scores)
    threshold = PASS_MARKS.get(cefr, 70)
    passed = score >= threshold and scores["task_completion"] >= 60 and scores["grammar"] >= 50
    corrected = str(result.get("corrected_answer") or exercise.get("answer", ""))
    return {
        "correct": passed, "score": score, "dimension_scores": scores,
        "feedback": str(result.get("feedback") or _copy(lang)["grammar"]), "improvement": str(result.get("improvement") or _copy(lang)["expand"]),
        "corrected_answer": corrected, "source": "ai", "error_type": None if passed else (result.get("error_type") or "production_below_cefr"),
        "missing_words": [] if passed else word_diff(answer, corrected)["missing"], "extra_words": [] if passed else word_diff(answer, corrected)["extra"],
        "cefr_standard": cefr, "pass_mark": threshold,
    }


async def evaluate_production(answer: str, exercise: dict, lesson_content: dict, lang: str = "en") -> dict[str, Any]:
    from app.core.config import settings

    fallback = local_feedback(answer, exercise, lesson_content.get("rule", ""), lang, lesson_content.get("cefr", "A2"))
    model = exercise.get("model_answer") or exercise.get("answer", "")
    if model and normalize_text(answer) == normalize_text(str(model)):
        return fallback
    if not settings.OPENAI_API_KEY:
        return fallback
    try:
        return await asyncio.wait_for(asyncio.to_thread(_ai_feedback, answer, exercise, lesson_content, lang), timeout=10)
    except Exception:
        return fallback
