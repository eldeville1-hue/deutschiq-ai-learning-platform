"""Strictly verified word-order answers for the reviewed offline Tutor drills.

Only exact reviewed sentences are graded. This never awards XP or mastery.
"""
import re
from typing import Optional

from app.services.tutor_fallback import TOPIC_LESSONS

# Explicitly reviewed alternatives only; never infer grammatical equivalence.
REVIEWED_ALTERNATIVES = {
    "word_order": ("Ich lerne heute Deutsch.",),
    "genitive_prepositions": ("Wir bleiben wegen des Regens zu Hause.",),
    "perfekt_auxiliary": ("Nach Berlin bin ich gefahren.",),
    "haben_conjugation": ("Heute hast du Zeit.",),
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
    if len(matched) != 1:
        return None
    topic, expected = matched[0]
    normalized = _normalize_sentence(learner_answer)
    accepted = (expected, *REVIEWED_ALTERNATIVES.get(topic, ()))
    correct = any(normalized == _normalize_sentence(candidate) for candidate in accepted)
    return {"topic": topic, "correct": correct, "expected": expected}

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
