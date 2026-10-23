"""Conservative session transitions; no model-generated answer is automatically graded."""
from app.models.tutor_practice import TutorPracticeSession
from app.services.tutor_turn_state import classify_tutor_turn

EXERCISE_MARKERS = ("übung", "aufgabe", "exercise", "practice", "упражнен", "задани", "ordne", "put these words", "собери предложение")


def update_practice_session(db, user_id: int, language: str, learner_message: str, tutor_answer: str) -> None:
    session = db.query(TutorPracticeSession).filter(
        TutorPracticeSession.user_id == user_id,
        TutorPracticeSession.language == language,
    ).first()
    turn = classify_tutor_turn(session.exercise_text, learner_message) if session and session.state in ("awaiting_attempt", "feedback_given") else "conversation"
    is_new_exercise = any(marker in tutor_answer.casefold() for marker in EXERCISE_MARKERS)
    # Every plausible answer counts as an attempt, even if the tutor's
    # feedback happens to include the word "exercise" or another task marker.
    if session and turn == "attempt":
        session.attempts += 1
        # Keep the task for a correction attempt after feedback as well. The model
        # cannot reliably certify a correct answer or completed exercise.
        session.state = "feedback_given"
        return
    if is_new_exercise:
        if session is None:
            session = TutorPracticeSession(
                user_id=user_id, language=language, exercise_text=tutor_answer,
                state="awaiting_attempt", attempts=0,
            )
            db.add(session)
        else:
            session.exercise_text = tutor_answer
            session.state = "awaiting_attempt"
            session.attempts = 0
    elif session and turn == "new_request":
        session.state = "interrupted"
