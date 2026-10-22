"""A publication-ready lesson cannot present a choice task without choices."""
from app.services.content_quality import validate_roadmap_content


def _content(version):
    return {
        "quality_version": version,
        "objective": "Use the right verb",
        "rule": "Er uses ist",
        "examples": ["Er ist hier."],
        "audio_text": "Er ist hier.",
        "common_mistakes": ["❌ Er sind hier", "✅ Er ist hier"],
        "exercises": [{
            "type": "choose", "question": "Er ___ hier",
            "answer": "ist", "explanation": "Use ist",
        }],
    }


def test_published_choice_requires_options():
    errors = validate_roadmap_content(_content(8))
    assert "publish:exercise:0:missing_options" in errors


def test_legacy_choice_without_options_keeps_compatibility():
    errors = validate_roadmap_content(_content(1))
    assert "publish:exercise:0:missing_options" not in errors
