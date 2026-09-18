from typing import Sequence


TOPIC_NAMES = {
    "articles": {"ru": "артикли", "de": "Artikel", "en": "articles"},
    "word_order": {"ru": "порядок слов", "de": "Wortstellung", "en": "word order"},
    "dative_case": {"ru": "дательный падеж", "de": "Dativ", "en": "the dative case"},
    "genitive_prepositions": {"ru": "предлоги с Genitiv", "de": "Präpositionen mit Genitiv", "en": "genitive prepositions"},
    "perfekt_auxiliary": {"ru": "Perfekt", "de": "Perfekt", "en": "the perfect tense"},
    "haben_conjugation": {"ru": "спряжение haben", "de": "Konjugation von haben", "en": "conjugating haben"},
}


def fallback_answer(question: str, lang: str, level: str, topics: Sequence[str]) -> str:
    """Return a small, actionable lesson when the external AI is unavailable."""
    lowered = question.casefold()
    topic_key = topics[0] if topics else "word_order"
    language = lang if lang in ("ru", "de", "en") else "en"
    names = TOPIC_NAMES.get(topic_key, {"ru": topic_key.replace("_", " "), "de": topic_key.replace("_", " "), "en": topic_key.replace("_", " ")})
    topic = names[language]
    wants_exercise = any(word in lowered for word in ("упраж", "задани", "übung", "aufgabe", "exercise", "practice", "quiz"))
    wants_error = any(word in lowered for word in ("ошиб", "fehler", "korrig", "error", "mistake", "correct"))

    if lang.startswith("de"):
        if wants_exercise:
            return f"Übung auf Niveau {level} – {topic}: Ordne „heute / ich / Deutsch / lerne“. Antworte mit dem vollständigen Satz."
        if wants_error:
            return "Schick mir bitte den deutschen Satz und – wenn möglich – deine ursprüngliche Antwort. Ich markiere genau eine Fehlerstelle, zeige die richtige Form und gebe dir einen kurzen neuen Versuch."
        return f"Kurzregel – {topic}: Im Hauptsatz steht das konjugierte Verb meist an Position 2. Beispiel: „Heute lerne ich Deutsch.“ Bilde jetzt einen eigenen Satz."

    if language == "en":
        if wants_exercise:
            return f"{level} practice — {topic}: Put these words in order: “heute / ich / Deutsch / lerne”. Reply with the complete sentence."
        if wants_error:
            return "Send your German sentence and your original answer. I’ll mark one error, show the correction and give you one short retry."
        return f"Quick rule — {topic}: In a German main clause, the conjugated verb usually takes position 2. Example: “Heute lerne ich Deutsch.” Now write one sentence of your own."

    if wants_exercise:
        return f"Упражнение уровня {level} — {topic}: собери предложение «heute / ich / Deutsch / lerne». Напиши готовую фразу."
    if wants_error:
        return "Пришли немецкое предложение и, если можешь, свой первоначальный ответ. Я отмечу одну конкретную ошибку, покажу правильный вариант и дам короткую попытку на закрепление."
    return f"Короткое правило — {topic}: в немецком главном предложении спрягаемый глагол обычно стоит на втором месте. Пример: „Heute lerne ich Deutsch.“ Теперь составь свою фразу."
