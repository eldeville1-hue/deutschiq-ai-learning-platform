"""Strictly verified word-order answers for the reviewed offline Tutor drills.

Only exact reviewed sentences are graded. This never awards XP or mastery.
"""
import re
from typing import Optional

from app.services.tutor_fallback import TOPIC_LESSONS
from app.services.tutor_exercise_bank import DRILLS
from app.services.tutor_clause_bank import CLAUSE_DRILLS

# Explicitly reviewed alternatives only; never infer grammatical equivalence.
REVIEWED_ALTERNATIVES = {
    "word_order": ("Ich lerne heute Deutsch.", "Deutsch lerne ich heute."),
    "genitive_prepositions": ("Wir bleiben wegen des Regens zu Hause.", "Zu Hause bleiben wir wegen des Regens."),
    "perfekt_auxiliary": ("Nach Berlin bin ich gefahren.", "Gefahren bin ich nach Berlin."),
    "haben_conjugation": ("Heute hast du Zeit.", "Zeit hast du heute."),
}


def _normalize_sentence(text: str) -> str:
    return re.sub(r"[.!?]+$", "", " ".join(text.strip().split())).casefold()


def grade_reviewed_word_order(exercise_text: str, learner_answer: str) -> Optional[dict]:
    """Return verified feedback only when the saved task uniquely matches a reviewed drill."""
    if not learner_answer.strip() or "?" in learner_answer or len(learner_answer) > 280:
        return None
    matched = [
        (topic, expected)
        for topic, (expected, words, *_rules) in TOPIC_LESSONS.items()
        if words.casefold() in exercise_text.casefold()
    ]
    bank_matches = [
        (topic, expected, alternatives)
        for _id, _level, topic, expected, words, alternatives in DRILLS
        if words.casefold() in exercise_text.casefold()
    ]
    clause_matches = [
        (topic, expected, alternatives)
        for _id, _level, topic, expected, words, alternatives in CLAUSE_DRILLS
        if words.casefold() in exercise_text.casefold()
    ]
    if len(matched) + len(bank_matches) + len(clause_matches) != 1:
        return None
    alternatives = (bank_matches or clause_matches)[0][2] if bank_matches or clause_matches else ()
    if bank_matches or clause_matches:
        selected = (bank_matches or clause_matches)[0]
        matched = [(selected[0], selected[1])]
    topic, expected = matched[0]
    normalized = _normalize_sentence(learner_answer)
    accepted = (expected, *alternatives, *REVIEWED_ALTERNATIVES.get(topic, ()))
    if any(normalized == _normalize_sentence(candidate) for candidate in accepted):
        return {"topic": topic, "correct": True, "expected": expected}

    # A valid topicalization can differ from every reviewed sample. In the
    # simple V2 drills, flag only demonstrably misplaced finite verbs when
    # the answer uses exactly the supplied words. Otherwise remain unsure.
    finite_verbs = {"word_order": "lerne", "haben_conjugation": "hast"}
    finite = finite_verbs.get(topic)
    if finite:
        tokens = normalized.split()
        expected_tokens = _normalize_sentence(expected).split()
        if sorted(tokens) == sorted(expected_tokens) and tokens.count(finite) == 1:
            if tokens.index(finite) != 1:
                return {"topic": topic, "correct": False, "expected": expected, "reason": "verb_position"}
    # Diagnose only a narrow, provable punctuation omission: the exact
    # reviewed sentence with its sole clause-boundary comma removed.
    if topic in ("weil_clause", "obwohl_clause", "damit_clause", "konjunktiv_ii"):
        for candidate in accepted:
            if candidate.count(",") == 1 and normalized == _normalize_sentence(candidate.replace(",", "")):
                return {
                    "topic": topic, "correct": False, "expected": expected,
                    "reason": "missing_clause_comma",
                }
    return {"topic": topic, "correct": None, "expected": expected}

