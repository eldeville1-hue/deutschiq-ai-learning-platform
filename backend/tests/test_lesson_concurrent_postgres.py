"""PostgreSQL integration: concurrent lesson starts share one persisted session."""
import asyncio
import os
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import StartLessonRequest, start_lesson
from app.models.learning import ExerciseAttempt, LearningSession
from app.models.lesson import Lesson
from app.models.user import User


@unittest.skipUnless(os.getenv("TEST_POSTGRES_URL"), "Requires CI PostgreSQL")
class ConcurrentLessonStartPostgresTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(os.environ["TEST_POSTGRES_URL"], pool_size=5)
        for model in (User, Lesson, LearningSession, ExerciseAttempt):
            model.__table__.create(self.engine, checkfirst=True)
        with Session(self.engine) as db:
            db.query(ExerciseAttempt).filter_by(lesson_id=981010).delete()
            db.query(LearningSession).filter_by(lesson_id=981010).delete()
            db.query(Lesson).filter_by(id=981010).delete()
            db.query(User).filter_by(telegram_id=981010).delete()
            db.add(User(id=981010, telegram_id=981010))
            db.add(Lesson(id=981010, level="A1", pillar="grammar",
                          topic="concurrent-start", weak_point_tags="", content={}))
            db.commit()

    def tearDown(self):
        with Session(self.engine) as db:
            db.query(LearningSession).filter_by(lesson_id=981010).delete()
            db.query(Lesson).filter_by(id=981010).delete()
            db.query(User).filter_by(telegram_id=981010).delete()
            db.commit()
        self.engine.dispose()

    def test_reopening_with_new_database_connection_restores_saved_answers(self):
        with Session(self.engine) as db:
            initial = asyncio.run(start_lesson(
                StartLessonRequest(user_id=981010, lesson_id=981010),
                db=db, authenticated_id=981010,
            ))
            db.add_all([
                ExerciseAttempt(user_id=981010, lesson_id=981010,
                                session_id=initial["session_id"], exercise_index=0,
                                topic="concurrent-start", answer="wrong", correct=False),
                ExerciseAttempt(user_id=981010, lesson_id=981010,
                                session_id=initial["session_id"], exercise_index=0,
                                topic="concurrent-start", answer="correct", correct=True),
                ExerciseAttempt(user_id=981010, lesson_id=981010,
                                session_id=initial["session_id"], exercise_index=1,
                                topic="concurrent-start", answer="wrong", correct=False),
            ])
            db.commit()

        # A separate SQLAlchemy session simulates a later API request after
        # the app was closed; no in-memory lesson state is reused.
        with Session(self.engine) as reopened_db:
            reopened = asyncio.run(start_lesson(
                StartLessonRequest(user_id=981010, lesson_id=981010),
                db=reopened_db, authenticated_id=981010,
            ))
            self.assertEqual(reopened["session_id"], initial["session_id"])
            self.assertTrue(reopened["resumed"])
            self.assertEqual(reopened["next_exercise_index"], 1)
            self.assertEqual(reopened_db.query(LearningSession).filter_by(
                user_id=981010, lesson_id=981010, status="active",
            ).count(), 1)
            self.assertEqual(reopened_db.query(ExerciseAttempt).filter_by(
                session_id=initial["session_id"],
            ).count(), 3)

    def test_two_simultaneous_starts_reuse_one_session(self):
        barrier = threading.Barrier(2)

        def start():
            with Session(self.engine) as db:
                barrier.wait(timeout=10)
                return asyncio.run(start_lesson(
                    StartLessonRequest(user_id=981010, lesson_id=981010),
                    db=db, authenticated_id=981010,
                ))

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(start) for _ in range(2)]
            results = [future.result(timeout=20) for future in futures]
        self.assertEqual(results[0]["session_id"], results[1]["session_id"])
        self.assertEqual(sorted(result["resumed"] for result in results), [False, True])
        with Session(self.engine) as db:
            self.assertEqual(db.query(LearningSession).filter_by(
                user_id=981010, lesson_id=981010, status="active",
            ).count(), 1)


if __name__ == "__main__":
    unittest.main()
