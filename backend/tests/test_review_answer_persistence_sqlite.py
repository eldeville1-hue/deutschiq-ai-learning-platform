"""Database-backed checks for review answers and their next due date."""
import asyncio
import unittest
from datetime import datetime, timedelta
from sqlalchemy import ARRAY, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import CheckAnswerRequest, check_answer
from app.models.learning import ExerciseAttempt, LearningSession, TopicMastery
from app.models.lesson import Lesson
from app.models.user import User


@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"


class ReviewAnswerPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        for model in (User, Lesson, LearningSession, ExerciseAttempt, TopicMastery):
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
