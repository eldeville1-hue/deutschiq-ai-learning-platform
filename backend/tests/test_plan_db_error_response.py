import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from sqlalchemy.exc import OperationalError

from app.api.endpoints.plan import get_plan


class LearningPlanDatabaseErrorTests(unittest.IsolatedAsyncioTestCase):
    async def test_database_error_is_not_an_empty_success(self):
        db = MagicMock()
        db.query.side_effect = OperationalError(
            "SELECT users", {}, Exception("database unavailable")
        )

        with patch("app.api.endpoints.plan.assert_owner"):
            with self.assertRaises(HTTPException) as error:
                await get_plan(user_id=123, db=db, authenticated_id=123)

        self.assertEqual(error.exception.status_code, 503)
        self.assertEqual(
            error.exception.detail, "Learning plan is temporarily unavailable"
        )
        db.rollback.assert_called_once()
