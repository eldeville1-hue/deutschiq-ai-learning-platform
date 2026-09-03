# backend/app/services/badges.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.progress import UserProgress
from app.models.badge import UserBadge

BADGE_CONFIG = {
    'first_lesson': {'name': 'Первый урок', 'icon': '🎯', 'condition': 'lessons_completed >= 1'},
    'week_streak': {'name': 'Неделя усилий', 'icon': '🔥', 'condition': 'streak >= 7'},
    'month_streak': {'name': 'Месяц усердия', 'icon': '⭐', 'condition': 'streak >= 30'},
    'level_b1': {'name': 'Уровень B1', 'icon': '🏆', 'condition': 'level == "B1"'},
    'level_b2': {'name': 'Уровень B2', 'icon': '👑', 'condition': 'level == "B2"'},
    'level_c1': {'name': 'Уровень C1', 'icon': '💎', 'condition': 'level == "C1"'},
    'perfect_test': {'name': 'Идеальный тест', 'icon': '💯', 'condition': 'test_score == 100'},
    'daily_streak_3': {'name': '3 дня подряд', 'icon': '📅', 'condition': 'streak >= 3'},
    'daily_streak_10': {'name': '10 дней подряд', 'icon': '🔥', 'condition': 'streak >= 10'},
    'daily_streak_30': {'name': '30 дней подряд', 'icon': '👑', 'condition': 'streak >= 30'},
    'lessons_10': {'name': '10 уроков', 'icon': '📚', 'condition': 'lessons_completed >= 10'},
    'lessons_50': {'name': '50 уроков', 'icon': '🎓', 'condition': 'lessons_completed >= 50'},
    'lessons_100': {'name': '100 уроков', 'icon': '🏅', 'condition': 'lessons_completed >= 100'},
}

def check_and_award_badges(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    
    lessons_completed = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.completed == True
    ).count()
    
    # Получаем последний результат теста (если есть)
    from app.models.diagnostic import DiagnosticResult
    last_test = db.query(DiagnosticResult).filter(
        DiagnosticResult.user_id == user_id
    ).order_by(DiagnosticResult.created_at.desc()).first()
    test_score = last_test.overall_score if last_test else 0
    
    awarded = []
    existing = [b.badge_type for b in db.query(UserBadge).filter(UserBadge.user_id == user_id).all()]
    
    checks = {
        'first_lesson': lessons_completed >= 1,
        'week_streak': user.streak >= 7,
        'month_streak': user.streak >= 30,
        'level_b1': user.current_level == 'B1',
        'level_b2': user.current_level == 'B2',
        'level_c1': user.current_level == 'C1',
        'perfect_test': test_score >= 100,
        'daily_streak_3': user.streak >= 3,
        'daily_streak_10': user.streak >= 10,
        'daily_streak_30': user.streak >= 30,
        'lessons_10': lessons_completed >= 10,
        'lessons_50': lessons_completed >= 50,
        'lessons_100': lessons_completed >= 100,
    }
    
    for badge_type, condition in checks.items():
        if badge_type in existing:
            continue
        if condition:
            badge = UserBadge(
                user_id=user_id,
                badge_type=badge_type,
                badge_name=BADGE_CONFIG[badge_type]['name'],
                badge_icon=BADGE_CONFIG[badge_type]['icon']
            )
            db.add(badge)
            awarded.append(BADGE_CONFIG[badge_type])
    
    if awarded:
        db.commit()
    
    return awarded

