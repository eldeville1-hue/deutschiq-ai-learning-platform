import asyncio
from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from app.api.endpoints.lesson import get_due_lesson_reviews


def test_due_lesson_api_filters_to_authenticated_user_and_limits():
    now = datetime.now()
    progress = SimpleNamespace(lesson_id=77, review_dates=[now - timedelta(days=2)])
    lesson = SimpleNamespace(id=77, title="Review lesson")
    user = SimpleNamespace(id=1)
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = user
    with patch("app.api.endpoints.lesson.due_reviews", return_value=[progress]) as due:
        with patch("app.api.endpoints.lesson.Lesson") as lesson_model:
            db.query.return_value.filter.return_value.all.return_value = [lesson]
            result = asyncio.run(get_due_lesson_reviews(limit=5, db=db, authenticated_id=9001))
            assert result["count"] == 1
            assert result["reviews"][0]["lesson_id"] == 77
            assert result["reviews"][0]["overdue_count"] == 1
            due.assert_called_once()
            assert due.call_args.args[1] == 1
    try:
        asyncio.run(get_due_lesson_reviews(limit=21, db=db, authenticated_id=9001))
        assert False, "Expected 422"
    except HTTPException as exc:
        assert exc.status_code == 422
