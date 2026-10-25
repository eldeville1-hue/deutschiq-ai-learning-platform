from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import OperationalError

from app.api.endpoints.plan import get_plan


@pytest.mark.asyncio
async def test_plan_database_error_is_not_an_empty_success():
    db = MagicMock()
    db.query.side_effect = OperationalError("SELECT users", {}, Exception("database unavailable"))

    with patch("app.api.endpoints.plan.assert_owner"):
        with pytest.raises(HTTPException) as exc:
            await get_plan(user_id=123, db=db, authenticated_id=123)

    assert exc.value.status_code == 503
    assert exc.value.detail == "Learning plan is temporarily unavailable"
    db.rollback.assert_called_once()
