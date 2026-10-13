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
