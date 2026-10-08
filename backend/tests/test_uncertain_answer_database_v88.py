import asyncio
import unittest
from unittest.mock import patch
from sqlalchemy import ARRAY, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import CheckAnswerRequest, check_answer
from app.models.user import User
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.learning import ExerciseAttempt, TopicMastery, LearningSession


@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"


class DatabaseUncertainAnswerTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        for model in (User, Lesson, LearningSession, TopicMastery, ExerciseAttempt, UserProgress):
            model.__table__.create(self.engine)
        self.db = Session(self.engine)
        self.db.add_all([
            User(id=1, telegram_id=9001, xp=55, streak=4),
            Lesson(id=77, level="B1", pillar="grammar", topic="infinitive",
                   weak_point_tags="", content={}),
            LearningSession(id="active-session", user_id=1, lesson_id=77,
                            status="active", score=None),
            TopicMastery(user_id=1, topic="infinitive", mastery=0.6,
                         attempts=3, correct_streak=2, correct_total=2),
        ])
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_uncertain_answer_preserves_database_state_in_both_modes(self):
        exercise = {"type": "translation", "answer": "Ich besuche meine Freundin morgen."}
        for mode in ("lesson", "review"):
            with self.subTest(mode=mode):
                request = CheckAnswerRequest(
                    user_id=9001, lesson_id=77, exercise_index=0,
                    answer="Ich besuche meine Freundin morgn.",
                    session_id="active-session", mode=mode,
                )
                with patch("app.api.endpoints.lesson.normalize_lesson_content",
                           return_value={"exercises": [exercise]}):
                    with patch("app.api.endpoints.lesson.localize_lesson_content",
                               return_value={"exercises": [exercise]}):
                        result = asyncio.run(check_answer(request, db=self.db, authenticated_id=9001))
                self.db.expire_all()
                user = self.db.query(User).filter_by(id=1).one()
                mastery = self.db.query(TopicMastery).filter_by(user_id=1).one()
                session = self.db.query(LearningSession).filter_by(id="active-session").one()
                self.assertEqual("uncertain", result["evaluation_status"])
                self.assertEqual((55, 4), (user.xp, user.streak))
                self.assertEqual((0.6, 3, 2, 2), (mastery.mastery, mastery.attempts,
                                                 mastery.correct_streak, mastery.correct_total))
                self.assertEqual(("active", None, None),
                                 (session.status, session.score, session.completed_at))
                self.assertEqual(0, self.db.query(ExerciseAttempt).count())
                self.assertEqual(0, self.db.query(UserProgress).count())


if __name__ == "__main__":
    unittest.main()
