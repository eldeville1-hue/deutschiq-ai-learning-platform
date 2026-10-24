from typing import Sequence
from app.services.tutor_exercise_bank import DRILLS
from app.services.tutor_clause_bank import CLAUSE_DRILLS
from app.services.tutor_transformation_bank import TRANSFORMATIONS
from app.services.tutor_writing_bank import WRITING_PROMPTS, WRITING_CRITERIA


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


def fallback_answer(question: str, lang: str, level: str, topics: Sequence[str], recent_answers: Sequence[str] = ()) -> str:
    """Return a small, actionable lesson when the external AI is unavailable."""
    lowered = question.casefold()
    topic_key = _detect_topic(question, topics)
    wants_practice = any(word in lowered for word in ('упраж', 'задани', 'übung', 'aufgabe', 'exercise', 'practice', 'quiz'))
    if wants_practice and not any(word in lowered for word in ('genitiv', 'genitive', 'dativ', 'dative', 'artikel', 'article', 'артикл', 'wortstellung', 'word order', 'порядок слов', 'perfekt', 'haben')):
        candidates = list(dict.fromkeys([topic for topic in topics if topic in TOPIC_LESSONS] + list(TOPIC_LESSONS)))
        for candidate in candidates:
            if not any(TOPIC_LESSONS[candidate][1] in previous for previous in recent_answers[-12:]):
                topic_key = candidate
                break
    example, words, rule_en, rule_de, rule_ru = TOPIC_LESSONS[topic_key]
    wants_writing = any(term in lowered for term in (
        "writing task", "writing exercise", "schreibaufgabe", "schreibübung",
        "письменное задание", "письменное упражнение", "сочинение", "essay"
    ))
    if wants_writing and level.upper()[:2] in ("B1", "B2"):
        recent_text = " ".join(recent_answers[-24:])
        options = [row for row in WRITING_PROMPTS if row[1] == level.upper()[:2]]
        selected = next((row for row in options if row[2] not in recent_text), options[0])
        language = lang if lang in ("ru", "de", "en") else "en"
        heading = {"ru": "Письменное задание", "de": "Schreibaufgabe", "en": "Writing task"}[language]
        count = {"ru": "слов", "de": "Wörter", "en": "words"}[language]
        return (
            f"{heading} {level}: {selected[2]} {selected[3]} "
            f"({selected[4]} {count}). {WRITING_CRITERIA[language]}"
        )
    wants_transformation = wants_practice and level.upper()[:2] == "B2" and any(
        term in lowered for term in ("transform", "umform", "перефраз", "преобраз", "rewrite")
    )
    if wants_transformation:
        recent_text = " ".join(recent_answers[-24:])
        selected = next(
            (row for row in TRANSFORMATIONS if row[4] not in recent_text),
            TRANSFORMATIONS[0],
        )
        instruction, source = selected[3], selected[4]
        language = lang if lang in ("ru", "de", "en") else "en"
        intro = {
            "ru": "Преобразуй предложения в одно, используя указанную конструкцию.",
            "de": "Forme die Sätze zu einem Satz um.",
            "en": "Combine the sentences into one using the requested structure.",
        }[language]
        return f"{intro} {instruction} {source} Напиши полный ответ." if language == "ru" else (
            f"{intro} {instruction} {source} Schreibe den ganzen Satz." if language == "de"
            else f"{intro} {instruction} {source} Write the complete sentence."
        )
    explicit_clause = any(term in lowered for term in (
        "weil", "obwohl", "damit", "konjunktiv", "subordinate", "nebensatz", "придаточ"
    ))
    explicit_existing_topic = any(term in lowered for term in (
        "genitiv", "genitive", "dativ", "dative", "artikel", "article",
        "wortstellung", "word order", "порядок слов", "perfekt", "haben"
    ))
    use_clause = explicit_clause or (bool(recent_answers) and not explicit_existing_topic)
    if wants_practice and use_clause and level.upper()[:2] in ("B1", "B2"):
        recent_text = " ".join(recent_answers[-24:])
        clause_candidates = [row for row in CLAUSE_DRILLS if row[1] == level.upper()[:2]]
        selected_clause = next(
            (row for row in clause_candidates if row[4] not in recent_text),
            clause_candidates[0],
        )
        if selected_clause[4] not in recent_text:
            words = selected_clause[4]
            topic_key = selected_clause[2]
            example = selected_clause[3]
    if wants_practice:
        level_key = level.upper()[:2]
        eligible = [row for row in DRILLS if row[1] == level_key and row[2] == topic_key]
        if not eligible:
            eligible = [row for row in DRILLS if row[1] == level_key]
        if eligible and topic_key not in ('weil_clause', 'obwohl_clause', 'damit_clause', 'konjunktiv_ii'):
            recent_text = " ".join(recent_answers[-24:])
            chosen = next((row for row in eligible if row[4] not in recent_text), eligible[0])
            example, words = chosen[3], chosen[4]
    language = lang if lang in ("ru", "de", "en") else "en"
    names = TOPIC_NAMES.get(topic_key, {"ru": topic_key.replace("_", " "), "de": topic_key.replace("_", " "), "en": topic_key.replace("_", " ")})
    topic = names[language] if topic_key in TOPIC_NAMES else {"ru": "придаточные предложения / Konjunktiv II", "de": "Nebensätze / Konjunktiv II", "en": "subordinate clauses / Konjunktiv II"}[language]
    wants_exercise = any(word in lowered for word in ("упраж", "задани", "übung", "aufgabe", "exercise", "practice", "quiz"))
    wants_error = any(word in lowered for word in ("ошиб", "fehler", "korrig", "error", "mistake", "correct"))

    if language == "de":
        if wants_exercise:
            return f"Übung auf Niveau {level} – {topic}: Ordne „{words}“. Antworte mit dem vollständigen Satz."
        if wants_error:
            return "Schick mir bitte den deutschen Satz und – wenn möglich – deine ursprüngliche Antwort. Ohne KI kann ich deinen Satz nicht zuverlässig individuell korrigieren. Ich kann dir aber eine Regel und eine passende Übung zeigen."
        return f"Kurzregel – {topic}: {rule_de} Beispiel: „{example}“ Bilde jetzt einen eigenen Satz."

    if language == "en":
        if wants_exercise:
            return f"{level} practice — {topic}: Put these words in order: “{words}”. Reply with the complete sentence."
        if wants_error:
            return "Send your German sentence and your original answer. Without AI, I cannot reliably correct your individual sentence. I can still show you a grammar rule and a matching exercise."
        return f"Quick rule — {topic}: {rule_en} Example: “{example}” Now write one sentence of your own."

    if wants_exercise:
        return f"Упражнение уровня {level} — {topic}: собери предложение «{words}». Напиши готовую фразу."
    if wants_error:
        return "Пришли немецкое предложение и, если можешь, свой первоначальный ответ. Без ИИ я не могу надёжно исправить именно твоё предложение. Но могу объяснить правило и дать упражнение по теме."
    return f"Короткое правило — {topic}: {rule_ru} Пример: „{example}“ Теперь составь свою фразу."
