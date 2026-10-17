"""Regression checks for conservative German exercise grading.

These checks intentionally distinguish an authored correct answer from
similar-looking German with different grammar or meaning.
"""
from app.services.answer_intelligence import evaluate_structured_answer


def grade(answer, expected, kind="fill", **extra):
    return evaluate_structured_answer(answer, {"type": kind, "answer": expected, **extra})


def test_authored_case_and_article_are_not_interchangeable():
    result = grade("Ich sehe der Mann", "Ich sehe den Mann", target_feature="case")
    assert result["evaluation_status"] == "verified"
    assert result["correct"] is False


def test_negation_reversing_meaning_is_not_accepted():
    result = grade("Ich habe Zeit", "Ich habe keine Zeit")
    assert result["correct"] is False


def test_one_missing_letter_can_change_a_german_verb():
    result = grade("Wir schreien", "Wir schreiben")
    assert result["correct"] is False


def test_unlisted_open_translation_is_not_marked_wrong_without_review():
    result = grade("Das ist ein schöner Tag", "Heute ist ein schöner Tag", kind="translate")
    assert result["evaluation_status"] == "uncertain"
    assert result["correct"] is False
    assert result["task_satisfied"] is None


def test_explicitly_authored_alternative_is_accepted():
    result = grade(
        "Heute ist ein schöner Tag", "Das ist ein schöner Tag",
        kind="translate", accepted_answers=["Heute ist ein schöner Tag"],
    )
    assert result["evaluation_status"] == "verified"
    assert result["correct"] is True


def test_punctuation_can_change_the_intended_meaning():
    result = grade("Wir essen Oma", "Wir essen, Oma!", kind="translate")
    assert result["evaluation_status"] == "uncertain"
    assert result["correct"] is False


def test_unlisted_open_answer_with_missing_negation_is_uncertain():
    result = grade("Ich kann kommen", "Ich kann nicht kommen", kind="translate")
    assert result["evaluation_status"] == "uncertain"
    assert result["correct"] is False


def test_unlisted_valid_word_order_variant_is_not_automatically_rejected():
    result = grade("Morgen fahre ich nach Berlin.", "Ich fahre morgen nach Berlin.", kind="translate")
    assert result["evaluation_status"] == "uncertain"
    assert result["task_satisfied"] is None
    assert result["correct"] is False


def test_authored_word_order_variant_receives_full_credit():
    result = grade(
        "Morgen fahre ich nach Berlin.", "Ich fahre morgen nach Berlin.",
        kind="translate", accepted_answers=["Morgen fahre ich nach Berlin."],
    )
    assert result["evaluation_status"] == "verified"
    assert result["correct"] is True


def test_changed_personal_pronoun_is_not_treated_as_equivalent():
    result = grade("Du lernst Deutsch.", "Ich lerne Deutsch.", kind="translate")
    assert result["evaluation_status"] == "uncertain"
    assert result["correct"] is False
    assert result["task_satisfied"] is None


def test_uncertain_open_answer_explains_that_it_is_not_confirmed_wrong():
    result = grade("Morgen fahre ich nach Berlin.", "Ich fahre morgen nach Berlin.", kind="translate")
    assert result["evaluation_status"] == "uncertain"
    assert "further review" in result["learner_feedback"]
    assert "confirmed errors" in result["learner_feedback"]


def test_missing_reference_gives_actionable_feedback_without_claiming_error():
    result = evaluate_structured_answer("Ich lerne Deutsch.", {"type": "translate"})
    assert result["evaluation_status"] == "needs_review"
    assert "no valid reference" in result["learner_feedback"]


def test_unlisted_dialogue_answer_requires_review_not_automatic_rejection():
    result = grade(
        "Ich heiße Anna und komme aus Hamburg.",
        "Ich heiße Leo und komme aus Berlin.",
        kind="dialogue",
    )
    assert result["evaluation_status"] == "uncertain"
    assert result["task_satisfied"] is None
    assert result["correct"] is False


def test_authored_dialogue_alternative_still_receives_credit():
    alternative = "Ich heiße Anna und komme aus Hamburg."
    result = grade(
        alternative, "Ich heiße Leo und komme aus Berlin.",
        kind="dialogue", accepted_answers=[alternative],
    )
    assert result["evaluation_status"] == "verified"
    assert result["correct"] is True


def test_dialogue_word_order_variant_has_no_confirmed_word_order_error():
    result = evaluate_structured_answer(
        "Morgen fahre ich nach Berlin.",
        {"type": "dialogue", "answer": "Ich fahre morgen nach Berlin.", "target_feature": "word_order"},
    )
    assert result["evaluation_status"] == "uncertain"
    assert result["task_satisfied"] is None
    assert not any(error["type"] == "word_order" for error in result["errors"])
