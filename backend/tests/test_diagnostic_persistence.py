"""Regression tests for diagnostic persistence and authorization."""
import asyncio
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.api.endpoints.diagnostic import SubmitAnswers, submit_diagnostic


class FailingSession:
    def __init__(self):
        self.rolled_back = False

    def query(self, model):
        raise SQLAlchemyError("database unavailable")

    def rollback(self):
        self.rolled_back = True


class DiagnosticPersistenceTests(unittest.TestCase):
    def test_failed_save_returns_503_and_rolls_back(self):
        db = FailingSession()
        payload = SubmitAnswers(user_id=12345, answers={1: "habe"}, language="en")
        result = {
            "level": "A1",
            "overall_score": 50,
            "pillars": {"grammar": 50, "vocabulary": 0, "listening": 0},
            "weak_points": {},
        }
        with patch("app.api.endpoints.diagnostic.calculate_level_and_scores", return_value=result):
            with self.assertRaises(HTTPException) as error:
                asyncio.run(submit_diagnostic(payload, db=db, authenticated_id=12345))
        self.assertEqual(error.exception.status_code, 503)
        self.assertTrue(db.rolled_back)

    def test_other_user_is_rejected(self):
        db = FailingSession()
        payload = SubmitAnswers(user_id=12345, answers={}, language="en")
        with self.assertRaises(HTTPException) as error:
            asyncio.run(submit_diagnostic(payload, db=db, authenticated_id=54321))
        self.assertEqual(error.exception.status_code, 403)
        self.assertFalse(db.rolled_back)


if __name__ == "__main__":
    unittest.main()
