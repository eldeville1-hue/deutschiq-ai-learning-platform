"""Offline curriculum audit: python audit_curriculum.py --output curriculum-audit.json."""
import argparse
import json
from pathlib import Path

from seed_30_day_plan import curriculum_audit_report, CURRICULUM, B1_CURRICULUM, A1_CURRICULUM, A2_CURRICULUM, B2_CURRICULUM, build_content, build_b1_content, build_b2_content, build_foundation_content
from app.services.content_quality import exercise_answer_audit, exercise_instruction_audit
from app.services.learning_effectiveness_audit import learning_effectiveness_evidence


def build_report():
    tracks = curriculum_audit_report()
    sources = [
        ("30-day roadmap", CURRICULUM, lambda row: build_content(row[0], row[1], row[2], row[4], row[5], row[6])),
        ("A1", A1_CURRICULUM, lambda row: build_foundation_content(row, "A1")),
        ("A2", A2_CURRICULUM, lambda row: build_foundation_content(row, "A2")),
        ("B1", B1_CURRICULUM, build_b1_content),
        ("B2", B2_CURRICULUM, build_b2_content),
    ]
    exercise_issues = {}
    exercise_findings = []
    learning_evidence = {}
    for track, rows, builder in sources:
        findings = []
        learning_evidence[track] = []
        for row in rows:
            try:
                content = builder(row)
                learning_evidence[track].append({"day": row[0], **learning_effectiveness_evidence(content)})
                for category, issues in (
                    ("answer", exercise_answer_audit(content)),
                    ("instruction", exercise_instruction_audit(content)),
                ):
                    for issue in issues:
                        findings.append({"day": row[0], "category": category, "issue": issue})
                        parts = issue.split(":", 2)
                        index = int(parts[1]) if len(parts) > 2 and parts[0] == "exercise" and parts[1].isdigit() else None
                        exercises = content.get("exercises") or []
                        exercise = exercises[index] if index is not None and index < len(exercises) else None
                        exercise_findings.append({
                            "track": track, "level": "A1" if track == "30-day roadmap" else track,
                            "day": row[0], "exercise_index": index,
                            "exercise_id": exercise.get("id") if isinstance(exercise, dict) else None,
                            "category": category, "severity": "blocking",
                            "issue": issue, "evidence": issue,
                        })
            except Exception as exc:
                issue = f"{type(exc).__name__}:{exc}"
                findings.append({"day": row[0], "category": "build", "issue": issue})
                exercise_findings.append({
                    "track": track, "level": "A1" if track == "30-day roadmap" else track,
                    "day": row[0], "exercise_index": None, "exercise_id": None,
                    "category": "build", "severity": "blocking",
                    "issue": issue, "evidence": issue,
                })
        exercise_issues[track] = findings
    repair_queue = []
    for track, lessons in learning_evidence.items():
        for lesson in lessons:
            if lesson["issues"]:
                repair_queue.append({"track": track, "day": lesson["day"], "issues": lesson["issues"]})
    repair_queue.sort(key=lambda item: (-len(item["issues"]), item["track"], item["day"]))
    return {
        "repair_queue": repair_queue,
        "status": "failed" if any(tracks.values()) or any(exercise_issues.values()) else "passed",
        "total_issues": sum(len(item["issues"]) for lessons in tracks.values() for item in lessons),
        "affected_lessons": sum(len(lessons) for lessons in tracks.values()),
        "tracks": tracks,
        "exercise_issues": exercise_issues,
        "exercise_findings": exercise_findings,
        "learning_effectiveness_evidence": learning_evidence,
        "total_exercise_issues": sum(len(items) for items in exercise_issues.values()),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate authored DeutschIQ lessons without database access")
    parser.add_argument("--output", type=Path, help="Optional destination for a JSON audit report")
    args = parser.parse_args(argv)
    report = build_report()
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Curriculum audit saved to {args.output}")
    else:
        print(rendered)
    return 1 if report["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
