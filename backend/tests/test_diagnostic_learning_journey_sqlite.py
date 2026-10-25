"""Exercise the diagnostic -> lesson -> saved answer path in one SQLite database."""
import asyncio
import unittest

from sqlalchemy import ARRAY, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.diagnostic import SubmitAnswers, submit_diagnostic
from app.api.endpoints.lesson import CheckAnswerRequest, StartLessonRequest, check_answer, start_lesson
from app.models.diagnostic import DiagnosticMistake, DiagnosticResult
from app.models.event import ProductEvent
from app.models.learning import ExerciseAttempt, LearningSession, TopicMastery
from app.models.lesson import Lesson
from app.models.user import User


@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"


class DiagnosticLearningJourneyTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        for model in (User, DiagnosticResult, DiagnosticMistake, ProductEvent,
                      Lesson, LearningSession, ExerciseAttempt, TopicMastery):
            model.__table__.create(self.engine, checkfirst=True)
        self.db = Session(self.engine)
        self.db.add(Lesson(
            id=10, level="A1", pillar="grammar", topic="articles",
            weak_point_tags="", content={"exercises": [{
                "type": "choose", "question": "Which article?",
                "answer": "das", "accepted_answers": ["das"],
                "options": ["der", "die", "das"],
            }]},
        ))
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_diagnostic_result_and_lesson_attempt_survive_reload(self):
        diagnostic = asyncio.run(submit_diagnostic(
            SubmitAnswers(user_id=9001, answers={1: "habe", 2: "Der"}, language="en"),
            db=self.db, authenticated_id=9001,
        ))
        self.assertTrue(diagnostic["persisted"])
        self.assertIn("articles", diagnostic["weak_points"])
        self.db.expire_all()
        user = self.db.query(User).filter_by(telegram_id=9001).one()
        self.assertTrue(user.diagnostic_completed)
        self.assertEqual(diagnostic["level"], user.current_level)
        self.assertEqual(1, self.db.query(DiagnosticResult).filter_by(user_id=user.id).count())
        self.assertEqual(1, self.db.query(DiagnosticMistake).count())

        session = asyncio.run(start_lesson(
            StartLessonRequest(user_id=9001, lesson_id=10),
            db=self.db, authenticated_id=9001,
        ))
        answer = asyncio.run(check_answer(
            CheckAnswerRequest(
                user_id=9001, lesson_id=10, exercise_index=0,
                answer="das", session_id=session["session_id"],
            ), db=self.db, authenticated_id=9001,
        ))
        self.assertTrue(answer["correct"])
        self.db.expire_all()
        self.assertEqual(1, self.db.query(ExerciseAttempt).filter_by(user_id=user.id).count())
        mastery = self.db.query(TopicMastery).filter_by(user_id=user.id, topic="articles").one()
        self.assertEqual(1, mastery.attempts)
        self.assertEqual(1, mastery.correct_total)


if __name__ == "__main__":
    unittest.main()
