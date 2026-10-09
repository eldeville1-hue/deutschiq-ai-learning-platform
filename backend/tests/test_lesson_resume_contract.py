"""Regression checks for lesson resume implementation and model contract.

These lightweight checks deliberately avoid database and external service setup.
"""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LESSON_API = ROOT / "app" / "api" / "endpoints" / "lesson.py"
LEARNING_MODEL = ROOT / "app" / "models" / "learning.py"


def test_resume_uses_existing_session_timestamp_column():
    source = LESSON_API.read_text(encoding="utf-8")
    model = LEARNING_MODEL.read_text(encoding="utf-8")
    assert "started_at = Column(" in model
    assert "LearningSession.started_at.desc()" in source
    assert "LearningSession.created_at" not in source


def test_start_returns_resume_cursor_for_new_and_existing_sessions():
    source = LESSON_API.read_text(encoding="utf-8")
    assert '"next_exercise_index": 0' in source
    assert '"next_exercise_index": next_index' in source
    assert 'ExerciseAttempt.session_id == existing.id' in source
    assert 'if attempt.correct and attempt.exercise_index >= 0' in source


def test_resume_queries_are_scoped_to_authenticated_user_and_lesson():
    source = LESSON_API.read_text(encoding="utf-8")
    start = source.split('async def start_lesson(', 1)[1].split('# Получить урок', 1)[0]
    assert 'assert_owner(authenticated_id, data.user_id)' in start
    assert 'LearningSession.user_id == user.id' in start
    assert 'LearningSession.lesson_id == lesson.id' in start
    assert 'LearningSession.status == "active"' in start


def test_cursor_calculation_for_reopened_lesson():
    """Execute the production helper without importing API/database dependencies."""
    import ast
    from types import SimpleNamespace

    source = LESSON_API.read_text(encoding="utf-8")
    function = next(
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == "next_unanswered_exercise_index"
    )
    namespace = {}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(LESSON_API), "exec"), namespace)
    cursor = namespace["next_unanswered_exercise_index"]
    attempt = lambda index, correct: SimpleNamespace(exercise_index=index, correct=correct)

    assert cursor([]) == 0
    assert cursor([attempt(0, True), attempt(1, True)]) == 2
    assert cursor([attempt(0, True), attempt(1, False)]) == 1
    assert cursor([attempt(0, True), attempt(1, False), attempt(1, True)]) == 2
    assert cursor([attempt(2, True)]) == 0
    assert cursor([attempt(-1, True)]) == 0
