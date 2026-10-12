"""Regression coverage for lesson answer failure telemetry ingestion."""
import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from fastapi import HTTPException
from app.api.endpoints.events import EventRequest, capture_event


class LessonAnswerFailureEventTests(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = SimpleNamespace(id=42)

    def test_event_is_accepted_and_persisted(self):
        payload = EventRequest(user_id=9001, event_name="lesson_answer_failed",
            properties={"lesson_id": 77, "exercise_index": 2, "status": 409,
                        "reason": "closed_session", "retry": False})
        response = asyncio.run(capture_event(payload, db=self.db, authenticated_id=9001))
        self.assertEqual(response.status_code, 204)
        self.db.add.assert_called_once()
        saved = self.db.add.call_args.args[0]
        self.assertEqual(saved.event_name, "lesson_answer_failed")
        self.assertEqual(saved.user_id, 42)
        self.assertEqual(saved.properties["reason"], "closed_session")
        self.assertNotIn("answer", saved.properties)
        self.db.commit.assert_called_once()

    def test_event_rejects_other_users(self):
        payload = EventRequest(user_id=9001, event_name="lesson_answer_failed")
        with self.assertRaises(HTTPException) as raised:
            asyncio.run(capture_event(payload, db=self.db, authenticated_id=9002))
        self.assertEqual(raised.exception.status_code, 403)
        self.db.add.assert_not_called()

    def test_unknown_event_still_rejected(self):
        payload = EventRequest(user_id=9001, event_name="unrecognized_event")
        with self.assertRaises(HTTPException) as raised:
            asyncio.run(capture_event(payload, db=self.db, authenticated_id=9001))
        self.assertEqual(raised.exception.status_code, 422)
        self.db.add.assert_not_called()

    def test_non_scalar_properties_are_filtered(self):
        payload = EventRequest(user_id=9001, event_name="lesson_answer_failed",
                               properties={"status": 500, "nested": {"answer": "private"}})
        asyncio.run(capture_event(payload, db=self.db, authenticated_id=9001))
        saved = self.db.add.call_args.args[0]
        self.assertEqual(saved.properties, {"status": 500})


if __name__ == "__main__":
    unittest.main()
