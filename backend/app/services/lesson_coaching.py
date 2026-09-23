"""Explainable adaptation and repair guidance for a learning session."""

from app.services.content_i18n import normalize_language


def supported_retry_exercise(exercise: dict, lesson_content: dict, language: str) -> dict:
    """Build a fresh, easier phone task without exposing the answer key."""
    examples = [str(item).strip() for item in lesson_content.get("examples", []) if str(item).strip()]
    original_answers = set(exercise.get("accepted_answers") or [exercise.get("answer", "")])
    model = next((item for item in examples[1:] if item not in original_answers), examples[0] if examples else str(exercise.get("answer", "")))
    model = model.rstrip(".?!")
    tokens = model.split()
    tokens = tokens[2:] + tokens[:2] if len(tokens) > 3 else list(reversed(tokens))
    lang = normalize_language(language)
    questions = {
        "ru": "Попробуй на новом примере. Собери фразу.",
        "de": "Versuche es mit einem neuen Beispiel. Baue den Satz.",
        "en": "Try a new example. Build the sentence.",
    }
    hints = {
        "ru": "Нажимай слова по порядку. Нажми слово в ответе, чтобы убрать его.",
        "de": "Tippe die Wörter der Reihe nach an. Tippe oben auf ein Wort, um es zu entfernen.",
        "en": "Tap the words in order. Tap a word above to remove it.",
    }
    return {
        "id": f"{exercise.get('id', 'exercise')}-retry",
        "type": "reorder",
        "stage": "guided",
        "question": questions[lang],
        "answer": model,
        "accepted_answers": [model, f"{model}."],
        "tokens": tokens,
        "hint": hints[lang],
        "explanation": str(exercise.get("explanation", "")),
        "misconception": exercise.get("misconception"),
    }


def learning_profile(mastery: float, recent_correct: list[bool], correct_streak: int = 0) -> dict:
    recent = recent_correct[-4:]
    recent_accuracy = round(sum(recent) / len(recent) * 100) if recent else None
    struggling = len(recent) >= 2 and sum(recent[-2:]) == 0
    if mastery < 35 or struggling:
        mode = "supported"
    elif mastery >= 75 and correct_streak >= 2 and (recent_accuracy is None or recent_accuracy >= 75):
        mode = "challenge"
    else:
        mode = "balanced"
    return {
        "mode": mode,
        "mastery": round(max(0, min(100, mastery))),
        "recent_accuracy": recent_accuracy,
        "show_guided_hint": mode == "supported",
    }


def repair_plan(error_type: str | None, missing_words: list[str], extra_words: list[str], language: str) -> list[str]:
    language = language if language in {"ru", "de", "en"} else "en"
    copy = {
        "ru": {
            "rule": "Назови правило урока одним коротким предложением.",
            "build": "Собери фразу заново: сначала основа, затем детали.",
            "check": "Прочитай ответ вслух и проверь порядок слов.",
            "missing": "Добавь пропущенные элементы: {words}.",
            "extra": "Проверь лишние элементы: {words}.",
        },
        "de": {
            "rule": "Nenne die Regel der Lektion in einem kurzen Satz.",
            "build": "Baue den Satz neu: zuerst das Grundgerüst, dann die Details.",
            "check": "Lies die Antwort laut und prüfe die Wortstellung.",
            "missing": "Ergänze die fehlenden Elemente: {words}.",
            "extra": "Prüfe die zusätzlichen Elemente: {words}.",
        },
        "en": {
            "rule": "State the lesson rule in one short sentence.",
            "build": "Rebuild the sentence: core structure first, then details.",
            "check": "Read the answer aloud and check the word order.",
            "missing": "Add the missing elements: {words}.",
            "extra": "Check the extra elements: {words}.",
        },
    }[language]
    steps = [copy["rule"]]
    if missing_words:
        steps.append(copy["missing"].format(words=", ".join(missing_words[:4])))
    elif extra_words:
        steps.append(copy["extra"].format(words=", ".join(extra_words[:4])))
    else:
        steps.append(copy["build"])
    steps.append(copy["check"])
    return steps
