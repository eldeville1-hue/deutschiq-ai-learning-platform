"""Read-only report of answer-key defects in the deployed lesson database.

Usage (from backend/): python -m scripts.audit_curriculum_answers
Optional: python -m scripts.audit_curriculum_answers --json
Never changes lessons or learner data.
"""
import argparse
import json
from collections import Counter

from app.core.database import SessionLocal
from app.models.lesson import Lesson
from app.services.content_quality import exercise_answer_audit

LEVELS = ("A1", "A2", "B1", "B2")


def build_report(lessons):
    report = {"levels": {}, "issues": [], "total_lessons": 0, "total_exercises": 0}
    for level in LEVELS:
        report["levels"][level] = {"lessons": 0, "exercises": 0, "affected_lessons": 0, "issues": 0}
    for lesson in lessons:
        if lesson.level not in LEVELS:
            continue
        stats = report["levels"][lesson.level]
        stats["lessons"] += 1
        report["total_lessons"] += 1
        content = lesson.content if isinstance(lesson.content, dict) else {}
        count = len(content.get("exercises") or [])
        stats["exercises"] += count
        report["total_exercises"] += count
        problems = exercise_answer_audit(content)
        if problems:
            stats["affected_lessons"] += 1
        stats["issues"] += len(problems)
        for problem in problems:
            report["issues"].append({
                "level": lesson.level,
                "lesson_id": lesson.id,
                "topic": lesson.topic,
                "issue": problem,
            })
    report["issue_counts"] = dict(sorted(Counter(
        item["issue"].split(":", 2)[-1] for item in report["issues"]
    ).items()))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable report")
    args = parser.parse_args()
    db = SessionLocal()
    try:
        lessons = db.query(Lesson).order_by(Lesson.level, Lesson.id).all()
        report = build_report(lessons)
    finally:
        db.close()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("DeutschIQ A1–B2 exercise answer audit (read-only)")
        for level, stats in report["levels"].items():
            print(f"{level}: {stats['lessons']} lessons, {stats['exercises']} exercises, "
                  f"{stats['affected_lessons']} affected lessons, {stats['issues']} issues")
        print(f"TOTAL: {report['total_lessons']} lessons, {report['total_exercises']} exercises")
        for item in report["issues"]:
            print(f"{item['level']} lesson {item['lesson_id']} ({item['topic']}): {item['issue']}")


if __name__ == "__main__":
    main()
