"""Database-backed checks for review answers and their next due date."""
import asyncio
import unittest
from datetime import datetime, timedelta
from sqlalchemy import ARRAY, JSON, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import CheckAnswerRequest, check_answer, get_due_lesson_reviews
from app.models.learning import ExerciseAttempt, LearningSession, TopicMastery
from app.models.lesson import Lesson
from app.models.user import User
from app.models.progress import UserProgress


@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"


class ReviewAnswerPersistenceTests(unittest.TestCase):
    def setUp(self):
        self._review_dates_type = UserProgress.__table__.c.review_dates.type
        UserProgress.__table__.c.review_dates.type = JSON()
        self.engine = create_engine("sqlite:///:memory:")
        for model in (User, Lesson, LearningSession, ExerciseAttempt, TopicMastery, UserProgress):
            model.__table__.create(self.engine, checkfirst=True)
        self.db = Session(self.engine)
        self.db.add_all([
            User(id=1, telegram_id=9001),
            Lesson(id=10, level="A2", pillar="grammar", topic="articles",
                   weak_point_tags="", content={"exercises": [
                       {"type": "choose", "question": "Choose the article", "answer": "der",
                        "options": ["der", "die", "das"]}]}),
            TopicMastery(user_id=1, topic="articles", mastery=50, attempts=1,
                         next_review_at=datetime.utcnow() - timedelta(days=1)),
        ])
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()
        UserProgress.__table__.c.review_dates.type = self._review_dates_type

    def review(self, answer, session_id):
        self.db.add(LearningSession(id=session_id, user_id=1, lesson_id=10, status="active"))
        self.db.commit()
        before = datetime.utcnow()
        result = asyncio.run(check_answer(CheckAnswerRequest(
            user_id=9001, lesson_id=10, exercise_index=0, answer=answer,
            session_id=session_id, mode="review", language="en",
        ), db=self.db, authenticated_id=9001))
        self.db.expire_all()
        mastery = self.db.query(TopicMastery).filter_by(user_id=1, topic="articles").one()
        self.assertGreater(mastery.next_review_at, before)
        self.assertEqual("passed" if result["correct"] else "practice_needed",
                         self.db.get(LearningSession, session_id).status)
        return result, mastery

    def test_review_consumes_overdue_lesson_dates_but_preserves_future(self):
        overdue = datetime.now() - timedelta(days=2)
        upcoming = datetime.now() + timedelta(days=3)
        self.db.add(UserProgress(user_id=1, lesson_id=10, completed=True,
                                 review_dates=[overdue.isoformat(), upcoming.isoformat()]))
        self.db.commit()
        self.review("der", "review-consume")
        progress = self.db.query(UserProgress).filter_by(user_id=1, lesson_id=10).one()
        self.assertEqual([upcoming.isoformat()], progress.review_dates)

    def test_due_queue_lifecycle_after_verified_answer(self):
        overdue = datetime.now() - timedelta(days=2)
        upcoming = datetime.now() + timedelta(days=3)
        self.db.add(UserProgress(user_id=1, lesson_id=10, completed=True,
                                 review_dates=[overdue.isoformat(), upcoming.isoformat()]))
        self.db.commit()
        before = asyncio.run(get_due_lesson_reviews(
            limit=5, db=self.db, authenticated_id=9001,
        ))
        self.assertEqual(1, before["count"])
        self.assertEqual(10, before["reviews"][0]["lesson_id"])
        self.assertEqual("articles", before["reviews"][0]["title"])
        self.review("der", "review-queue-lifecycle")
        after = asyncio.run(get_due_lesson_reviews(
            limit=5, db=self.db, authenticated_id=9001,
        ))
        self.assertEqual({"reviews": [], "count": 0}, after)
        progress = self.db.query(UserProgress).filter_by(user_id=1, lesson_id=10).one()
        self.assertEqual([upcoming.isoformat()], progress.review_dates)

    def test_wrong_review_remains_due_until_correct_retry(self):
        overdue = datetime.now() - timedelta(days=2)
        upcoming = datetime.now() + timedelta(days=3)
        self.db.add(UserProgress(user_id=1, lesson_id=10, completed=True,
                                 review_dates=[overdue.isoformat(), upcoming.isoformat()]))
        self.db.commit()
        wrong, _ = self.review("die", "review-wrong-then-right")
        self.assertFalse(wrong["correct"])
        pending = asyncio.run(get_due_lesson_reviews(
            limit=5, db=self.db, authenticated_id=9001,
        ))
        self.assertEqual(1, pending["count"])
        self.assertEqual(2, len(self.db.query(UserProgress).filter_by(
            user_id=1, lesson_id=10).one().review_dates))
        correct, _ = self.review("der", "review-right-after-wrong")
        self.assertTrue(correct["correct"])
        after = asyncio.run(get_due_lesson_reviews(
            limit=5, db=self.db, authenticated_id=9001,
        ))
        self.assertEqual(0, after["count"])
        self.assertEqual([upcoming.isoformat()], self.db.query(UserProgress).filter_by(
            user_id=1, lesson_id=10).one().review_dates)

    def test_correct_review_saves_new_due_date(self):
        result, mastery = self.review("der", "review-correct")
        self.assertTrue(result["correct"])
        self.assertEqual(1, self.db.query(ExerciseAttempt).count())
        self.assertGreater(mastery.next_review_at, datetime.utcnow())

    def test_wrong_review_saves_retry_date_and_lapse(self):
        result, mastery = self.review("die", "review-wrong")
        self.assertFalse(result["correct"])
        self.assertEqual(1, mastery.lapse_count)
        self.assertEqual(0, mastery.correct_streak)
        self.assertEqual(1, self.db.query(ExerciseAttempt).count())


if __name__ == "__main__":
    unittest.main()
