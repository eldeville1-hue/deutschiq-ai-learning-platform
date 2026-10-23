"""Conservative session transitions; no model-generated answer is automatically graded."""
from app.models.tutor_practice import TutorPracticeSession
from app.services.tutor_turn_state import classify_tutor_turn

EXERCISE_MARKERS = ("übung", "aufgabe", "exercise", "practice", "упражнен", "задани", "ordne", "put these words", "собери предложение")


def update_practice_session(db, user_id: int, language: str, learner_message: str, tutor_answer: str) -> None:
    session = db.query(TutorPracticeSession).filter(
        TutorPracticeSession.user_id == user_id,
        TutorPracticeSession.language == language,
    ).first()
    turn = classify_tutor_turn(session.exercise_text, learner_message) if session and session.state == "awaiting_attempt" else "conversation"
    is_new_exercise = any(marker in tutor_answer.casefold() for marker in EXERCISE_MARKERS)
    # A correction that mentions the word "exercise" is not automatically a new task.
    if turn == "attempt" and not is_new_exercise:
        session.attempts += 1
        session.state = "feedback_given"
        return
    if is_new_exercise:
        if session is None:
            session = TutorPracticeSession(user_id=user_id, language=language, exercise_text=tutor_answer)
            db.add(session)
        else:
            session.exercise_text = tutor_answer
            session.state = "awaiting_attempt"
            session.attempts = 0
    elif session and turn == "new_request":
        session.state = "interrupted"
