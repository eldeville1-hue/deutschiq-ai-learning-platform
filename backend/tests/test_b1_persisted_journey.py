"""B1 persisted lesson regression: error, independent recovery, reload and account isolation.

Run: cd backend && python -m unittest tests.test_b1_persisted_journey
This is an API/service integration test, not a Telegram browser E2E test.
"""
import asyncio
import unittest

from fastapi import HTTPException
from unittest.mock import AsyncMock, patch
from sqlalchemy import ARRAY, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import (
    CheckAnswerRequest, StartLessonRequest, check_answer, start_lesson, get_due_reviews,
)
from app.models.learning import ExerciseAttempt, LearningSession, TopicMastery
from app.models.lesson import Lesson
from app.models.user import User
from app.services.assessment_insights import independent_progression_evidence


@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"


class B1PersistedJourneyTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        for model in (User, Lesson, LearningSession, ExerciseAttempt, TopicMastery):
            model.__table__.create(self.engine, checkfirst=True)
        self.db = Session(self.engine)
        self.db.add_all([
            User(telegram_id=91001),
            User(telegram_id=91002),
            Lesson(
                id=910, level="B1", pillar="grammar", topic="connectors",
                weak_point_tags="", content={"exercises": [
                    {"type": "choose", "question": "Choose the conjunction.",
                     "answer": "obwohl", "accepted_answers": ["obwohl"],
                     "options": ["weil", "obwohl", "deshalb"]},
                    {"type": "choose", "question": "Choose the causal conjunction.",
                     "answer": "weil", "accepted_answers": ["weil"],
                     "options": ["obwohl", "weil", "trotzdem"]},
                ]},
            ),
        ])
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def start(self, learner, resume=None):
        return asyncio.run(start_lesson(
            StartLessonRequest(user_id=learner, lesson_id=910, resume_session_id=resume),
            db=self.db, authenticated_id=learner,
        ))

    def answer(self, learner, session_id, index, value, mode="lesson") :
        return asyncio.run(check_answer(
            CheckAnswerRequest(
                user_id=learner, lesson_id=910, session_id=session_id,
                exercise_index=index, answer=value, confidence="sure", mode=mode,
            ), db=self.db, authenticated_id=learner,
        ))

    def test_error_then_independent_recovery_persists_without_duplicate_credit(self):
        session = self.start(91001)
        self.assertFalse(session["resumed"])
        failed = self.answer(91001, session["session_id"], 0, "weil")
        self.assertFalse(failed["correct"])
        self.assertEqual("verified", failed["evaluation_status"])
        self.assertTrue(failed["needs_support"])
        self.db.expire_all()
        resumed = self.start(91001)
        self.assertTrue(resumed["resumed"])
        self.assertEqual(session["session_id"], resumed["session_id"])
        self.assertEqual(0, resumed["next_exercise_index"])

        corrected = self.answer(91001, session["session_id"], 0, "obwohl")
        self.assertTrue(corrected["correct"])
        self.assertEqual("guided_retry", corrected["learning_evidence"]["assistance_level"])
        self.db.expire_all()
        self.assertEqual(1, self.start(91001)["next_exercise_index"])

        independent = self.answer(91001, session["session_id"], 1, "weil")
        self.assertTrue(independent["correct"])
        self.assertEqual("independent", independent["learning_evidence"]["assistance_level"])
        self.db.expire_all()
        self.assertEqual(2, self.start(91001)["next_exercise_index"])

        owner = self.db.query(User).filter_by(telegram_id=91001).one()
        mastery = self.db.query(TopicMastery).filter_by(user_id=owner.id, topic="connectors").one()
        self.assertEqual(3, mastery.attempts)
        self.assertEqual(2, mastery.correct_total)
        self.assertEqual(3, self.db.query(ExerciseAttempt).filter_by(user_id=owner.id).count())
        with self.assertRaises(HTTPException) as duplicate:
            self.answer(91001, session["session_id"], 1, "weil")
        self.assertEqual(409, duplicate.exception.status_code)
        self.db.expire_all()
        self.assertEqual(3, self.db.query(ExerciseAttempt).filter_by(user_id=owner.id).count())

    def test_verified_production_persists_independent_evidence_and_retry_is_guided(self):
        self.db.add(Lesson(
            id=911, level="B1", pillar="writing", topic="formal_email",
            weak_point_tags="", content={"exercises": [
                {"type": "production", "question": "Write a short German email.",
                 "answer": "Ich schreibe Ihnen wegen des Termins."},
            ]},
        ))
        self.db.commit()
        feedback = {
            "correct": True, "corrected_answer": "Ich schreibe Ihnen wegen des Termins.", "feedback": "Good formal email.", "score": 86, "dimension_scores": {
                "grammar": 85, "task_completion": 90,
            }, "cefr_standard": "B1", "source": "rubric",
        }
        with patch("app.api.endpoints.lesson.evaluate_production", new_callable=AsyncMock, return_value=feedback):
            session = asyncio.run(start_lesson(
                StartLessonRequest(user_id=91001, lesson_id=911),
                db=self.db, authenticated_id=91001,
            ))
            response = asyncio.run(check_answer(
                CheckAnswerRequest(
                    user_id=91001, lesson_id=911, session_id=session["session_id"],
                    exercise_index=0, answer="Ich schreibe Ihnen wegen des Termins.",
                ), db=self.db, authenticated_id=91001,
            ))
        self.assertTrue(response["correct"])
        owner = self.db.query(User).filter_by(telegram_id=91001).one()
        attempt = self.db.query(ExerciseAttempt).filter_by(user_id=owner.id, lesson_id=911).one()
        self.assertEqual(86, attempt.production_score)
        self.assertEqual(85, attempt.assessment["dimensions"]["grammar"])
        self.assertEqual("verified", attempt.assessment["evaluation"]["evaluation_status"])
        self.assertEqual("independent", attempt.assessment["learning_evidence"]["assistance_level"])
        self.assertEqual(1, attempt.assessment["learning_evidence"]["attempt_number"])
        self.assertEqual(1, independent_progression_evidence([attempt])["independent_samples"])

    def test_failed_review_is_due_and_successful_review_is_rescheduled(self):
        from datetime import datetime, timedelta

        first = self.start(91001)
        self.assertTrue(self.answer(91001, first["session_id"], 0, "obwohl")["correct"])
        owner = self.db.query(User).filter_by(telegram_id=91001).one()
        mastery = self.db.query(TopicMastery).filter_by(user_id=owner.id, topic="connectors").one()
        mastery.next_review_at = datetime.utcnow() - timedelta(days=1)
        self.db.commit()

        due = asyncio.run(get_due_reviews(db=self.db, authenticated_id=91001))
        self.assertEqual(1, due["count"])
        self.assertEqual("connectors", due["reviews"][0]["topic"])
        other_due = asyncio.run(get_due_reviews(db=self.db, authenticated_id=91002))
        self.assertEqual(0, other_due["count"])

        # Review uses a separate exercise to avoid replaying a completed answer.
        failed = self.answer(91001, first["session_id"], 1, "obwohl", mode="review")
        self.assertFalse(failed["correct"])
        self.db.expire_all()
        mastery = self.db.query(TopicMastery).filter_by(user_id=owner.id, topic="connectors").one()
        self.assertGreater(mastery.lapse_count, 0)
        self.assertIsNotNone(mastery.next_review_at)
        self.assertGreater(mastery.next_review_at, datetime.utcnow())

    def test_other_learner_cannot_resume_or_submit_to_owner_session(self):
        owner_session = self.start(91001)["session_id"]
        other = self.start(91002, resume=owner_session)
        self.assertNotEqual(owner_session, other["session_id"])
        with self.assertRaises(HTTPException) as forbidden:
            self.answer(91002, owner_session, 0, "obwohl")
        self.assertEqual(409, forbidden.exception.status_code)
        other_user = self.db.query(User).filter_by(telegram_id=91002).one()
        self.assertEqual(0, self.db.query(ExerciseAttempt).filter_by(user_id=other_user.id).count())


if __name__ == "__main__":
    unittest.main()
