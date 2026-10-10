"""Regression: recommendations must not expose another Telegram learner's data."""
import asyncio
import unittest
from unittest.mock import MagicMock

from fastapi import HTTPException

from app.api.endpoints.learning import today
from app.api.endpoints.plan import get_plan


class PersonalizationOwnershipTests(unittest.TestCase):
    def test_other_users_daily_recommendation_is_forbidden_before_database_read(self):
        db = MagicMock()
        with self.assertRaises(HTTPException) as error:
            asyncio.run(today(9002, db=db, authenticated_id=9001))
        self.assertEqual(403, error.exception.status_code)
        db.query.assert_not_called()

    def test_other_users_roadmap_is_forbidden_before_database_read(self):
        db = MagicMock()
        with self.assertRaises(HTTPException) as error:
            asyncio.run(get_plan(9002, db=db, authenticated_id=9001))
        self.assertEqual(403, error.exception.status_code)
        db.query.assert_not_called()

    def test_missing_auth_identity_does_not_allow_daily_recommendation(self):
        db = MagicMock()
        with self.assertRaises(HTTPException) as error:
            asyncio.run(today(9002, db=db, authenticated_id=None))
        self.assertEqual(403, error.exception.status_code)
        db.query.assert_not_called()


if __name__ == "__main__":
    unittest.main()
