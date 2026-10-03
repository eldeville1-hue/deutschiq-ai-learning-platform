import ast
import re
import unittest
from pathlib import Path
from app.services.content_quality import curriculum_journey_issues, normalize_lesson_content, publication_blockers, validate_lesson_content, validate_roadmap_content
from app.content.b1_curriculum import B1_CURRICULUM, build_b1_content
from app.content.b2_curriculum import B2_CURRICULUM, build_b2_content
from app.content.foundation_curriculum import A1_CURRICULUM, A2_CURRICULUM, build_foundation_content
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
            self.assertEqual(14, content["quality_version"])
            self.assertEqual(3, len(content["assessment_rubric"]))
            self.assertEqual(3, len(set(content["examples"])))
            final = next(exercise for exercise in content["exercises"] if exercise.get("mission_role") == "final")
            self.assertLessEqual(len(final["target_patterns"]), 3)
            self.assertEqual(5, len(content["exercises"]))
            self.assertEqual("mission_loop_v1", content["learning_method"])
            self.assertEqual(5, len({exercise["id"] for exercise in content["exercises"]}))
            self.assertTrue(all(exercise.get("accessibility_label") for exercise in content["exercises"]))
            listening = next(exercise for exercise in content["exercises"] if exercise["type"] == "listening_choice")
            repeat = next(exercise for exercise in content["exercises"] if exercise["type"] == "repeat")
            self.assertTrue(listening.get("audio_text"))
            self.assertTrue(repeat.get("audio_text"))
            self.assertNotEqual(listening.get("audio_text"), repeat.get("audio_text"))
            guided_types.update(exercise["type"] for exercise in content["exercises"] if exercise["stage"] == "guided")
            self.assertTrue(all(exercise.get("misconception") for exercise in content["exercises"]))
            self.assertEqual(
                {"context_choice", "dialogue", "listening_choice", "repeat"},
                {exercise["type"] for exercise in content["exercises"] if exercise["type"] not in {"error_repair", "reorder"}},
            )
            self.assertEqual([], publication_blockers(content))
            self.assertEqual(2, len(final["conversation_turns"]))
            for language in ("ru", "de", "en"):
                localized = localize_lesson_content(content, language)
                self.assertTrue(localized["title"])
                self.assertTrue(localized["rule"])
                self.assertTrue(localized["objective"])
                self.assertTrue(localized["scenario"])
                self.assertEqual(3, len(localized["assessment_rubric"]))
                self.assertNotIn("i18n", localized)
                self.assertTrue(all("i18n" not in exercise for exercise in localized["exercises"]))
                if language != "ru":
                    visible = " ".join([
                        localized["title"], localized["rule"], localized["objective"],
                        *(exercise.get("question", "") for exercise in localized["exercises"]),
                        *(exercise.get("hint", "") for exercise in localized["exercises"]),
                        *(exercise.get("explanation", "") for exercise in localized["exercises"]),
                    ])
                    self.assertIsNone(re.search(r"[А-Яа-яЁё]", visible), f"Cyrillic leaked into {language} day {row[0]}")
        self.assertEqual({"error_repair", "reorder"}, guided_types)

    def test_b1_genitive_reference_lesson_has_five_practical_interactions(self):
        row = next(item for item in B1_CURRICULUM if item[2] == "genitive_prepositions")
        content = build_b1_content(row)
        exercises = content["exercises"]

        self.assertEqual(
            {"reorder", "context_choice", "listening_choice", "dialogue", "repeat"},
            {exercise["type"] for exercise in exercises},
        )
        self.assertEqual(5, len({exercise["id"] for exercise in exercises}))
        self.assertTrue(all(exercise.get("stage") for exercise in exercises))
        listening = next(exercise for exercise in exercises if exercise["type"] == "listening_choice")
        repeat = next(exercise for exercise in exercises if exercise["type"] == "repeat")
        self.assertIn("Während der Besprechung", listening["audio_text"])
        self.assertIn("Aufgrund eines technischen Problems", repeat["audio_text"])

        localized_answers = {
            "ru": "Время действия",
            "de": "Zeitangabe",
            "en": "Time relationship",
        }
        for language, expected in localized_answers.items():
            localized = localize_lesson_content(content, language)
            listening = next(exercise for exercise in localized["exercises"] if exercise["type"] == "listening_choice")
            self.assertEqual(expected, listening["answer"])
            self.assertIn(expected, listening["options"])

    def test_b2_track_has_16_multilingual_lessons(self):
        self.assertEqual(16, len(B2_CURRICULUM))
        self.assertEqual({1, 2, 3, 4}, {row[1] for row in B2_CURRICULUM})
        for row in B2_CURRICULUM:
            content = build_b2_content(row)
            self.assertEqual([], validate_roadmap_content(content), f"day {row[0]}")
            self.assertEqual("B2", content["track"])
            self.assertEqual(5, content["quality_version"])
            self.assertEqual(5, len(content["exercises"]))
            self.assertEqual(3, len(content["assessment_rubric"]))
            self.assertEqual(3, len(set(content["examples"])))
            self.assertLessEqual(len(content["exercises"][3]["target_patterns"]), 3)
            for language in ("ru", "de", "en"):
                localized = localize_lesson_content(content, language)
                self.assertTrue(localized["title"])
                self.assertTrue(localized["rule"])
                self.assertTrue(localized["scenario"])
                self.assertEqual(3, len(localized["assessment_rubric"]))
                self.assertTrue(all("i18n" not in exercise for exercise in localized["exercises"]))

    def test_a1_and_a2_have_complete_multilingual_learning_loops(self):
        guided_types = set()
        for level, curriculum in (("A1", A1_CURRICULUM), ("A2", A2_CURRICULUM)):
            self.assertEqual(20, len(curriculum))
            self.assertEqual({1, 2, 3, 4}, {row[1] for row in curriculum})
            for row in curriculum:
                content = build_foundation_content(row, level)
                self.assertEqual([], validate_roadmap_content(content), f"{level} day {row[0]}")
                self.assertEqual(level, content["track"])
                self.assertGreaterEqual(content["quality_version"], 5)
                self.assertEqual(5, len(content["exercises"]))
                guided_types.add(content["exercises"][0]["type"])
                exercise_types = {item["type"] for item in content["exercises"]}
                self.assertTrue({"listening_choice", "dialogue", "repeat"}.issubset(exercise_types))
                if level == "A2":
                    self.assertEqual(5, len(exercise_types))
                self.assertEqual(3, len(set(content["examples"])))
                self.assertLessEqual(len(content["exercises"][3]["target_patterns"]), 3)
                for language in ("ru", "de", "en"):
                    localized = localize_lesson_content(content, language)
                    self.assertTrue(localized["title"])
                    self.assertTrue(localized["objective"])
                    self.assertTrue(localized["scenario"])
                    self.assertTrue(all("i18n" not in item for item in localized["exercises"]))
        self.assertTrue({"reorder", "listening_choice", "error_repair", "analogy_choice"}.issubset(guided_types))

    def test_a1_and_a2_foundations_are_sequentially_prerequisite_gated(self):
        for level, curriculum in (("A1", A1_CURRICULUM), ("A2", A2_CURRICULUM)):
            lessons = [build_foundation_content(row, level) for row in curriculum]
            self.assertEqual([], lessons[0]["prerequisites"])
            for index, lesson in enumerate(lessons[1:], start=1):
                self.assertEqual([curriculum[index - 1][2]], lesson["prerequisites"])

    def test_a1_has_stable_audio_manifest_for_every_listening_moment(self):
        expected_urls = set()
        for row in A1_CURRICULUM:
            content = build_foundation_content(row, "A1")
            topic = row[2]
            prefix = f"/media/audio/a1/{topic}/"

            self.assertEqual("curated_tts", content["audio_source"])
            self.assertEqual(f"{prefix}model.mp3?v=11", content["audio_url"])
            expected_urls.add(content["audio_url"])

            listening = next(item for item in content["exercises"] if item["type"] == "listening_choice")
            repeat = next(item for item in content["exercises"] if item["type"] == "repeat")
            dialogue = next(item for item in content["exercises"] if item["type"] == "dialogue")
            self.assertEqual(f"{prefix}model.mp3?v=11", listening["audio_url"])
            self.assertEqual(f"{prefix}repeat.mp3?v=11", repeat["audio_url"])
            expected_urls.update((listening["audio_url"], repeat["audio_url"]))

            for index, turn in enumerate(dialogue["conversation_turns"], start=1):
                self.assertEqual(f"{prefix}turn-{index}.mp3?v=11", turn["audio_url"])
                expected_urls.add(turn["audio_url"])

            for language in ("ru", "de", "en"):
                localized = localize_lesson_content(content, language)
                localized_dialogue = next(item for item in localized["exercises"] if item["type"] == "dialogue")
                self.assertTrue(all(turn.get("audio_url") for turn in localized_dialogue["conversation_turns"]))

        self.assertEqual(20, len({url for url in expected_urls if url.endswith("model.mp3?v=11")}))
        self.assertGreaterEqual(len(expected_urls), 80)
        audio_root = Path(__file__).resolve().parents[1] / "static" / "audio"
        self.assertEqual(84, len(expected_urls))
        for url in expected_urls:
            audio_file = audio_root / url.split("?", 1)[0].removeprefix("/media/audio/")
            self.assertTrue(audio_file.is_file(), url)
            self.assertGreater(audio_file.stat().st_size, 1_000, url)

    def test_a2_is_a_varied_publishable_mission_path_with_stable_audio(self):
        lessons = [build_foundation_content(row, "A2") for row in A2_CURRICULUM]
        expected_urls = set()
        self.assertEqual([5, 10, 15, 20], [item["day"] for item in lessons if item.get("checkpoint")])
        self.assertEqual(5, len({item["experience_type"] for item in lessons}))
        sequences = [tuple(exercise["type"] for exercise in item["exercises"]) for item in lessons]
        self.assertEqual(5, len(set(sequences)))
        self.assertFalse(any(left == right for left, right in zip(sequences, sequences[1:])))
        for row, content in zip(A2_CURRICULUM, lessons):
            topic = row[2]
            prefix = f"/media/audio/a2/{topic}/"
            self.assertEqual(13, content["quality_version"])
            self.assertEqual("curated_tts", content["audio_source"])
            self.assertEqual(f"{prefix}model.mp3?v=13", content["audio_url"])
            expected_urls.add(content["audio_url"])
            self.assertEqual([], validate_roadmap_content(content), f"A2 day {content['day']}")
            self.assertEqual([], publication_blockers(content))
            listening = next(item for item in content["exercises"] if item["type"] == "listening_choice")
            repeat = next(item for item in content["exercises"] if item["type"] == "repeat")
            dialogue = next(item for item in content["exercises"] if item["type"] == "dialogue")
            self.assertEqual(f"{prefix}model.mp3?v=13", listening["audio_url"])
            self.assertEqual(f"{prefix}repeat.mp3?v=13", repeat["audio_url"])
            expected_urls.update((listening["audio_url"], repeat["audio_url"]))
            self.assertTrue(all(turn.get("audio_url", "").startswith(prefix) for turn in dialogue["conversation_turns"]))
            expected_urls.update(turn["audio_url"] for turn in dialogue["conversation_turns"])
            for language in ("ru", "de", "en"):
                localized = localize_lesson_content(content, language)
                localized_dialogue = next(item for item in localized["exercises"] if item["type"] == "dialogue")
                self.assertTrue(all(turn.get("audio_url") for turn in localized_dialogue["conversation_turns"]))
        self.assertEqual(84, len(expected_urls))
        audio_root = Path(__file__).resolve().parents[1] / "static" / "audio"
        for url in expected_urls:
            audio_file = audio_root / url.split("?", 1)[0].removeprefix("/media/audio/")
            self.assertTrue(audio_file.is_file(), url)
            self.assertGreater(audio_file.stat().st_size, 1_000, url)

    def test_a1_first_conversation_is_a_connected_five_lesson_module(self):
        lessons = [build_foundation_content(row, "A1") for row in A1_CURRICULUM[:5]]

        self.assertEqual([1, 2, 3, 4, 5], [item["module_step"] for item in lessons])
        self.assertTrue(all(item["module_size"] == 5 for item in lessons))
        self.assertTrue(all(item["quality_version"] == 10 for item in lessons))
        self.assertTrue(all(item["learning_method"] == "mission_loop_v1" for item in lessons))
        self.assertTrue(all(item["module_title"] == "Первый разговор" for item in lessons))
        self.assertTrue(all(item.get("can_do") for item in lessons))
        self.assertFalse(any(item.get("checkpoint") for item in lessons[:-1]))
        self.assertTrue(lessons[-1]["checkpoint"])
        self.assertEqual([], lessons[0]["prerequisites"])
        self.assertEqual(["greetings"], lessons[1]["prerequisites"])
        checkpoint_exercise = lessons[-1]["exercises"][3]
        self.assertEqual(3, len(checkpoint_exercise["conversation_turns"]))
        self.assertEqual(["heiße", "woher", "wo"], checkpoint_exercise["target_patterns"])
        self.assertIn("Woher kommst du?", checkpoint_exercise["model_answer"])

        expected_shapes = [
            ["reorder", "analogy_choice", "listening_choice", "dialogue", "repeat"],
            ["listening_choice", "context_choice", "reorder", "dialogue", "repeat"],
            ["error_repair", "context_choice", "listening_choice", "dialogue", "repeat"],
            ["analogy_choice", "listening_choice", "context_choice", "dialogue", "repeat"],
            ["listening_choice", "error_repair", "analogy_choice", "dialogue", "repeat"],
        ]
        self.assertEqual(expected_shapes, [[exercise["type"] for exercise in content["exercises"]] for content in lessons])
        self.assertEqual(5, len({content["experience_type"] for content in lessons}))
        for content in lessons:
            self.assertEqual([], validate_roadmap_content(content))
            self.assertEqual(5, len({exercise["id"] for exercise in content["exercises"]}))
            self.assertTrue(all(exercise.get("accessibility_label") for exercise in content["exercises"]))
            self.assertTrue(content["mission"])
            self.assertTrue(content["success_evidence"])
            final = [item for item in content["exercises"] if item.get("mission_role") == "final"]
            self.assertEqual(1, len(final))
            self.assertGreaterEqual(len(final[0]["conversation_turns"]), 2)
            for language in ("ru", "de", "en"):
                localized = localize_lesson_content(content, language)
                self.assertTrue(localized["module_title"])
                self.assertTrue(localized["can_do"])
                self.assertTrue(localized["communication_goal"])
                self.assertTrue(localized["mission"])
                self.assertTrue(localized["success_evidence"])
                self.assertTrue(all(exercise.get("accessibility_label") for exercise in localized["exercises"]))
                analogies = [item for item in localized["exercises"] if item["type"] == "analogy_choice"]
                if analogies:
                    self.assertTrue(analogies[0].get("analogy_source"))
                    self.assertTrue(analogies[0].get("analogy_target"))
                    self.assertTrue(analogies[0].get("pattern_label"))
                self.assertGreaterEqual(len(localized["exercises"][3]["conversation_turns"]), 2)
                if content.get("checkpoint"):
                    self.assertEqual(3, len(localized["exercises"][3]["conversation_turns"]))

    def test_every_a1_lesson_is_a_validated_mission_and_each_module_has_a_checkpoint(self):
        lessons = [build_foundation_content(row, "A1") for row in A1_CURRICULUM]

        self.assertTrue(all(item["quality_version"] == 10 for item in lessons))
        self.assertTrue(all(item["learning_method"] == "mission_loop_v1" for item in lessons))
        self.assertEqual([5, 10, 15, 20], [item["day"] for item in lessons if item.get("checkpoint")])
        self.assertEqual(4, len({item["module_title"] for item in lessons}))
        self.assertEqual(5, len({item["experience_type"] for item in lessons}))
        sequences = [tuple(exercise["type"] for exercise in item["exercises"]) for item in lessons]
        self.assertEqual(5, len(set(sequences)))
        self.assertFalse(any(left == right for left, right in zip(sequences, sequences[1:])))
        for module in range(1, 5):
            module_lessons = [item for item in lessons if item["module"] == module]
            self.assertEqual([1, 2, 3, 4, 5], [item["module_step"] for item in module_lessons])
            self.assertTrue(module_lessons[-1]["checkpoint"])
        for content in lessons:
            self.assertEqual([], validate_roadmap_content(content), f"A1 day {content['day']}")
            final = [item for item in content["exercises"] if item.get("mission_role") == "final"]
            self.assertEqual(1, len(final))
            self.assertGreaterEqual(len(final[0]["conversation_turns"]), 2)
            self.assertTrue(content["mission"])
            self.assertTrue(content["success_evidence"])
            self.assertEqual([], publication_blockers(content))
            self.assertEqual("targeted_retry", content["repair_flow"]["mode"])
            self.assertEqual("changed_context_retrieval", content["delayed_review"]["method"])
            self.assertEqual({"ru", "de"}, {language for language, status in content["content_review"]["languages"].items() if status == "reviewed"})
            final_question = final[0]["question"]
            for language in ("ru", "de"):
                localized = localize_lesson_content(content, language)
                self.assertTrue(localized["delayed_review"]["reason"])
                self.assertNotEqual(final_question, localized["delayed_review"]["prompt"])

    def test_complete_a1_journey_has_no_sequence_gaps(self):
        lessons = []
        for index, row in enumerate(A1_CURRICULUM, start=1):
            lessons.append(type("Lesson", (), {"id": index, "topic": row[2], "content": build_foundation_content(row, "A1")})())
        self.assertEqual([], curriculum_journey_issues(lessons))

        lessons[9].content["prerequisites"] = ["wrong_topic"]
        self.assertIn("journey:day_10_prerequisite_gap", curriculum_journey_issues(lessons))

        for lesson in lessons:
            lesson.content["exercises"] = lessons[0].content["exercises"]
        self.assertIn("journey:exercise_shapes_too_repetitive", curriculum_journey_issues(lessons))
        self.assertIn("journey:adjacent_exercise_shapes_repeat", curriculum_journey_issues(lessons))

    def test_complete_b1_journey_is_publishable_and_connected(self):
        lessons = [
            type("Lesson", (), {"id": index, "topic": row[2], "content": build_b1_content(row)})()
            for index, row in enumerate(B1_CURRICULUM, start=1)
        ]

        self.assertEqual(
            [],
            curriculum_journey_issues(lessons, 24, list(range(31, 55)), [36, 42, 48, 54]),
        )
        self.assertEqual([36, 42, 48, 54], [lesson.content["day"] for lesson in lessons if lesson.content["checkpoint"]])
        self.assertEqual(6, len({tuple(exercise["type"] for exercise in lesson.content["exercises"]) for lesson in lessons}))
        self.assertTrue(all(not publication_blockers(lesson.content) for lesson in lessons))

    def test_v8_publication_gate_blocks_unreviewed_content(self):
        content = build_foundation_content(A1_CURRICULUM[0], "A1")
        content["content_review"]["languages"]["de"] = "pending"
        content["delayed_review"].pop("i18n")

        blockers = publication_blockers(content)

        self.assertIn("review:de:not_reviewed", blockers)
        self.assertIn("review:ru:missing_copy", blockers)
        self.assertIn("review:de:missing_copy", blockers)

    def test_every_a2_lesson_is_a_connected_mission_with_independent_checkpoints(self):
        lessons = [build_foundation_content(row, "A2") for row in A2_CURRICULUM]

        self.assertEqual(20, len(lessons))
        self.assertTrue(all(item["quality_version"] == 13 for item in lessons))
        self.assertTrue(all(item["learning_method"] == "mission_loop_v1" for item in lessons))
        self.assertEqual([5, 10, 15, 20], [item["day"] for item in lessons if item.get("checkpoint")])
        self.assertEqual(4, len({item["module_title"] for item in lessons}))
        for module in range(1, 5):
            module_lessons = [item for item in lessons if item["module"] == module]
            self.assertEqual([1, 2, 3, 4, 5], [item["module_step"] for item in module_lessons])
            self.assertTrue(module_lessons[-1]["checkpoint"])
            self.assertEqual(3, len(module_lessons[-1]["exercises"][3]["conversation_turns"]))
        for content in lessons:
            self.assertEqual([], validate_roadmap_content(content), f"A2 day {content['day']}")
            self.assertEqual(5, len({exercise["type"] for exercise in content["exercises"]}))
            final = [item for item in content["exercises"] if item.get("mission_role") == "final"]
            self.assertEqual(1, len(final))
            self.assertGreaterEqual(len(final[0]["conversation_turns"]), 2)
            self.assertTrue(content["mission"])
            self.assertTrue(content["success_evidence"])

    def test_quality_v4_rejects_repetitive_or_unmapped_practice(self):
        content = {
            "quality_version": 4, "learning_method": "notice_build_use_reflect",
            "objective": "x", "rule": "x", "examples": ["x", "y", "z"], "audio_text": "x",
            "common_mistakes": ["❌ x", "✅ y"], "day": 1, "communication_goal": "x",
            "recall_prompt": "x", "cefr": "A1", "prerequisites": [],
            "exercises": [
                {"type": "fill", "stage": stage, "question": "same", "answer": "x", "explanation": "x"}
                for stage in ("guided", "independent", "transfer", "transfer", "transfer")
            ],
        }
        errors = validate_roadmap_content(content)
        self.assertIn("adaptive:insufficient_variety", errors)
        self.assertIn("adaptive:missing_misconception", errors)
        self.assertIn("adaptive:duplicate_prompt", errors)

    def test_quality_v5_requires_context_and_open_production(self):
        content = build_foundation_content(A1_CURRICULUM[0], "A1")
        content.pop("scenario")
        content["exercises"][3]["target_patterns"] = ["a", "b", "c", "d"]
        errors = validate_roadmap_content(content)
        self.assertIn("foundation:missing_scenario", errors)
        self.assertIn("foundation:overconstrained_production", errors)


if __name__ == "__main__":
    unittest.main()
