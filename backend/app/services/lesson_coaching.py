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
    elif target_skill and any(isinstance(item, dict) and item.get("skill_id") for item in lesson_content.get("retry_examples", [])):
        # A tagged retry bank is skill-specific. Never substitute an unrelated
        # untagged example when this skill has no unused authored candidate.
        return None
    def similarity(item):
        words = sentence_key(item).split()
        return (len(set(reference_tokens) & set(words)), -abs(len(words) - len(reference_tokens)))
    model = max(candidates, key=similarity) if candidates else None
    if model is None:
        return None
    # Do not present the same answer as a new retry. The caller can still
    # show its focused feedback and the original model for review.
    if sentence_key(model) in original_answers:
        return None
    model = model.rstrip(".?!")
    # Use a curriculum-authored target when available. Avoid hiding an
    # unrelated article just because it appears earlier in the sentence.
    authored_target = next((item.get("target") for item in tagged
                            if item["sentence"].strip().rstrip(".?!") == model
                            and isinstance(item.get("target"), str)), None)
    answer_tokens = model.split()
    # A reorder exercise is not meaningful if the correct sequence is unchanged.
    if len(answer_tokens) < 2 or len({token.casefold() for token in answer_tokens}) < 2:
        return None
    # For case, article, and verb-form skills, ask the learner to retrieve
    # the actual form instead of merely rearranging a fully visible sentence.
    # The blank is selected from a complete, authored answer.
    form_skills = {"dative_case", "prepositions", "dative_pronouns", "articles",
                   "perfekt_auxiliary", "participles", "verbs_of_movement"}
    if target_skill in form_skills:
        import re
        words = list(re.finditer(r"\b[\wÄÖÜäöüß]+\b", model))
        forms = {
            "dative_case": {"dem", "der", "den", "einem", "einer", "einen"},
            "prepositions": {"für", "ohne", "durch", "gegen", "mit", "aus", "bei", "nach", "seit", "von", "zu"},
            "dative_pronouns": {"mir", "dir", "ihm", "ihr", "uns", "euch", "ihnen"},
            "articles": {"der", "die", "das", "ein", "eine", "einen", "kein", "keine", "keinen"},
            "perfekt_auxiliary": {"habe", "hast", "hat", "haben", "habt", "bin", "bist", "ist", "sind", "seid"},
            "participles": set(),
            "verbs_of_movement": {"bin", "bist", "ist", "sind", "seid"},
        }
        eligible = [word for word in words if word.group().casefold() in forms[target_skill]]
        if authored_target:
            eligible = [word for word in words if word.group() == authored_target]
        if target_skill == "participles" and not authored_target:
            eligible = [word for word in words if word.group().casefold().startswith(("ge", "be", "ver", "er", "auf", "an", "ein"))
                        and len(word.group()) > 5]
        if eligible:
            chosen = eligible[-1] if target_skill == "participles" else eligible[0]
            blanked = model[:chosen.start()] + "___" + model[chosen.end():]
            prompts = {
                "ru": "Вставь правильную форму в новом предложении:",
                "de": "Ergänze die richtige Form im neuen Satz:",
                "en": "Fill in the correct form in this new sentence:",
            }
            return {
                "id": f"{exercise.get('id', 'exercise')}-retry",
                "type": "fill",
                "stage": "guided",
                "question": f"{prompts[normalize_language(language)]} {blanked}",
                "answer": chosen.group(),
                "accepted_answers": [chosen.group()],
                "hint": str(lesson_content.get("rule") or exercise.get("hint") or ""),
                "explanation": str(lesson_content.get("rule") or exercise.get("explanation", "")),
                "misconception": exercise.get("misconception"),
                "mission_role": exercise.get("mission_role"),
            }
    # Never turn a form-retrieval retry into a word-order puzzle. If the 
    # authored sentence lacks a safe target, show the original feedback instead. 
    if target_skill in form_skills: 
        return None
    tokens = answer_tokens[2:] + answer_tokens[:2] if len(answer_tokens) > 3 else list(reversed(answer_tokens))
    if tokens == answer_tokens:
        tokens = answer_tokens[1:] + answer_tokens[:1]
    if tokens == answer_tokens:
        return None
    lang = normalize_language(language)
    questions = {
        "ru": "Попробуй на новом примере. Собери фразу.",
        "de": "Versuche es mit einem neuen Beispiel. Baue den Satz.",
        "en": "Try a new example. Build the sentence.",
    }
    if not candidates:
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


