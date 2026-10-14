# backend/app/services/srs.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.progress import UserProgress

def schedule_review(db: Session, user_id: int, lesson_id: int):
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.lesson_id == lesson_id
    ).first()
    if progress:
        # Keep an existing review plan stable when a completion response is
        # retried or an already-completed lesson is opened again.
        if progress.review_dates:
            return
        intervals = [1, 3, 7, 14, 30]
        now = datetime.now()
        progress.review_dates = [(now + timedelta(days=d)) for d in intervals]
        db.commit()

