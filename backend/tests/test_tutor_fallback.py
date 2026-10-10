from app.services.tutor_fallback import fallback_answer


def test_russian_exercise_is_actionable_and_level_aware():
    answer = fallback_answer("Дай упражнение", "ru", "B1", ["articles"])
    assert "Упражнение" in answer
    assert "B1" in answer
    assert "полным" not in answer


def test_german_error_flow_asks_for_the_sentence():
    answer = fallback_answer("Erkläre meinen Fehler", "de", "A2", ["word_order"])
    assert "Schick mir" in answer
    assert "nicht zuverlässig individuell korrigieren" in answer


def test_rule_fallback_uses_personal_topic():
    answer = fallback_answer("Объясни правило", "ru", "A2", ["dative_case"])
    assert "дательный падеж" in answer
    assert "Ich helfe dem Mann" in answer
    assert "Heute lerne ich Deutsch" not in answer


def test_explicit_question_topic_overrides_weak_skill():
    answer = fallback_answer("Explain Perfekt", "en", "B1", ["articles"])
    assert "Ich bin nach Berlin gefahren" in answer
    assert "articles" not in answer


def test_exercise_matches_the_named_topic():
    answer = fallback_answer("Дай упражнение на Dativ", "ru", "A2", ["word_order"])
    assert "dem Mann" in answer
    assert "heute / ich / Deutsch / lerne" not in answer


def test_offline_correction_does_not_promise_ai_feedback():
    for language, question, expected in (
        ("ru", "Исправь ошибку", "не могу надёжно"),
        ("de", "Korrigiere meinen Fehler", "nicht zuverlässig"),
        ("en", "Correct my mistake", "cannot reliably"),
    ):
        answer = fallback_answer(question, language, "B2", ["articles"])
        assert expected in answer
