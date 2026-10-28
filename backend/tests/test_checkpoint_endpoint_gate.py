"""Checkpoint endpoint security regression: direct GET/POST cannot bypass evidence."""
import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException
from sqlalchemy import ARRAY, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.checkpoint import CheckpointSubmission, get_checkpoint, submit_checkpoint
from app.models.learning import ExerciseAttempt, TopicMastery
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.user import User
from app.models.event import ProductEvent


@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"


class CheckpointEndpointGateTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        for model in (User, Lesson, UserProgress, TopicMastery, ExerciseAttempt, ProductEvent):
            model.__table__.create(self.engine, checkfirst=True)
        self.db = Session(self.engine)
        self.user = User(telegram_id=92001, current_level="A1")
        self.other = User(telegram_id=92002, current_level="A1")
        self.lesson = Lesson(
            id=920, level="A1", pillar="grammar", topic="connectors",
            weak_point_tags="[]", is_active=True,
            content={"track": "A1", "day": 1, "exercises": [
                {"type": "dialogue", "mission_role": "final", "question": "Answer in German"}
            ]},
        )
        self.db.add_all([self.user, self.other, self.lesson])
        self.db.flush()
        self.db.add(UserProgress(user_id=self.user.id, lesson_id=self.lesson.id, completed=True, score=100, review_dates="[]"))
        self.db.add(TopicMastery(user_id=self.user.id, topic="connectors", mastery=95))
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_direct_get_and_submit_are_forbidden_without_independent_evidence(self):
        for index in range(4):
            self.db.add(ExerciseAttempt(
                user_id=self.user.id, lesson_id=self.lesson.id,
                session_id="assisted", exercise_index=index,
                topic="connectors", answer="obwohl", correct=True,
                assessment={
                    "dimensions": {"task_completion": 95, "grammar": 95, "coherence": 95},
                    "evaluation": {"evaluation_status": "verified"},
                    "learning_evidence": {"assistance_level": "guided_retry", "attempt_number": 2},
                },
            ))
        self.db.commit()
        with self.assertRaises(HTTPException) as blocked_get:
            asyncio.run(get_checkpoint(92001, "A1", db=self.db, authenticated_id=92001))
        self.assertEqual(403, blocked_get.exception.status_code)
        with patch("app.api.endpoints.checkpoint.evaluate_production") as scorer:
            with self.assertRaises(HTTPException) as blocked_post:
                asyncio.run(submit_checkpoint(
                    CheckpointSubmission(user_id=92001, level="A1", answers=["perfect"]),
                    db=self.db, authenticated_id=92001,
                ))
            self.assertEqual(403, blocked_post.exception.status_code)
            scorer.assert_not_called()
        self.db.refresh(self.user)
        self.assertEqual("A1", self.user.current_level)

    def test_checkpoint_rejects_missing_blank_or_extra_answers_before_scoring(self):
        for answers in ([], [""], ["  "], ["first", "unexpected"]):
            with self.subTest(answers=answers):
                with patch("app.api.endpoints.checkpoint.eligibility", return_value={"eligible": True}):
                    with patch("app.api.endpoints.checkpoint.evaluate_production") as scorer:
                        with self.assertRaises(HTTPException) as blocked:
                            asyncio.run(submit_checkpoint(
                                CheckpointSubmission(user_id=92001, level="A1", answers=answers),
                                db=self.db, authenticated_id=92001,
                            ))
                        self.assertEqual(422, blocked.exception.status_code)
                        scorer.assert_not_called()
        self.db.refresh(self.user)
        self.assertEqual("A1", self.user.current_level)

    def test_checkpoint_without_final_missions_does_not_score_or_graduate(self):
        self.lesson.content = {"track": "A1", "day": 1, "exercises": [
            {"type": "choose", "question": "Choose", "answer": "ja"},
        ]}
        self.db.commit()
        with patch("app.api.endpoints.checkpoint.eligibility", return_value={"eligible": True}):
            with patch("app.api.endpoints.checkpoint.evaluate_production") as scorer:
                with self.assertRaises(HTTPException) as blocked:
                    asyncio.run(submit_checkpoint(
                        CheckpointSubmission(user_id=92001, level="A1", answers=["ja"]),
                        db=self.db, authenticated_id=92001,
                    ))
                self.assertEqual(409, blocked.exception.status_code)
                scorer.assert_not_called()

    def test_passing_checkpoint_graduates_only_owner_and_replay_is_blocked(self):
        feedback = {
            "correct": True, "score": 90, "dimension_scores": {
                "task_completion": 95, "grammar": 90,
            }, "feedback": "Well done", "improvement": "",
        }
        with patch("app.api.endpoints.checkpoint.eligibility", return_value={"eligible": True}):
            with patch("app.api.endpoints.checkpoint.evaluate_production", new_callable=AsyncMock, return_value=feedback) as scorer:
                result = asyncio.run(submit_checkpoint(
                    CheckpointSubmission(user_id=92001, level="A1", answers=["Guten Tag!"]),
                    db=self.db, authenticated_id=92001,
                ))
                self.assertTrue(result["passed"])
                self.assertEqual("A2", result["unlocked_level"])
                self.assertEqual(1, scorer.await_count)
        self.db.expire_all()
        owner = self.db.query(User).filter_by(telegram_id=92001).one()
        other = self.db.query(User).filter_by(telegram_id=92002).one()
        self.assertEqual("A2", owner.current_level)
        self.assertEqual("A1", other.current_level)
        self.assertEqual(1, self.db.query(ProductEvent).filter_by(user_id=owner.id, event_name="checkpoint_completed").count())
        with patch("app.api.endpoints.checkpoint.evaluate_production") as scorer:
            with self.assertRaises(HTTPException) as blocked:
                asyncio.run(submit_checkpoint(
                    CheckpointSubmission(user_id=92001, level="A1", answers=["Guten Tag!"]),
                    db=self.db, authenticated_id=92001,
                ))
            self.assertEqual(403, blocked.exception.status_code)
            scorer.assert_not_called()

    def test_failed_checkpoint_keeps_level_and_records_recovery(self):
        feedback = {
            "correct": False, "score": 30, "dimension_scores": {
                "task_completion": 30, "grammar": 25,
            }, "feedback": "Try again", "improvement": "Add details",
        }
        with patch("app.api.endpoints.checkpoint.eligibility", return_value={"eligible": True}):
            with patch("app.api.endpoints.checkpoint.evaluate_production", new_callable=AsyncMock, return_value=feedback):
                result = asyncio.run(submit_checkpoint(
                    CheckpointSubmission(user_id=92001, level="A1", answers=["Hallo"]),
                    db=self.db, authenticated_id=92001,
                ))
        self.assertFalse(result["passed"])
        self.assertEqual("repair", result["next_route"])
        self.assertEqual([ "connectors" ], result["recovery_topics"])
        self.db.expire_all()
        self.assertEqual("A1", self.db.query(User).filter_by(telegram_id=92001).one().current_level)

    def test_other_user_cannot_fetch_or_submit_checkpoint(self):
        with self.assertRaises(HTTPException) as blocked:
            asyncio.run(get_checkpoint(92001, "A1", db=self.db, authenticated_id=92002))
        self.assertEqual(403, blocked.exception.status_code)
        with self.assertRaises(HTTPException) as blocked:
            asyncio.run(submit_checkpoint(
                CheckpointSubmission(user_id=92001, level="A1", answers=[]),
                db=self.db, authenticated_id=92002,
            ))
        self.assertEqual(403, blocked.exception.status_code)


if __name__ == "__main__":
    unittest.main()
