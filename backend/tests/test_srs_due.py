"""Deterministic checks for due-review selection."""
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from app.services.srs_due import due_review_dates, due_reviews, consume_due_review


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


def test_consuming_due_dates_preserves_future_and_is_idempotent():
    now = datetime(2026, 10, 14, 10, 0)
    upcoming = now + timedelta(days=3)
    progress = MagicMock(review_dates=[now - timedelta(days=2), now, upcoming])
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = progress
    assert consume_due_review(db, 1, 77, as_of=now) is True
    assert progress.review_dates == [upcoming]
    assert consume_due_review(db, 1, 77, as_of=now) is False
    assert progress.review_dates == [upcoming]
    db.commit.assert_not_called()


def test_consuming_missing_review_is_noop():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    assert consume_due_review(db, 1, 77, as_of=datetime(2026, 10, 14)) is False
    db.commit.assert_not_called()
