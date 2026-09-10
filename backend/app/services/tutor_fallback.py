from typing import Sequence


TOPIC_NAMES = {
    "articles": ("артикли", "Artikel"),
    "word_order": ("порядок слов", "Wortstellung"),
    "dative_case": ("дательный падеж", "Dativ"),
    "genitive_prepositions": ("предлоги с Genitiv", "Präpositionen mit Genitiv"),
    "perfekt_auxiliary": ("Perfekt", "Perfekt"),
    "haben_conjugation": ("спряжение haben", "Konjugation von haben"),
}


def fallback_answer(question: str, lang: str, level: str, topics: Sequence[str]) -> str:
    """Return a small, actionable lesson when the external AI is unavailable."""
    lowered = question.casefold()
    topic_key = topics[0] if topics else "word_order"
    topic_ru, topic_de = TOPIC_NAMES.get(
        topic_key,
        (topic_key.replace("_", " "), topic_key.replace("_", " ")),
    )
    wants_exercise = any(word in lowered for word in ("упраж", "задани", "übung", "aufgabe"))
    wants_error = any(word in lowered for word in ("ошиб", "fehler", "korrig"))

    if lang.startswith("de"):
        if wants_exercise:
            return f"Übung für Niveau {level} – {topic_de}: Setze die Wörter richtig zusammen: „heute / ich / Deutsch / lerne“. Antworte nur mit dem vollständigen Satz; danach korrigiere ich ihn."
        if wants_error:
            return "Schick mir bitte den deutschen Satz und – wenn möglich – deine ursprüngliche Antwort. Ich markiere genau eine Fehlerstelle, zeige die richtige Form und gebe dir einen kurzen neuen Versuch."
        return f"Kurzregel zu {topic_de}: Im deutschen Hauptsatz steht das konjugierte Verb normalerweise an Position 2. Beispiele: „Heute lerne ich Deutsch.“ und „Am Abend übt sie Grammatik.“ Schreib jetzt einen eigenen Satz."

    if wants_exercise:
        return f"Упражнение для уровня {level} — {topic_ru}: собери правильное предложение из слов «heute / ich / Deutsch / lerne». Напиши только готовую фразу, и я сразу её проверю."
    if wants_error:
        return "Пришли немецкое предложение и, если можешь, свой первоначальный ответ. Я отмечу одну конкретную ошибку, покажу правильный вариант и дам короткую попытку на закрепление."
    return f"Короткое правило по теме «{topic_ru}»: в немецком главном предложении спрягаемый глагол обычно стоит на втором месте. Примеры: „Heute lerne ich Deutsch.“ и „Am Abend übt sie Grammatik.“ Теперь составь одну свою фразу."
