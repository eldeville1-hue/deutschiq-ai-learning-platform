import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from app.api.endpoints.lesson import CheckAnswerRequest, check_answer


class UncertainAnswerApiTests(unittest.TestCase):
    def test_uncertain_response_never_writes_progress(self):
        exercise = {"type": "translation", "answer": "Ich besuche meine Freundin morgen."}
        for mode in ("lesson", "review"):
            with self.subTest(mode=mode):
                db = MagicMock()
                db.query.return_value.filter.return_value.first.return_value = SimpleNamespace(
                    id=77, topic="German", level="B1", content={}
                )
                request = CheckAnswerRequest(
                    user_id=9001, lesson_id=77, exercise_index=0,
                    answer="Ich besuche meine Freundin morgn.",
                    session_id="existing-session", mode=mode,
                )
                with patch("app.api.endpoints.lesson.normalize_lesson_content",
                           return_value={"exercises": [exercise]}):
                    with patch("app.api.endpoints.lesson.localize_lesson_content",
                               return_value={"exercises": [exercise]}):
                        result = asyncio.run(check_answer(request, db=db, authenticated_id=9001))
                self.assertEqual("uncertain", result["evaluation_status"])
                self.assertFalse(result["correct"])
                db.add.assert_not_called()
                db.commit.assert_not_called()
                db.flush.assert_not_called()
                self.assertEqual(3, db.query.call_count)


if __name__ == "__main__":
    unittest.main()
