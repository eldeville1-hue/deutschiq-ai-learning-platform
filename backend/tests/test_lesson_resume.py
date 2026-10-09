import asyncio
import unittest

from fastapi import HTTPException
from sqlalchemy import ARRAY, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import StartLessonRequest, start_lesson
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
                self.assertFalse(result['resumed'])
                self.assertNotEqual(session_id, result['session_id'])

    def test_resume_still_requires_authenticated_owner(self):
        with self.assertRaises(HTTPException) as error:
            asyncio.run(start_lesson(StartLessonRequest(user_id=9001, lesson_id=77), self.db, authenticated_id=9002))
        self.assertEqual(403, error.exception.status_code)
