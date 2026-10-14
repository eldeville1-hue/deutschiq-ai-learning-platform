"""Deterministic checks for due-review selection."""
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from app.services.srs_due import due_review_dates, due_reviews


def test_due_review_dates_handles_empty_future_and_overdue():
    now = datetime(2026, 10, 14, 10, 0)
    assert due_review_dates(None, as_of=now) == []
    assert due_review_dates([], as_of=now) == []
    assert due_review_dates([now + timedelta(days=1)], as_of=now) == []
    assert due_review_dates([
        now + timedelta(days=2), now - timedelta(days=3), now,
    ], as_of=now) == [now - timedelta(days=3), now]


def test_due_reviews_only_completed_and_ordered_by_oldest_due_date():
    now = datetime(2026, 10, 14, 10, 0)
    older = MagicMock(completed=True, review_dates=[now - timedelta(days=5)])
    recent = MagicMock(completed=True, review_dates=[now - timedelta(hours=1)])
    future = MagicMock(completed=True, review_dates=[now + timedelta(days=1)])
    unscheduled = MagicMock(completed=True, review_dates=[])
    query = MagicMock()
    query.filter.return_value.all.return_value = [recent, future, unscheduled, older]
    db = MagicMock()
    db.query.return_value = query
    assert due_reviews(db, 1, as_of=now) == [older, recent]
    db.commit.assert_not_called()
