"""Handler-level regression for roadmap personalization using saved attempts."""
import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.api.endpoints.plan import get_plan
from app.models.diagnostic import DiagnosticResult
from app.models.learning import ExerciseAttempt, TopicMastery
from app.models.progress import UserProgress
from app.models.user import User


def lesson(lesson_id, topic, day):
    return SimpleNamespace(
        id=lesson_id, topic=topic, content={"day": day, "track": "A2"},
        weak_point_tags=[topic], level="A2", pillar="grammar", estimated_time=6,
    )


class PersonalizedPlanApiTests(unittest.TestCase):
    def test_saved_repeated_errors_mark_articles_as_recommended(self):
        user = SimpleNamespace(id=5, telegram_id=9001, language_code="en", current_level="A2")
        first, articles = lesson(1, "word_order", 1), lesson(2, "articles", 2)
        attempts = [
            SimpleNamespace(id=1, topic="articles", correct=False),
            SimpleNamespace(id=2, topic="word_order", correct=True),
            SimpleNamespace(id=3, topic="articles", correct=False),
        ]
        db = MagicMock()
        def query(model):
            chain = MagicMock()
            if model is User:
                chain.filter.return_value.first.return_value = user
            elif model is TopicMastery:
                chain.filter.return_value.all.return_value = [
                    SimpleNamespace(topic="word_order", mastery=85, attempts=5),
                    SimpleNamespace(topic="articles", mastery=75, attempts=4),
                ]
            elif model is UserProgress.lesson_id:
                chain.filter.return_value.all.return_value = []
            elif model is DiagnosticResult:
                chain.filter.return_value.order_by.return_value.first.return_value = None
            elif model is ExerciseAttempt:
                chain.filter.return_value.order_by.return_value.limit.return_value.all.return_value = list(reversed(attempts))
            return chain
        db.query.side_effect = query
        with patch("app.api.endpoints.plan.generate_plan", return_value=[first, articles]), \
             patch("app.api.endpoints.plan.normalize_lesson_content", side_effect=lambda content, *_: content), \
             patch("app.api.endpoints.plan.localize_lesson_content", side_effect=lambda content, *_: content):
            result = asyncio.run(get_plan(9001, db=db, authenticated_id=9001))
        self.assertEqual([1, 2], [item["id"] for item in result])
        self.assertEqual([False, True], [item["recommended"] for item in result])
        self.assertEqual([], result[1]["blocked_by"])


if __name__ == "__main__":
    unittest.main()
