from typing import Sequence


TOPIC_NAMES = {
    "articles": {"ru": "артикли", "de": "Artikel", "en": "articles"},
    "word_order": {"ru": "порядок слов", "de": "Wortstellung", "en": "word order"},
    "dative_case": {"ru": "дательный падеж", "de": "Dativ", "en": "the dative case"},
    "genitive_prepositions": {"ru": "предлоги с Genitiv", "de": "Präpositionen mit Genitiv", "en": "genitive prepositions"},
    "perfekt_auxiliary": {"ru": "Perfekt", "de": "Perfekt", "en": "the perfect tense"},
    "haben_conjugation": {"ru": "спряжение haben", "de": "Konjugation von haben", "en": "conjugating haben"},
}

# Reviewed, deterministic examples. Never label a generic word-order drill as
# practice for an unrelated grammar topic.
TOPIC_LESSONS = {
    "articles": ("Der Hund schläft.", "der / Hund / schläft", "Nouns have grammatical gender; learn each noun with its article.", "Nomen haben ein grammatisches Geschlecht; lerne sie mit Artikel.", "У существительных есть грамматический род; учи их вместе с артиклем."),
    "word_order": ("Heute lerne ich Deutsch.", "heute / ich / Deutsch / lerne", "The conjugated verb usually takes second position in a main clause.", "Im Hauptsatz steht das konjugierte Verb normalerweise an zweiter Position.", "В главном предложении спрягаемый глагол обычно стоит на втором месте."),
    "dative_case": ("Ich helfe dem Mann.", "ich / helfe / dem Mann", "The verb helfen takes the dative case: dem Mann.", "Das Verb helfen verlangt den Dativ: dem Mann.", "Глагол helfen требует Dativ: dem Mann."),
    "genitive_prepositions": ("Wegen des Regens bleiben wir zu Hause.", "wegen / des Regens / bleiben wir zu Hause", "In formal German, wegen is commonly followed by the genitive.", "In der Standardsprache steht nach wegen häufig der Genitiv.", "В нормативном немецком после wegen часто используется Genitiv."),
    "perfekt_auxiliary": ("Ich bin nach Berlin gefahren.", "ich / bin / nach Berlin / gefahren", "Many verbs of movement use sein in the Perfekt.", "Viele Bewegungsverben bilden das Perfekt mit sein.", "Многие глаголы движения образуют Perfekt с sein."),
    "haben_conjugation": ("Du hast heute Zeit.", "du / hast / heute Zeit", "Haben changes to hast with du.", "Haben wird bei du zu hast.", "С местоимением du глагол haben принимает форму hast."),
}


def _detect_topic(question: str, topics: Sequence[str]) -> str:
    lowered = question.casefold()
    keywords = {
        "articles": ("artikel", "article", "артикл"),
        "word_order": ("wortstellung", "word order", "порядок слов"),
        "dative_case": ("dativ", "dative", "дательн"),
        "genitive_prepositions": ("genitiv", "genitive", "родительн"),
        "perfekt_auxiliary": ("perfekt", "perfect tense", "прошедш"),
        "haben_conjugation": ("haben", "спряжени"),
    }
    for topic, terms in keywords.items():
        if any(term in lowered for term in terms):
            return topic
    return next((topic for topic in topics if topic in TOPIC_LESSONS), "word_order")


def fallback_answer(question: str, lang: str, level: str, topics: Sequence[str]) -> str:
    """Return a small, actionable lesson when the external AI is unavailable."""
    lowered = question.casefold()
    topic_key = _detect_topic(question, topics)
    example, words, rule_en, rule_de, rule_ru = TOPIC_LESSONS[topic_key]
    language = lang if lang in ("ru", "de", "en") else "en"
    names = TOPIC_NAMES.get(topic_key, {"ru": topic_key.replace("_", " "), "de": topic_key.replace("_", " "), "en": topic_key.replace("_", " ")})
    topic = names[language]
    wants_exercise = any(word in lowered for word in ("упраж", "задани", "übung", "aufgabe", "exercise", "practice", "quiz"))
    wants_error = any(word in lowered for word in ("ошиб", "fehler", "korrig", "error", "mistake", "correct"))

    if lang.startswith("de"):
        if wants_exercise:
            return f"Übung auf Niveau {level} – {topic}: Ordne „{words}“. Antworte mit dem vollständigen Satz."
        if wants_error:
            return "Schick mir bitte den deutschen Satz und – wenn möglich – deine ursprüngliche Antwort. Ich markiere genau eine Fehlerstelle, zeige die richtige Form und gebe dir einen kurzen neuen Versuch."
        return f"Kurzregel – {topic}: {rule_de} Beispiel: „{example}“ Bilde jetzt einen eigenen Satz."

    if language == "en":
        if wants_exercise:
            return f"{level} practice — {topic}: Put these words in order: “{words}”. Reply with the complete sentence."
        if wants_error:
            return "Send your German sentence and your original answer. I’ll mark one error, show the correction and give you one short retry."
        return f"Quick rule — {topic}: {rule_en} Example: “{example}” Now write one sentence of your own."

    if wants_exercise:
        return f"Упражнение уровня {level} — {topic}: собери предложение «{words}». Напиши готовую фразу."
    if wants_error:
        return "Пришли немецкое предложение и, если можешь, свой первоначальный ответ. Я отмечу одну конкретную ошибку, покажу правильный вариант и дам короткую попытку на закрепление."
    return f"Короткое правило — {topic}: {rule_ru} Пример: „{example}“ Теперь составь свою фразу."
