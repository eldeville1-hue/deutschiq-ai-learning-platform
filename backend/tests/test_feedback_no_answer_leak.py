"""Hints for a retry should not disclose the answer tokens."""
from app.services.lesson_coaching import feedback_focus


def test_missing_word_feedback_does_not_leak_answer():
    for language in ("ru", "de", "en"):
        hint = feedback_focus("missing_words", ["gegangen"], [], language)
        assert "gegangen" not in hint
        assert hint.strip()


def test_extra_word_feedback_does_not_quote_student_tokens():
    for language in ("ru", "de", "en"):
        hint = feedback_focus("answer_mismatch", [], ["SECRET_TOKEN"], language)
        assert "SECRET_TOKEN" not in hint
        assert hint.strip()


def test_specific_grammar_feedback_remains_targeted():
    assert "verb" in feedback_focus("conjugation", ["ist"], [], "en").lower()
