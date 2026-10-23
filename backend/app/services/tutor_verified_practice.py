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
