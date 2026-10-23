"""Conservative, deterministic hints for tutor practice turn continuity.

This is a conversation-state classifier, not an answer grader. It must never
award XP or assert correctness.
"""
from typing import Sequence

TASK_MARKERS = ("übung", "aufgabe", "exercise", "practice", "упражнен", "задани", "ordne", "put these words", "собери предложение", "ergänze", "übersetze")
NEW_REQUEST_MARKERS = ("explain", "объясни", "erkläre", "new exercise", "новое упражнение", "neue übung", "change topic", "другая тема", "anderes thema")


def classify_tutor_turn(previous_assistant: str, learner_message: str) -> str:
    """Return 'attempt', 'new_request', or 'conversation'.

    A previous exercise plus a short, non-command learner reply is a likely
    attempt; ambiguous turns remain ordinary conversation.
    """
    message = learner_message.strip().casefold()
    if not message:
        return "conversation"
    if any(marker in message for marker in NEW_REQUEST_MARKERS):
        return "new_request"
    if not any(marker in previous_assistant.casefold() for marker in TASK_MARKERS):
        return "conversation"
    if len(message) > 280 or "?" in message:
        return "conversation"
    return "attempt"


def practice_turn_instruction(state: str) -> str:
    if state == "attempt":
        return ("The learner likely attempted the exercise in your previous turn. "
                "Assess the response against that specific task before generating anything new. "
                "If incorrect, give a concise hint and invite one retry; if correct, confirm briefly "
                "and offer a different transfer exercise. Do not award XP or claim verified mastery.")
    if state == "new_request":
        return "The learner is requesting a change or explanation; follow their request instead of grading it."
    return ""
