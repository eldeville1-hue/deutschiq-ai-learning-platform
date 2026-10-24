"""Objective length-only feedback for saved open-ended writing tasks."""
import re
from app.services.tutor_writing_bank import WRITING_PROMPTS

def writing_length_feedback(exercise_text: str, answer: str, language: str):
    """Return a non-evaluative length check only for an identifiable writing task."""
    matches = [row for row in WRITING_PROMPTS if row[2] in exercise_text]
    if len(matches) != 1 or not answer.strip():
        return None
    words = re.findall(r"\b[^\W_]+(?:[-'][^\W_]+)*\b", answer, flags=re.UNICODE)
    count = len(words)
    low, high = (int(value) for value in matches[0][4].split("-"))
    status = "short" if count < low else "long" if count > high else "within"
    lang = language if language in ("ru", "de", "en") else "en"
    templates = {
        "ru": {
            "short": "Текст пока короче рекомендуемого объёма.",
            "long": "Текст длиннее рекомендуемого объёма.",
            "within": "Объём текста соответствует рекомендации.",
            "note": "Это только подсчёт слов, не оценка содержания, грамматики или уровня.",
        },
        "de": {
            "short": "Der Text ist kuerzer als empfohlen.",
            "long": "Der Text ist laenger als empfohlen.",
            "within": "Die Textlaenge liegt im empfohlenen Bereich.",
            "note": "Dies ist nur eine Wortzaehlung, keine Bewertung von Inhalt, Grammatik oder Sprachniveau.",
        },
        "en": {
            "short": "The text is shorter than recommended.",
            "long": "The text is longer than recommended.",
            "within": "The text length is within the recommended range.",
            "note": "This checks word count only, not content, grammar or language level.",
        },
    }
    localized = templates[lang]
    return f"{count} / {low}-{high} words. {localized[status]} {localized['note']}"
