from app.services.misconception_feedback import misconception_feedback


def test_evaluator_error_categories_have_specific_multilingual_hints():
    for tag in ("missing_words", "answer_mismatch", "word_order", "conjugation", "auxiliary", "case", "article", "adjective", "preposition", "negation", "infinitive"):
        hints = [misconception_feedback(tag, lang) for lang in ("ru", "de", "en")]
        assert all(hints)
        assert len(set(hints)) == 3
        assert all(hint != misconception_feedback("unknown", lang) for hint, lang in zip(hints, ("ru", "de", "en")))


def test_unknown_error_keeps_safe_general_hint():
    assert misconception_feedback("unknown", "en") == misconception_feedback(None, "en")
