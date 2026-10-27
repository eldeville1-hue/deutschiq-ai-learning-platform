"""End-to-end service regression: saved attempts drive the daily lesson choice."""
import asyncio
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from sqlalchemy import ARRAY, JSON, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.learning import today
from app.api.endpoints.lesson import CheckAnswerRequest, StartLessonRequest, check_answer, start_lesson, get_due_lesson_reviews
from app.models.diagnostic import DiagnosticResult
from app.models.learning import ExerciseAttempt, LearningSession, TopicMastery
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.user import User


@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"


class PersistedAdaptiveTodayTests(unittest.TestCase):
    def setUp(self):
        self._weak_tags_type = Lesson.__table__.c.weak_point_tags.type
        Lesson.__table__.c.weak_point_tags.type = JSON()
        self._review_dates_type = UserProgress.__table__.c.review_dates.type
        UserProgress.__table__.c.review_dates.type = JSON()
        self.engine = create_engine("sqlite:///:memory:")
        for model in (User, Lesson, LearningSession, ExerciseAttempt, TopicMastery,
                      UserProgress, DiagnosticResult):
            model.__table__.create(self.engine, checkfirst=True)
        self.db = Session(self.engine)
        self.lessons = [
            Lesson(id=10, level="A2", pillar="grammar", topic="word_order",
                   weak_point_tags=["word_order"], content={"day": 1, "track": "A2",
                       "exercises": [{"type": "choose", "question": "Word order?",
                                      "answer": "Ich gehe heute.", "options": ["Ich gehe heute.", "Ich heute gehe."]}]}),
            Lesson(id=11, level="A2", pillar="grammar", topic="articles",
                   weak_point_tags=["articles"], content={"day": 2, "track": "A2",
                       "exercises": [{"type": "choose", "question": "Article?",
                                      "answer": "der", "options": ["der", "die"]}]}),
        ]
        self.db.add(User(id=1, telegram_id=9001, current_level="A2", language_code="en"))
        self.db.add_all(self.lessons)
        self.db.add_all([
            TopicMastery(user_id=1, topic="word_order", mastery=85, attempts=5,
                         stability_days=5, next_review_at=datetime.now(timezone.utc) + timedelta(days=5)),
            TopicMastery(user_id=1, topic="articles", mastery=85, attempts=5,
                         stability_days=5, next_review_at=datetime.now(timezone.utc) + timedelta(days=5)),
        ])
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()
        UserProgress.__table__.c.review_dates.type = self._review_dates_type
        Lesson.__table__.c.weak_point_tags.type = self._weak_tags_type

    def answer(self, value, lesson_id=11):
        session = asyncio.run(start_lesson(
            StartLessonRequest(user_id=9001, lesson_id=lesson_id),
            db=self.db, authenticated_id=9001,
        ))
        return asyncio.run(check_answer(
            CheckAnswerRequest(user_id=9001, lesson_id=lesson_id, exercise_index=0,
                               answer=value, session_id=session["session_id"]),
            db=self.db, authenticated_id=9001,
        ))

    def recommendation(self):
        self.db.expire_all()
        with patch("app.api.endpoints.learning.generate_plan", return_value=self.lessons), \
             patch("app.api.endpoints.learning.normalize_lesson_content", side_effect=lambda content, *_: content), \
             patch("app.api.endpoints.learning.localize_lesson_content", side_effect=lambda content, *_: content):
            return asyncio.run(today(9001, db=self.db, authenticated_id=9001))

    def test_persisted_error_repair_then_due_review(self):
        """A real stored mistake changes Today, and a verified review clears its due item."""
        self.assertEqual(10, self.recommendation()["next_lesson"]["id"])
        self.assertFalse(self.answer("die")["correct"])
        self.assertFalse(self.answer("die")["correct"])
        self.assertEqual(11, self.recommendation()["next_lesson"]["id"])

        # Complete an independent correct attempt and simulate the due date
        # that the review scheduler will eventually reach.
        self.assertTrue(self.answer("der")["correct"])
        self.db.query(LearningSession).filter_by(user_id=1, lesson_id=11).update({"status": "completed"})
        self.db.commit()
        self.assertTrue(self.answer("der")["correct"])
        self.db.add(UserProgress(
            user_id=1, lesson_id=11, completed=True,
            review_dates=[(datetime.now() - timedelta(days=1)).isoformat()],
        ))
        self.db.commit()
        due = asyncio.run(get_due_lesson_reviews(limit=10, db=self.db, authenticated_id=9001))
        self.assertIn(11, [item["lesson_id"] for item in due["reviews"]])

        # The review is a separate attempt, not a resubmission of a
        # completed learning exercise in its original session.
        self.db.query(LearningSession).filter_by(user_id=1, lesson_id=11).update({"status": "completed"})
        self.db.commit()
        session = asyncio.run(start_lesson(
            StartLessonRequest(user_id=9001, lesson_id=11),
            db=self.db, authenticated_id=9001,
        ))
        review = asyncio.run(check_answer(
            CheckAnswerRequest(
                user_id=9001, lesson_id=11, exercise_index=0, answer="der",
                session_id=session["session_id"], mode="review", language="en",
            ),
            db=self.db, authenticated_id=9001,
        ))
        self.assertTrue(review["correct"])
        self.db.expire_all()
        remaining = asyncio.run(get_due_lesson_reviews(limit=10, db=self.db, authenticated_id=9001))
        self.assertNotIn(11, [item["lesson_id"] for item in remaining["reviews"]])
        self.assertEqual(5, self.db.query(ExerciseAttempt).filter_by(user_id=1).count())

    def test_saved_errors_prioritize_skill_and_recovery_removes_focus(self):
        self.assertEqual(10, self.recommendation()["next_lesson"]["id"])
        self.assertFalse(self.answer("die")["correct"])
        self.assertFalse(self.answer("die")["correct"])
        self.assertEqual(11, self.recommendation()["next_lesson"]["id"])
        self.assertTrue(self.answer("der")["correct"])
        # A correct answer completes this exercise; a new independent attempt
        # must use a new session rather than resubmit a completed exercise.
        self.db.query(LearningSession).filter_by(user_id=1, lesson_id=11).update({"status": "completed"})
        self.db.commit()
        self.assertTrue(self.answer("der")["correct"])
        self.assertEqual(4, self.db.query(ExerciseAttempt).filter_by(user_id=1).count())
        self.assertEqual(10, self.recommendation()["next_lesson"]["id"])


if __name__ == "__main__":
    unittest.main()
