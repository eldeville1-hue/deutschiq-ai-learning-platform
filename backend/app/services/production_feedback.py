import asyncio
import json
import re
from typing import Any
from app.services.answer_intelligence import normalize_text, word_diff

def _words(value: str) -> list[str]:
    return re.findall(r"[a-zäöüß]+", value.lower())


def local_feedback(answer: str, exercise: dict, rule: str, lang: str = "en") -> dict[str, Any]:
    words = _words(answer)
    patterns = [str(item).lower() for item in exercise.get("target_patterns", [])]
    normalized_answer = normalize_text(answer)
    pattern_hits = sum(1 for item in patterns if normalize_text(item) in normalized_answer)
    has_capital_start = bool(answer.strip()[:1].isupper())
    has_enough_language = len(words) >= 4
    target_ratio = pattern_hits / max(len(patterns), 1) if patterns else 1.0
    score = min(100, (45 if has_enough_language else 15) + round(45 * target_ratio) + (10 if has_capital_start else 0))
    passed = has_enough_language and target_ratio >= 0.5 and score >= 70
    language = lang if lang in ("ru", "de", "en") else "en"
    if passed:
        feedback = {"ru": "Задача выполнена. Сравни с моделью и произнеси фразу вслух.", "de": "Aufgabe erfüllt. Vergleiche mit dem Modell und sprich den Satz laut.", "en": "Task completed. Compare with the model and say the sentence aloud."}[language]
    elif not has_enough_language:
        feedback = {"ru": "Ответ слишком короткий. Напиши полное немецкое предложение минимум из четырёх слов.", "de": "Die Antwort ist zu kurz. Schreibe einen vollständigen deutschen Satz mit mindestens vier Wörtern.", "en": "The answer is too short. Write a complete German sentence of at least four words."}[language]
    elif patterns:
        lead = {"ru": "Используй структуру", "de": "Nutze die Struktur", "en": "Use the target structure"}[language]
        feedback = f"{lead}: {', '.join(patterns[:3])}. {rule}"
    else:
        feedback = {"ru": f"Проверь структуру предложения. {rule}", "de": f"Prüfe die Satzstruktur. {rule}", "en": f"Check the sentence structure. {rule}"}[language]
    model = exercise.get("model_answer") or exercise.get("answer", "")
    diff = word_diff(answer, model)
    error_type = None if passed else ("response_too_short" if not has_enough_language else exercise.get("misconception") or "missing_target_structure")
    return {
        "correct": passed,
        "score": score,
        "feedback": feedback,
        "corrected_answer": model,
        "source": "local",
        "error_type": error_type,
        "missing_words": diff["missing"],
        "extra_words": diff["extra"],
    }


def _ai_feedback(answer: str, exercise: dict, lesson_content: dict, lang: str) -> dict[str, Any]:
    from openai import OpenAI
    from app.core.config import settings

    client = OpenAI(api_key=settings.OPENAI_API_KEY, timeout=8.0, max_retries=0)
    prompt = {
        "cefr": lesson_content.get("cefr", "A2"),
        "objective": lesson_content.get("objective", ""),
        "rule": lesson_content.get("rule", ""),
        "task": exercise.get("question", ""),
        "target_patterns": exercise.get("target_patterns", []),
        "model_answer": exercise.get("model_answer") or exercise.get("answer", ""),
        "learner_answer": answer,
    }
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        temperature=0.1,
        max_tokens=260,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "Evaluate one German learner sentence for task completion, grammar and clarity at the given CEFR. "
                    f"Write feedback in { {'ru':'Russian','de':'German','en':'English'}.get(lang, 'English') }. Do not require an exact model match. Return JSON only: "
                    '{"correct":bool,"score":0-100,"feedback":"brief feedback",'
        '"corrected_answer":"corrected German sentence","error_type":"brief category"}.'
                ),
            },
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
    )
    result = json.loads(response.choices[0].message.content or "{}")
    score = max(0, min(100, int(result.get("score", 0))))
    return {
        "correct": bool(result.get("correct")) and score >= 70,
        "score": score,
        "feedback": str(result.get("feedback") or {"ru": "Проверь предложение ещё раз.", "de": "Prüfe den Satz noch einmal.", "en": "Check the sentence once more."}.get(lang, "Check the sentence once more.")),
        "corrected_answer": str(result.get("corrected_answer") or exercise.get("answer", "")),
        "source": "ai",
        "error_type": result.get("error_type"),
        "missing_words": word_diff(answer, str(result.get("corrected_answer") or exercise.get("answer", "")))["missing"],
    }


async def evaluate_production(answer: str, exercise: dict, lesson_content: dict, lang: str = "en") -> dict[str, Any]:
    from app.core.config import settings

    fallback = local_feedback(answer, exercise, lesson_content.get("rule", ""), lang)
    if not settings.OPENAI_API_KEY:
        return fallback
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(_ai_feedback, answer, exercise, lesson_content, lang),
            timeout=10,
        )
    except Exception:
        return fallback
