from types import SimpleNamespace
from scripts.audit_curriculum_answers import build_report


def lesson(id, level, exercises):
    return SimpleNamespace(id=id, level=level, topic="Articles", content={"exercises": [{"question": "Choose the correct form.", "explanation": "Check the rule.", **exercise} for exercise in exercises]})


def test_answer_audit_report_identifies_problematic_lessons():
    report = build_report([
        lesson(1, "A1", [{"type": "choose", "answer": "den", "options": ["der", "dem"]}]),
        lesson(2, "B2", [{"type": "choose", "answer": "obwohl", "options": ["weil", "obwohl"]}]),
        lesson(3, "A2", [{"type": "fill", "answer": "habe"}]),
    ])
    assert report["total_lessons"] == 3
    assert report["total_exercises"] == 3
    assert report["levels"]["A1"]["affected_lessons"] == 1
    assert report["levels"]["B2"]["issues"] == 0
    assert report["issues"][0]["lesson_id"] == 1
    assert report["issues"][0]["issue"] == "exercise:0:answer_not_in_options"


def test_answer_audit_report_is_read_only_and_filters_levels():
    item = lesson(4, "A1", [{"type": "fill", "answer": "bin"}])
    before = item.content["exercises"][0].copy()
    report = build_report([item, lesson(5, "C1", [{"type": "fill", "answer": "x"}])])
    assert report["total_lessons"] == 1
    assert report["issues"] == []
    assert item.content["exercises"][0] == before


def test_report_includes_instruction_and_listening_source_issues():
    report = build_report([lesson(6, "A2", [
        {"type": "listening", "answer": "ja", "question": "", "explanation": ""},
    ])])
    assert report["answer_issues"] == 0
    assert report["instruction_issues"] == 3
    assert report["levels"]["A2"]["affected_lessons"] == 1
    assert {issue["category"] for issue in report["issues"]} == {"instruction"}
    assert {issue["issue"] for issue in report["issues"]} == {
        "exercise:0:missing_question",
        "exercise:0:missing_explanation",
        "exercise:0:missing_listening_source",
    }
