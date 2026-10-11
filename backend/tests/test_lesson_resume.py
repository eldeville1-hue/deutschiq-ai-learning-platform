import asyncio
import unittest
from types import SimpleNamespace

from fastapi import HTTPException
from sqlalchemy import ARRAY, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import (StartLessonRequest, CheckAnswerRequest, start_lesson, check_answer, next_unanswered_exercise_index)
from app.models.user import User
from app.models.lesson import Lesson
from app.models.learning import LearningSession, ExerciseAttempt


@compiles(ARRAY, 'sqlite')
def sqlite_array(_type, _compiler, **_kwargs):
    return 'TEXT'


class LessonResumeTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        for model in (User, Lesson, LearningSession, ExerciseAttempt):
            model.__table__.create(self.engine)
        self.db = Session(self.engine)
        self.db.add_all([User(id=1, telegram_id=9001), User(id=2, telegram_id=9002),
            Lesson(id=77, level='B1', pillar='grammar', topic='advice', weak_point_tags='', content={}),
            Lesson(id=78, level='B1', pillar='grammar', topic='other', weak_point_tags='', content={})])
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def start(self, resume_id=None):
        return asyncio.run(start_lesson(StartLessonRequest(user_id=9001, lesson_id=77,
            resume_session_id=resume_id), self.db, authenticated_id=9001))

    def test_active_session_is_reused_without_creating_a_duplicate(self):
        first = self.start()
        resumed = self.start(first['session_id'])
        self.assertTrue(resumed['resumed'])
        self.assertEqual(first['session_id'], resumed['session_id'])
        self.assertEqual(1, self.db.query(LearningSession).count())

    def test_foreign_wrong_lesson_and_completed_sessions_are_not_resumed(self):
        for session_id, owner, lesson, status in [('foreign', 2, 77, 'active'),
            ('other-lesson', 1, 78, 'active'), ('finished', 1, 77, 'completed')]:
            self.db.add(LearningSession(id=session_id, user_id=owner, lesson_id=lesson, status=status))
        self.db.commit()
        for session_id in ('foreign', 'other-lesson', 'finished', 'missing'):
            with self.subTest(session_id=session_id):
                result = self.start(session_id)
                # An invalid requested ID may still recover another valid active
                # session for this same learner and lesson.
                self.assertNotEqual(session_id, result['session_id'])
                recovered = self.db.get(LearningSession, result['session_id'])
                self.assertEqual((1, 77, 'active'), (recovered.user_id, recovered.lesson_id, recovered.status))

    def test_resume_still_requires_authenticated_owner(self):
        with self.assertRaises(HTTPException) as error:
            asyncio.run(start_lesson(StartLessonRequest(user_id=9001, lesson_id=77), self.db, authenticated_id=9002))
        self.assertEqual(403, error.exception.status_code)


class LessonCursorTests(unittest.TestCase):
    def test_only_contiguous_correct_answers_advance_cursor(self):
        attempts = [SimpleNamespace(exercise_index=0, correct=True),
                    SimpleNamespace(exercise_index=1, correct=False),
                    SimpleNamespace(exercise_index=2, correct=True)]
        self.assertEqual(1, next_unanswered_exercise_index(attempts))
        attempts.append(SimpleNamespace(exercise_index=1, correct=True))
        self.assertEqual(3, next_unanswered_exercise_index(attempts))

    def test_empty_and_negative_attempts_do_not_advance_cursor(self):
        self.assertEqual(0, next_unanswered_exercise_index([]))
        self.assertEqual(0, next_unanswered_exercise_index([
            SimpleNamespace(exercise_index=-1, correct=True),
            SimpleNamespace(exercise_index=0, correct=False)]))

    def test_repeated_correct_attempt_does_not_skip_exercises(self):
        attempts = [SimpleNamespace(exercise_index=0, correct=True) for _ in range(3)]
        self.assertEqual(1, next_unanswered_exercise_index(attempts))


class MissingLessonAnswerTests(unittest.TestCase):
    def test_deleted_lesson_returns_404_instead_of_crashing(self):
        engine = create_engine('sqlite:///:memory:')
        Lesson.__table__.create(engine)
        db = Session(engine)
        request = CheckAnswerRequest(user_id=9001, lesson_id=999999,
            exercise_index=0, answer='test', session_id='not-a-session')
        with self.assertRaises(HTTPException) as error:
            asyncio.run(check_answer(request, db, authenticated_id=9001))
        self.assertEqual(404, error.exception.status_code)
        self.assertEqual('Lesson not found', error.exception.detail)
        db.close()
        engine.dispose()
