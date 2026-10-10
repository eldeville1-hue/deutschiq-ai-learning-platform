"""HTTP-handler regression for personalized daily recommendations."""
import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.api.endpoints.learning import today


def lesson(lesson_id, topic, day):
    return SimpleNamespace(
        id=lesson_id, topic=topic, content={"day": day, "track": "A2", "exercises": []},
        weak_point_tags=[topic], level="A2", estimated_time=6,
    )


class PersonalizedTodayApiTests(unittest.TestCase):
    def test_persisted_repeated_errors_change_daily_recommendation(self):
        user = SimpleNamespace(id=5, telegram_id=9001, language_code="en")
        first = lesson(1, "word_order", 1)
        articles = lesson(2, "articles", 2)
        attempts = [
            SimpleNamespace(id=1, topic="articles", correct=False),
            SimpleNamespace(id=2, topic="word_order", correct=True),
            SimpleNamespace(id=3, topic="articles", correct=False),
        ]
        db = MagicMock()
        mastered = [
            SimpleNamespace(topic="word_order", mastery=85, stability_days=3,
                            next_review_at=None, attempts=5, lapse_count=0),
            SimpleNamespace(topic="articles", mastery=75, stability_days=2,
                            next_review_at=None, attempts=4, lapse_count=1),
        ]
        # Each ORM query starts with a different model. Configure the result
        # at the query boundary, not by accidentally sharing filter chains.
        from app.models.user import User
        from app.models.learning import TopicMastery, ExerciseAttempt
        from app.models.progress import UserProgress
        from app.models.diagnostic import DiagnosticResult
        def query(model):
            chain = MagicMock()
            if model is User:
                chain.filter.return_value.first.return_value = user
            elif model is TopicMastery:
                chain.filter.return_value.order_by.return_value.all.return_value = mastered
                chain.filter.return_value.order_by.return_value.limit.return_value.all.return_value = []
            elif model is UserProgress.lesson_id:
                chain.filter.return_value.all.return_value = []
            elif model is DiagnosticResult:
                chain.filter.return_value.order_by.return_value.first.return_value = None
            elif model is ExerciseAttempt:
                chain.filter.return_value.order_by.return_value.limit.return_value.all.side_effect = [
                    list(reversed(attempts)), [], [],
                ]
            return chain
        db.query.side_effect = query
        with patch("app.api.endpoints.learning.generate_plan", return_value=[first, articles]), \
             patch("app.api.endpoints.learning.normalize_lesson_content", side_effect=lambda content, *_: content), \
             patch("app.api.endpoints.learning.localize_lesson_content", side_effect=lambda content, *_: content), \
             patch("app.api.endpoints.learning.assessment_insights", return_value={"priority_topics": []}):
            result = asyncio.run(today(9001, db=db, authenticated_id=9001))
        self.assertEqual(2, result["next_lesson"]["id"])
        self.assertEqual("articles", result["next_lesson"]["topic"])
        self.assertEqual(2, next(p["lesson_id"] for p in result["session"]["phases"] if p["kind"] == "learn"))


if __name__ == "__main__":
    unittest.main()
