import ast
import unittest
from pathlib import Path
from app.services.content_quality import normalize_lesson_content, validate_lesson_content, validate_roadmap_content
from app.content.b1_curriculum import B1_CURRICULUM, build_b1_content
from app.services.content_i18n import localize_lesson_content


class ContentQualityTests(unittest.TestCase):
    def test_normalizer_supplies_learning_sequence(self):
        content = normalize_lesson_content({"rule":"x", "examples":["Ich lerne."]}, "word_order", "A2")
        self.assertEqual(content["audio_text"], "Ich lerne.")
        self.assertIn("objective", content)

    def test_validator_rejects_uncheckable_exercise(self):
        content = normalize_lesson_content({"rule":"x", "examples":["x"], "exercises":[{"type":"fill", "question":"q"}]}, "x", "A1")
        errors = validate_lesson_content(content)
        self.assertIn("exercise:0:missing_answer", errors)

    def test_legacy_listening_lesson_is_migrated(self):
        content = normalize_lesson_content(
            {
                "examples": ["Danke, gut!"],
                "common_mistakes": [],
                "exercises": [
                    {"type": "listen", "question": "Was hörst du?", "answer": "Danke, gut!"}
                ],
            },
            "Аудирование: приветствие",
            "A1",
        )
        self.assertEqual(content["exercises"][0]["type"], "listening")
        self.assertTrue(content["common_mistakes"])
        self.assertEqual([], validate_lesson_content(content))

    def test_complete_roadmap_has_30_multimodal_daily_challenges(self):
        source = Path(__file__).resolve().parents[1] / "seed_30_day_plan.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        namespace = {}
        wanted = {"CURRICULUM", "LESSON_DETAILS", "GOLD_LESSON_EXAMPLES"}
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id in wanted for target in node.targets):
                exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"), namespace)
            if isinstance(node, ast.FunctionDef) and node.name == "build_content":
                exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"), namespace)

        self.assertEqual(len(namespace["CURRICULUM"]), 30)
        total_exercises = 0
        exercise_types = set()
        for row in namespace["CURRICULUM"]:
            day, topic, rule, _, example, question, answer = row
            content = namespace["build_content"](day, topic, rule, example, question, answer)
            self.assertEqual(content["quality_version"], 2)
            self.assertEqual(validate_roadmap_content(content), [], f"day {day}")
            kinds = {item["type"] for item in content["exercises"]}
            exercise_types.update(kinds)
            self.assertTrue({"listening", "production", "repeat"}.issubset(kinds))
            self.assertGreaterEqual(len(set(content["examples"])), 3)
            self.assertFalse(content["title"].lower().startswith("tag "))
            total_exercises += len(content["exercises"])
        self.assertGreaterEqual(total_exercises, 120)
        self.assertTrue({"fill", "reorder", "listening", "production", "repeat"}.issubset(exercise_types))

    def test_b1_track_has_24_multilingual_varied_lessons(self):
        self.assertEqual(24, len(B1_CURRICULUM))
        self.assertEqual({1, 2, 3, 4}, {row[1] for row in B1_CURRICULUM})
        guided_types = set()
        for row in B1_CURRICULUM:
            content = build_b1_content(row)
            self.assertEqual([], validate_roadmap_content(content), f"day {row[0]}")
            self.assertEqual("B1", content["track"])
            self.assertEqual("B1", content["cefr"])
            self.assertEqual(4, len(content["exercises"]))
            guided_types.add(content["exercises"][0]["type"])
            for language in ("ru", "de", "en"):
                localized = localize_lesson_content(content, language)
                self.assertTrue(localized["title"])
                self.assertTrue(localized["rule"])
                self.assertTrue(localized["objective"])
                self.assertNotIn("i18n", localized)
                self.assertTrue(all("i18n" not in exercise for exercise in localized["exercises"]))
        self.assertEqual({"choose", "fill", "reorder"}, guided_types)


if __name__ == "__main__":
    unittest.main()
