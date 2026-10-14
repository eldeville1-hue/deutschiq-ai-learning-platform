"""Read-only helpers for identifying due spaced-repetition reviews."""
from datetime import datetime
from app.models.progress import UserProgress


def due_review_dates(review_dates, *, as_of=None):
    """Return review timestamps due on or before as_of, oldest first.

    Missing schedules are not considered due. Naive timestamps follow the
    existing scheduler's local-naive datetime convention.
    """
    now = as_of or datetime.now()
    if not review_dates:
        return []
    return sorted(date for date in review_dates if date <= now)


def due_reviews(db, user_id: int, *, as_of=None):
    """Return completed progress records with at least one due review.

    This is intentionally read-only: listing reviews must not reschedule them.
    """
    now = as_of or datetime.now()
    records = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.completed.is_(True),
    ).all()
    return sorted(
        (progress for progress in records if due_review_dates(progress.review_dates, as_of=now)),
        key=lambda progress: due_review_dates(progress.review_dates, as_of=now)[0],
    )
