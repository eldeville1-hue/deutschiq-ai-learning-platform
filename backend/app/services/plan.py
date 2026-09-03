# backend/app/services/plan.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.diagnostic import DiagnosticResult
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.learning import TopicMastery
from datetime import datetime, timezone

def generate_plan(db: Session, user_id: int, limit: int = 30):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    
    diag = db.query(DiagnosticResult).filter(
        DiagnosticResult.user_id == user_id
    ).order_by(DiagnosticResult.created_at.desc()).first()
    
    weak_points = diag.weak_points if diag and diag.weak_points else {}
    mastery_rows = db.query(TopicMastery).filter(TopicMastery.user_id == user_id).all()
    mastery = {row.topic: row.mastery for row in mastery_rows}
    due = {row.topic for row in mastery_rows if row.next_review_at and row.next_review_at <= datetime.now(timezone.utc)}
    lessons = db.query(Lesson).filter(Lesson.is_active == True).all()
    roadmap = [lesson for lesson in lessons if isinstance(lesson.content, dict) and lesson.content.get("day")]
    if roadmap:
        # Weak diagnostic topics come first; roadmap order breaks equal priorities.
        roadmap.sort(key=lambda lesson: (
            0 if lesson.topic in due else 1,
            mastery.get(lesson.topic, 101),
            -sum(weak_points.get(tag, 0) for tag in (lesson.weak_point_tags or [])),
            lesson.content.get("day", 999),
        ))
        return roadmap[:limit]

    weak_tags = list(weak_points.keys())
    if weak_tags:
        lessons = [lesson for lesson in lessons if set(lesson.weak_point_tags or []) & set(weak_tags)]
    
    def priority(lesson):
        return sum(weak_points.get(tag, 0) for tag in lesson.weak_point_tags)
    
    lessons.sort(key=priority, reverse=True)
    
    return lessons[:limit]
