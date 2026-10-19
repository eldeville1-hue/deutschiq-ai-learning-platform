"""Server-side contract checks for learner-selected B2 data scenarios."""
import pytest
from fastapi import HTTPException
from app.api.endpoints.lesson import CheckAnswerRequest, resolve_practice_variant
from app.content.b2_curriculum import B2_CURRICULUM, build_b2_content


def data_exercise():
    row = next(row for row in B2_CURRICULUM if row[2] == "data_description")
    lesson = build_b2_content(row)
    return next(item for item in lesson["exercises"] if item["id"] == "data_description-dialogue")


@pytest.mark.parametrize("variant_id,earlier,later,delta,term", [
    ("data_description-decrease", 60, 45, -15, "sank"),
    ("data_description-stable", 40, 40, 0, "unverändert"),
])
def test_selected_variant_uses_server_owned_figures_and_model(variant_id, earlier, later, delta, term):
    original = data_exercise()
    selected = resolve_practice_variant(original, original, variant_id, "en")
    figures = selected["data_figures"]
    assert figures["earlier"]["percent"] == earlier
    assert figures["later"]["percent"] == later
    assert figures["later"]["percent"] - figures["earlier"]["percent"] == delta
    assert term in selected["answer"]
    assert selected["accepted_answers"] == [selected["answer"]]
    assert selected["question"] != original["question"]


def test_invalid_variant_is_rejected_without_using_client_figures():
    original = data_exercise()
    with pytest.raises(HTTPException) as error:
        resolve_practice_variant(original, original, "fake-data-variant", "en")
    assert error.value.status_code == 422


def test_variant_not_allowed_for_guided_retry():
    original = data_exercise()
    with pytest.raises(HTTPException) as error:
        resolve_practice_variant(original, original, "data_description-stable", "en", retry=True)
    assert error.value.status_code == 422


def test_check_answer_request_accepts_variant_identifier():
    request = CheckAnswerRequest(
        user_id=1, lesson_id=77, exercise_index=3, answer="Der Anteil blieb unverändert.",
        session_id="test-session", practice_variant_id="data_description-stable",
    )
    assert request.practice_variant_id == "data_description-stable"
