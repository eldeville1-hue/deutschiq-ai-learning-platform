import asyncio
import json
import re
from typing import Any

def _words(value: str) -> list[str]:
    return re.findall(r"[a-zäöüß]+", value.lower())


def local_feedback(answer: str, exercise: dict, rule: str) -> dict[str, Any]:
    words = _words(answer)
    patterns = [str(item).lower() for item in exercise.get("target_patterns", [])]
    pattern_hits = sum(1 for item in patterns if item in answer.lower())
    has_capital_start = bool(answer.strip()[:1].isupper())
    has_enough_language = len(words) >= 4
    score = min(100, (45 if has_enough_language else 20) + (35 if pattern_hits else 0) + (20 if has_capital_start else 0))
    passed = has_enough_language and score >= 70
    if passed:
        feedback = "Фраза выполняет задачу. Сравни её с моделью и произнеси вслух один раз."
    elif not has_enough_language:
        feedback = "Ответ слишком короткий. Напиши полное немецкое предложение минимум из четырёх слов."
    elif patterns:
        feedback = f"Используй целевую структуру урока: {', '.join(patterns[:3])}. Правило: {rule}"
    else:
        feedback = f"Проверь структуру предложения. Правило: {rule}"
    return {
        "correct": passed,
        "score": score,
        "feedback": feedback,
        "corrected_answer": exercise.get("model_answer") or exercise.get("answer", ""),
        "source": "local",
    }


def _ai_feedback(answer: str, exercise: dict, lesson_content: dict) -> dict[str, Any]:
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
                    "Ты проверяешь одну немецкую фразу ученика. Оцени выполнение задания, грамматику "
                    "и понятность на указанном CEFR. Не требуй совпадения с моделью. Верни только JSON: "
                    '{"correct":bool,"score":0-100,"feedback":"кратко по-русски",'
                    '"corrected_answer":"исправленная немецкая фраза"}.'
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
        "feedback": str(result.get("feedback") or "Проверь предложение ещё раз."),
        "corrected_answer": str(result.get("corrected_answer") or exercise.get("answer", "")),
        "source": "ai",
    }


async def evaluate_production(answer: str, exercise: dict, lesson_content: dict) -> dict[str, Any]:
    from app.core.config import settings

    fallback = local_feedback(answer, exercise, lesson_content.get("rule", ""))
    if not settings.OPENAI_API_KEY:
        return fallback
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(_ai_feedback, answer, exercise, lesson_content),
            timeout=10,
        )
    except Exception:
        return fallback