# Topic-specific reminders are safe even when we cannot determine the precise
# mistake. Never present them as a diagnosis of a particular learner answer.
TOPIC_HINTS = {
    "word_order": {
        "ru": "Подсказка: в главном предложении спрягаемый глагол обычно стоит на второй позиции.",
        "de": "Tipp: Im Hauptsatz steht das konjugierte Verb normalerweise an zweiter Position.",
        "en": "Hint: In a main clause, the conjugated verb usually takes second position.",
    },
    "articles": {
        "ru": "Подсказка: проверь артикль и род существительного.",
        "de": "Tipp: Prüfe den Artikel und das Genus des Nomens.",
        "en": "Hint: Check the article and the noun's grammatical gender.",
    },
    "dative_case": {
        "ru": "Подсказка: helfen требует Dativ — проверь форму артикля.",
        "de": "Tipp: Helfen verlangt den Dativ. Prüfe die Artikelform.",
        "en": "Hint: Helfen takes the dative case. Check the article form.",
    },
    "genitive_prepositions": {
        "ru": "Подсказка: после wegen в нормативном немецком часто используется Genitiv.",
        "de": "Tipp: Nach wegen steht in der Standardsprache häufig der Genitiv.",
        "en": "Hint: In standard German, wegen is often followed by the genitive.",
    },
    "perfekt_auxiliary": {
        "ru": "Подсказка: многие глаголы движения образуют Perfekt с sein.",
        "de": "Tipp: Viele Bewegungsverben bilden das Perfekt mit sein.",
        "en": "Hint: Many movement verbs use sein in the Perfekt.",
    },
    "haben_conjugation": {
        "ru": "Подсказка: с du глагол haben принимает форму hast.",
        "de": "Tipp: Bei du lautet die Form von haben: hast.",
        "en": "Hint: With du, haben becomes hast.",
    },
}


CLAUSE_HINTS = {
    "weil_clause": {
        "ru": "После weil спрягаемый глагол стоит в конце придаточного предложения.",
        "de": "Nach weil steht das konjugierte Verb am Ende des Nebensatzes.",
        "en": "After weil, the finite verb goes at the end of the subordinate clause.",
    },
    "obwohl_clause": {
        "ru": "После obwohl глагол стоит в конце придаточного; если придаточное первое, главное начинается с глагола.",
        "de": "Nach obwohl steht das Verb am Ende des Nebensatzes. Steht er zuerst, folgt das Hauptsatzverb direkt danach.",
        "en": "After obwohl, the verb goes last in the subordinate clause. If that clause comes first, the main-clause verb follows immediately.",
    },
    "damit_clause": {
        "ru": "Damit вводит цель: спрягаемый глагол в придаточном стоит в конце.",
        "de": "Damit leitet einen Zwecksatz ein; das konjugierte Verb steht am Ende.",
        "en": "Damit introduces a purpose clause; its finite verb comes last.",
    },
    "konjunktiv_ii": {
        "ru": "Для нереальной ситуации используй hätte/wäre или würde + Infinitiv; после wenn глагол стоит в конце.",
        "de": "Für hypothetische Situationen nutze hätte/wäre oder würde + Infinitiv; nach wenn steht das Verb am Ende.",
        "en": "For hypothetical situations, use hätte/wäre or würde + infinitive; after wenn, the verb goes last.",
    },
}
TOPIC_HINTS.update(CLAUSE_HINTS)


CLAUSE_PUNCTUATION_HINTS = {
    "ru": "Между главным и придаточным предложениями нужна запятая.",
    "de": "Zwischen Hauptsatz und Nebensatz muss ein Komma stehen.",
    "en": "A comma is required between the main clause and the subordinate clause.",
}


def verified_specific_feedback(topic: str, reason: str, language: str) -> str:
    """Use an error-specific explanation only for a provably detected error."""
    lang = language if language in ("ru", "de", "en") else "en"
    if reason == "missing_clause_comma":
        return CLAUSE_PUNCTUATION_HINTS[lang] + " " + {
            "ru": "Добавь запятую и попробуй ещё раз.",
            "de": "Setze das Komma und versuche es erneut.",
            "en": "Add the comma and try again.",
        }[lang]
    return verified_retry_feedback(topic, lang)


def verified_retry_feedback(topic: str, language: str) -> str:
    """Give a reviewed topic hint without claiming to locate the exact error."""
    lang = language if language in ("ru", "de", "en") else "en"
    intro = {
        "ru": "Пока не совпадает с проверенными вариантами.",
        "de": "Das entspricht noch keiner geprüften Lösung.",
        "en": "This does not match a reviewed answer yet.",
    }[lang]
    outro = {
        "ru": "Попробуй ещё раз.",
        "de": "Versuche es noch einmal.",
        "en": "Try again.",
    }[lang]
    return f"{intro} {TOPIC_HINTS[topic][lang]} {outro}"


def unverified_answer_feedback(language: str) -> str:
    """Do not mark unreviewed grammatical alternatives as incorrect."""
    return {
        "ru": "Этот вариант не входит в проверенные ответы. Я не могу надёжно определить, правильный ли он. Попробуй другую формулировку или запроси подсказку.",
        "de": "Diese Variante ist nicht unter den geprüften Antworten. Ich kann sie nicht zuverlässig bewerten. Versuche eine andere Formulierung oder fordere einen Tipp an.",
        "en": "This variant is not among the reviewed answers. I cannot reliably grade it. Try another wording or request a hint.",
    }[language if language in ("ru", "de", "en") else "en"]
