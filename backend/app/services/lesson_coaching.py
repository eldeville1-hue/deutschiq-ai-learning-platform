"""Explainable adaptation and repair guidance for a learning session."""

from app.services.content_i18n import normalize_language
from app.services.misconception_feedback import misconception_feedback


def supported_retry_exercise(exercise: dict, lesson_content: dict, language: str) -> dict | None:
    """Build a fresh, easier phone task without exposing the answer key."""
    examples = [str(item).strip() for item in lesson_content.get("examples", []) if str(item).strip()]
    def sentence_key(value):
        return " ".join(str(value).split()).rstrip(".?!").casefold()

    original_answers = {sentence_key(item) for item in exercise.get("accepted_answers") or [exercise.get("answer", "")]}
    # Select a different authored example with similar vocabulary and length.
    # This keeps retries closer to the original pattern without inventing keys.
    reference = str((exercise.get("accepted_answers") or [exercise.get("answer", "")])[0])
    reference_tokens = sentence_key(reference).split()
    candidates = [item for item in examples if sentence_key(item) not in original_answers]
    # Explicit skill labels take precedence over surface word overlap.
    # Untagged examples remain usable for older curriculum content.
    target_skill = exercise.get("skill_id") or exercise.get("grammar_skill")
    tagged = [item for item in lesson_content.get("retry_examples", [])
              if isinstance(item, dict) and item.get("skill_id") == target_skill
              and isinstance(item.get("sentence"), str) and item["sentence"].strip()
              and sentence_key(item["sentence"]) not in original_answers] if target_skill else []
    if tagged:
        candidates = [item["sentence"].strip() for item in tagged]
    def similarity(item):
        words = sentence_key(item).split()
        return (len(set(reference_tokens) & set(words)), -abs(len(words) - len(reference_tokens)))
    model = max(candidates, key=similarity) if candidates else (examples[0] if examples else reference)
    # Do not present the same answer as a new retry. The caller can still
    # show its focused feedback and the original model for review.
    if sentence_key(model) in original_answers:
        return None
    model = model.rstrip(".?!")
    tokens = model.split()
    tokens = tokens[2:] + tokens[:2] if len(tokens) > 3 else list(reversed(tokens))
    lang = normalize_language(language)
    questions = {
        "ru": "Попробуй на новом примере. Собери фразу.",
        "de": "Versuche es mit einem neuen Beispiel. Baue den Satz.",
        "en": "Try a new example. Build the sentence.",
    }
    if not fresh:
        questions = {
            "ru": "Закрепи структуру. Собери фразу с подсказкой.",
            "de": "Festige das Muster. Baue den Satz mit Hilfe.",
            "en": "Practise the pattern. Build the sentence with support.",
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
        "explanation": str(lesson_content.get("rule") or exercise.get("explanation", "")),
        "misconception": exercise.get("misconception"),
        "mission_role": exercise.get("mission_role"),
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


def feedback_focus(error_type: str | None, missing_words: list[str], extra_words: list[str], language: str) -> str:
    """Return one actionable correction before revealing the complete model."""
    lang = normalize_language(language)
    copy = {
        "ru": {
            "missing": "Добавь: {words}.",
            "extra": "Убери или замени: {words}.",
            "order": "Все нужные слова есть — теперь проверь их порядок.",
        },
        "de": {
            "missing": "Ergänze: {words}.",
            "extra": "Entferne oder ersetze: {words}.",
            "order": "Alle nötigen Wörter sind da – prüfe jetzt ihre Reihenfolge.",
        },
        "en": {
            "missing": "Add: {words}.",
            "extra": "Remove or replace: {words}.",
            "order": "All required words are present—now check their order.",
        },
    }[lang]
    if missing_words:
        return copy["missing"].format(words=", ".join(missing_words[:4]))
    if extra_words:
        return copy["extra"].format(words=", ".join(extra_words[:4]))
    if error_type in {"answer_mismatch", "verb_not_final", "word_order"}:
        return copy["order"]
    return misconception_feedback(error_type, lang)


def success_feedback(explanation: str | None, language: str) -> str:
    """Never return an empty success state to the learner."""
    if explanation and explanation.strip():
        return explanation.strip()
    lang = normalize_language(language)
    return {
        "ru": "Форма и смысл подходят этой ситуации.",
        "de": "Form und Bedeutung passen zu dieser Situation.",
        "en": "The form and meaning fit this situation.",
    }[lang]
