"""Explainable adaptation and repair guidance for a learning session."""


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

