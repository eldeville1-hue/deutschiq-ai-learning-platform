# backend/app/services/plan.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.diagnostic import DiagnosticResult
from app.models.lesson import Lesson
from app.services.learning_route import roadmap_order

def generate_plan(db: Session, user_id: int, limit: int = 30):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    
    diag = db.query(DiagnosticResult).filter(
        DiagnosticResult.user_id == user_id
    ).order_by(DiagnosticResult.created_at.desc()).first()
    
    weak_points = diag.weak_points if diag and diag.weak_points else {}
    lessons = db.query(Lesson).filter(Lesson.is_active == True).all()
    roadmap = [lesson for lesson in lessons if isinstance(lesson.content, dict) and lesson.content.get("day")]
    if roadmap:
        # The visible route is pedagogical and stable. Personalization chooses a
        # recommendation; it must never renumber or reshuffle the curriculum.
        roadmap.sort(key=roadmap_order)
        return roadmap[:limit]

    weak_tags = list(weak_points.keys())
    if weak_tags:
        lessons = [lesson for lesson in lessons if set(lesson.weak_point_tags or []) & set(weak_tags)]
    
    def priority(lesson):
        return sum(weak_points.get(tag, 0) for tag in lesson.weak_point_tags)
    
    lessons.sort(key=priority, reverse=True)
    
    return lessons[:limit]
