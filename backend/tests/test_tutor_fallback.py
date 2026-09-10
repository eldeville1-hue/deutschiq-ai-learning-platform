from app.services.tutor_fallback import fallback_answer


def test_russian_exercise_is_actionable_and_level_aware():
    answer = fallback_answer("Дай упражнение", "ru", "B1", ["articles"])
    assert "Упражнение" in answer
    assert "B1" in answer
    assert "полным" not in answer


def test_german_error_flow_asks_for_the_sentence():
    answer = fallback_answer("Erkläre meinen Fehler", "de", "A2", ["word_order"])
    assert "Schick mir" in answer
    assert "Fehlerstelle" in answer


def test_rule_fallback_uses_personal_topic():
    answer = fallback_answer("Объясни правило", "ru", "A2", ["dative_case"])
    assert "дательный падеж" in answer
    assert "Heute lerne ich Deutsch" in answer
