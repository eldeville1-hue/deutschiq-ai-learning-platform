import ast
import re
import unittest
from copy import deepcopy
from pathlib import Path

from app.services.content_i18n import LESSON_COPY, localize_lesson_content, normalize_language


class InternationalizationTests(unittest.TestCase):
    def test_all_thirty_lessons_have_english_and_german_copy(self):
        self.assertEqual(30, len(LESSON_COPY["en"]))
        self.assertEqual(30, len(LESSON_COPY["de"]))
        for lang in ("en", "de"):
            for day in range(1, 31):
                content = localize_lesson_content({"day": day, "title": "RU", "rule": "RU", "objective": "RU", "communication_goal": "RU", "exercises": [{"answer": "x"}, {"answer": "Hallo."}, {"answer": "x"}, {"answer": "x"}]}, lang)
                self.assertTrue(content["title"])
                self.assertTrue(content["rule"])
                self.assertNotEqual("RU", content["title"])
                self.assertEqual(4, len(content["exercises"]))
                self.assertTrue(all(item.get("question") for item in content["exercises"]))
                visible_copy = " ".join(str(item) for item in (
                    content["title"], content["rule"], content["objective"],
                    content["recall_prompt"], *(exercise.get("question", "") for exercise in content["exercises"]),
                    *(exercise.get("hint", "") for exercise in content["exercises"]),
                ))
                self.assertIsNone(re.search(r"[А-Яа-яЁё]", visible_copy), f"Cyrillic leaked into {lang} day {day}")

    def test_all_placement_questions_are_complete_in_each_language(self):
        source = Path(__file__).resolve().parents[1] / "app" / "api" / "endpoints" / "diagnostic.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        namespace = {"deepcopy": deepcopy}
        wanted = {"MOCK_QUESTIONS", "PLACEMENT_QUESTION_IDS", "DIAGNOSTIC_COPY"}
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id in wanted for target in node.targets):
                exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"), namespace)
            if isinstance(node, ast.FunctionDef) and node.name in {"normalize_language", "localized_questions"}:
                exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"), namespace)

        expected_ids = namespace["PLACEMENT_QUESTION_IDS"]
        for lang in ("ru", "de", "en"):
            questions = [item for item in namespace["localized_questions"](lang) if item["id"] in expected_ids]
            self.assertEqual(len(expected_ids), len(questions))
            for question in questions:
                self.assertTrue(question["text"])
                self.assertEqual(4, len(question["options"]))
                self.assertIn(question["correct_answer"], question["options"])
                self.assertTrue(question["explanation"])
                if lang != "ru":
                    visible = " ".join([question["text"], question["explanation"], *question["options"]])
                    self.assertIsNone(re.search(r"[А-Яа-яЁё]", visible), f"Cyrillic leaked into {lang} question {question['id']}")

    def test_language_codes_are_normalized_safely(self):
        self.assertEqual("de", normalize_language("de-DE"))
        self.assertEqual("ru", normalize_language("ru-RU"))
        self.assertEqual("en", normalize_language("fr"))


if __name__ == "__main__":
    unittest.main()
