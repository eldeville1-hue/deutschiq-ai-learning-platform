ALLOWED_EXERCISE_TYPES = {
    "choose", "fill", "translate", "reorder", "listening", "production", "recall", "repeat",
    "error_repair", "transform", "context_choice", "listening_choice", "dialogue",
}


def normalize_lesson_content(content: dict, topic: str, level: str) -> dict:
    value = dict(content or {})
    examples = value.get("examples") or []
    example = examples[0] if examples else "Heute lerne ich Deutsch."
    value.setdefault("objective", f"Использовать тему «{topic}» в собственной немецкой фразе.")
    value.setdefault("rule", "Изучи структуру и примени её в задании.")
    value.setdefault("examples", [example])
    value.setdefault("audio_text", example)
    if not value.get("common_mistakes"):
        value["common_mistakes"] = [
            "❌ Не переноси русскую структуру дословно.",
            f"✅ Ориентируйся на модель: {example}",
        ]
    value.setdefault("cefr", level)
    value.setdefault("prerequisites", [])
    exercises = []
    for index, exercise in enumerate(value.get("exercises") or []):
        item = dict(exercise)
        item.setdefault("type", "fill")
        if item["type"] == "listen":
            item["type"] = "listening"
        item.setdefault("stage", ("guided", "independent", "transfer")[min(index, 2)])
        if item.get("answer") and not item.get("accepted_answers"):
            item["accepted_answers"] = [item["answer"]]
        item.setdefault("explanation", item.get("hint") or "Сравни ответ с правилом и повтори структуру ещё раз.")
        exercises.append(item)
    if not any(item.get("type") == "repeat" for item in exercises):
        exercises.append({
            "type": "repeat", "stage": "transfer",
            "question": "Произнеси пример вслух. Система проверит распознанные слова.",
            "answer": example, "accepted_answers": [example],
            "explanation": "Повтори фразу ещё раз, сохраняя порядок слов и окончания.",
        })
    value["exercises"] = exercises
    return value


def validate_lesson_content(content: dict) -> list[str]:
    errors = []
    for field in ("objective", "rule", "examples", "audio_text", "common_mistakes", "exercises"):
        if not content.get(field):
            errors.append(f"missing:{field}")
    for index, exercise in enumerate(content.get("exercises") or []):
        kind = exercise.get("type")
        if kind not in ALLOWED_EXERCISE_TYPES:
            errors.append(f"exercise:{index}:invalid_type")
        if not exercise.get("question"):
            errors.append(f"exercise:{index}:missing_question")
        if not (exercise.get("answer") or exercise.get("accepted_answers")):
            errors.append(f"exercise:{index}:missing_answer")
        if not exercise.get("explanation"):
            errors.append(f"exercise:{index}:missing_explanation")
    return errors


def validate_roadmap_content(content: dict) -> list[str]:
    errors = validate_lesson_content(content)
    for field in ("day", "communication_goal", "recall_prompt", "cefr", "prerequisites"):
        if field not in content or content.get(field) in (None, ""):
            errors.append(f"missing:{field}")
    stages = {item.get("stage") for item in content.get("exercises") or []}
    for stage in ("guided", "independent", "transfer"):
        if stage not in stages:
            errors.append(f"missing_stage:{stage}")
    productions = [item for item in content.get("exercises") or [] if item.get("type") in {"production", "dialogue"}]
    if not productions:
        errors.append("missing:production")
    elif not productions[0].get("target_patterns"):
        errors.append("production:missing_target_patterns")
    if content.get("quality_version", 0) >= 2:
        if len(content.get("examples") or []) < 3:
            errors.append("gold:insufficient_examples")
        kinds = {item.get("type") for item in content.get("exercises") or []}
        if not kinds.intersection({"listening", "listening_choice"}):
            errors.append("gold:missing_listening")
        if not kinds.intersection({"production", "dialogue"}):
            errors.append("gold:missing_production")
        if "repeat" not in kinds:
            errors.append("gold:missing_repeat")
        if len(content.get("exercises") or []) < 4:
            errors.append("gold:insufficient_exercises")
        mistakes = content.get("common_mistakes") or []
        if not any("❌" in item for item in mistakes) or not any("✅" in item for item in mistakes):
            errors.append("gold:missing_contrast")
    if content.get("quality_version", 0) >= 4:
        exercises = content.get("exercises") or []
        kinds = {item.get("type") for item in exercises}
        prompts = [str(item.get("question", "")).strip().casefold() for item in exercises]
        if content.get("learning_method") != "notice_build_use_reflect":
            errors.append("adaptive:missing_learning_method")
        if len(exercises) < 5 or len(kinds) < 4:
            errors.append("adaptive:insufficient_variety")
        if any(not item.get("misconception") for item in exercises):
            errors.append("adaptive:missing_misconception")
        if len(prompts) != len(set(prompts)):
            errors.append("adaptive:duplicate_prompt")
    return errors
