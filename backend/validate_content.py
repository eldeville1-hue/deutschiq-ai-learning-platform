from app.core.database import SessionLocal
from app.models.lesson import Lesson
from app.services.content_quality import normalize_lesson_content, validate_lesson_content, validate_roadmap_content


def main():
    db = SessionLocal()
    failures = []
    try:
        for lesson in db.query(Lesson).filter(Lesson.is_active == True).all():
            content = normalize_lesson_content(lesson.content or {}, lesson.topic, lesson.level)
            errors = validate_roadmap_content(content) if content.get("day") else validate_lesson_content(content)
            if errors:
                failures.append(f"{lesson.id}:{lesson.topic}: {', '.join(errors)}")
        if failures:
            raise SystemExit("\n".join(failures))
        print("Content quality check passed")
    finally:
        db.close()


if __name__ == "__main__":
    main()
