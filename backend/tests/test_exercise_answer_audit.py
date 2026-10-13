from app.services.content_quality import exercise_answer_audit


def test_valid_choice_with_authored_alternative_passes():
    content = {"exercises": [{
        "type": "context_choice", "question": "Choose the right form",
        "answer": "den", "accepted_answers": ["den"],
        "options": ["der", "den", "dem"],
    }]}
    assert exercise_answer_audit(content) == []


def test_choice_with_missing_correct_option_is_flagged():
    content = {"exercises": [{
        "type": "choose", "answer": "den", "options": ["der", "dem"],
    }]}
    assert "exercise:0:answer_not_in_options" in exercise_answer_audit(content)


def test_duplicate_choices_are_detected_even_with_whitespace_and_case():
    content = {"exercises": [{
        "type": "listening_choice", "answer": "Ja", "options": ["Ja", " ja "],
    }]}
    assert "exercise:0:duplicate_options" in exercise_answer_audit(content)


def test_malformed_alternatives_do_not_crash_audit():
    content = {"exercises": [{
        "type": "fill", "answer": "", "accepted_answers": ["", None],
    }]}
    issues = exercise_answer_audit(content)
    assert "exercise:0:invalid_accepted_answers" in issues
    assert "exercise:0:no_usable_answer" in issues


def test_invalid_exercise_and_missing_choices_are_reported():
    content = {"exercises": [
        None, {"type": "analogy_choice", "answer": "richtig", "options": ["richtig"]},
    ]}
    issues = exercise_answer_audit(content)
    assert "exercise:0:not_object" in issues
    assert "exercise:1:invalid_options" in issues