def repeated_error_focus(attempts: list[dict], available_skills: set[str] | None = None) -> str | None:
    """Choose a repeatedly missed skill from recent attempts, never an unseen skill.

    Attempts are chronological dictionaries with skill_id and correct. Require
    at least two wrong attempts and more errors than successes for the skill.
    """
    counts: dict[str, list[int]] = {}
    last_wrong: dict[str, int] = {}
    for index, attempt in enumerate(attempts[-12:]):
        if not isinstance(attempt, dict) or not isinstance(attempt.get("correct"), bool):
            continue
        skill = attempt.get("skill_id")
        if not isinstance(skill, str) or not skill.strip():
            continue
        if available_skills is not None and skill not in available_skills:
            continue
        totals = counts.setdefault(skill, [0, 0])
        if attempt["correct"]:
            totals[1] += 1
        else:
            totals[0] += 1
            last_wrong[skill] = index
    eligible = [skill for skill, (wrong, right) in counts.items()
                if wrong >= 2 and wrong > right]
    # Prefer unresolved recent mistakes over older mistakes with equal net errors.
    # A skill with a more recent correct answer is still eligible only when
    # its total errors exceed successes, preserving the existing evidence gate.
    return max(eligible, key=lambda skill: (counts[skill][0] - counts[skill][1],
                                             last_wrong[skill])) if eligible else None


def learning_profile(mastery: float, recent_correct: list[bool], correct_streak: int = 0,
                     recent_skill_attempts: list[dict] | None = None,
                     available_skills: set[str] | None = None) -> dict:
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
        "focus_skill": repeated_error_focus(recent_skill_attempts or [], available_skills),
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
    # Repair steps must address the detected grammar error rather than always
    # directing learners to check word order.
    targeted = {
        "ru": {
            "case": ("Проверь падеж после глагола или предлога.", "Подставь правильную форму артикля или местоимения."),
            "article": ("Определи род и падеж существительного.", "Выбери правильный артикль для этого контекста."),
            "conjugation": ("Найди подлежащее и его лицо.", "Согласуй окончание глагола с подлежащим."),
            "auxiliary": ("Определи, нужен ли в Perfekt haben или sein.", "Поставь вспомогательный глагол в правильную форму."),
        },
        "de": {
            "case": ("Prüfe den Kasus nach Verb oder Präposition.", "Setze Artikel oder Pronomen in die passende Form."),
            "article": ("Bestimme Genus und Kasus des Nomens.", "Wähle den passenden Artikel im Satz."),
            "conjugation": ("Bestimme Person und Numerus des Subjekts.", "Passe die Verbendung an das Subjekt an."),
            "auxiliary": ("Prüfe, ob das Perfekt haben oder sein braucht.", "Konjugiere das Hilfsverb passend zum Subjekt."),
        },
        "en": {
            "case": ("Check the case required by the verb or preposition.", "Choose the matching article or pronoun form."),
            "article": ("Identify the noun's gender and case.", "Choose the article that fits this sentence."),
            "conjugation": ("Identify the subject's person and number.", "Match the verb ending to the subject."),
            "auxiliary": ("Check whether Perfekt needs haben or sein.", "Conjugate the auxiliary for the subject."),
        },
    }
    if error_type in targeted[language]:
        first, practice = targeted[language][error_type]
        return [first, practice]
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
