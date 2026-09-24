import unittest
import asyncio
from datetime import datetime
from types import SimpleNamespace

from fastapi import HTTPException

from app.api.endpoints.internal import curriculum_preview_catalog, curriculum_preview_lesson, require_control_key
from app.core.config import settings
from app.services.beta_insights import tester_alias, tester_progress


class FakeLessonQuery:
    def __init__(self, lessons):
        self.lessons = lessons

    def filter(self, *args):
        return self

    def all(self):
        return self.lessons

    def first(self):
        return self.lessons[0] if self.lessons else None


class FakeLessonDb:
    def __init__(self, lessons):
        self.lessons = lessons

    def query(self, _model):
        return FakeLessonQuery(self.lessons)


class BetaControlCenterTests(unittest.TestCase):
    def test_curriculum_preview_requires_control_key(self):
        original = settings.TASK_SECRET
        settings.TASK_SECRET = "preview-secret"
        try:
            with self.assertRaises(HTTPException) as denied:
                require_control_key("wrong")
            self.assertEqual(403, denied.exception.status_code)
            self.assertIsNone(require_control_key("preview-secret"))
        finally:
            settings.TASK_SECRET = original

    def test_curriculum_preview_is_sorted_and_returns_localized_content(self):
        lessons = [
            SimpleNamespace(id=2, level="B1", pillar="grammar", topic="later", estimated_time=12, xp_reward=50,
                content={"day": 2, "module": 1, "title": "Later", "rule": "Regel", "examples": ["Ich lerne."], "exercises": [{"type": "fill", "question": "Q", "answer": "A"}]}),
            SimpleNamespace(id=1, level="A1", pillar="speaking", topic="hello", estimated_time=8, xp_reward=40,
                content={"day": 1, "module": 1, "title": "Hello", "rule": "Use Hallo", "examples": ["Hallo!"], "exercises": [{"type": "fill", "question": "Say hello", "answer": "Hallo"}]}),
        ]
        db = FakeLessonDb(lessons)

        catalog = asyncio.run(curriculum_preview_catalog(db))
        detail = asyncio.run(curriculum_preview_lesson(1, "en", FakeLessonDb([lessons[1]])))

        self.assertEqual([1, 2], [item["id"] for item in catalog])
        self.assertEqual(1, catalog[0]["exercise_count"])
        self.assertTrue(detail["preview"])
        self.assertEqual("A1", detail["level"])
        self.assertEqual("Hallo", detail["content"]["exercises"][0]["answer"])

    def test_alias_is_stable_and_does_not_expose_database_id(self):
        alias = tester_alias(123456, "test-secret")
        self.assertEqual(alias, tester_alias(123456, "test-secret"))
        self.assertTrue(alias.startswith("T-"))
        self.assertNotIn("123456", alias)

    def test_tester_progress_connects_journey_without_telegram_identity(self):
        now = datetime.now()
        enrollment = SimpleNamespace(user_id=7, invite_id=3, joined_at=now, consent=True, goal="conversation")
        user = SimpleNamespace(id=7, language_code="de", diagnostic_completed=True)
        invite = SimpleNamespace(id=3, label="Beta tester 01")
        sessions = [
            SimpleNamespace(user_id=7, status="passed", started_at=now),
            SimpleNamespace(user_id=7, status="active", started_at=now),
        ]
        events = [SimpleNamespace(user_id=7, event_name="beta_feedback", created_at=now)]

        result = tester_progress([enrollment], [user], [invite], sessions, events, "test-secret")[0]

        self.assertEqual("Beta tester 01", result["invite"])
        self.assertEqual(2, result["lessons_started"])
        self.assertEqual(1, result["lessons_completed"])
        self.assertEqual(1, result["feedback_count"])
        self.assertNotIn("user_id", result)


if __name__ == "__main__":
    unittest.main()
