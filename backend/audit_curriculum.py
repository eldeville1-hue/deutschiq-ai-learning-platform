"""Offline curriculum audit: python audit_curriculum.py --output curriculum-audit.json."""
import argparse
import json
from pathlib import Path

from seed_30_day_plan import curriculum_audit_report


def build_report():
    tracks = curriculum_audit_report()
    return {
        "status": "failed" if any(tracks.values()) else "passed",
        "total_issues": sum(len(item["issues"]) for lessons in tracks.values() for item in lessons),
        "affected_lessons": sum(len(lessons) for lessons in tracks.values()),
        "tracks": tracks,
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
