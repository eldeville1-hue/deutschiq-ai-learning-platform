import unittest
from unittest.mock import patch
import asyncio

from app.services.production_feedback import local_feedback, evaluate_production
from app.services.misconception_feedback import misconception_feedback
from app.services.answer_intelligence import evaluate_structured_answer, normalize_text


class ProductionFeedbackTests(unittest.TestCase):
    def test_b2_causation_guard_overrides_ai_and_gives_localized_advice(self):
        from app.services.production_feedback import _ai_feedback
        from types import SimpleNamespace
        import json

        exercise = {
            "question": "Belegen die Zahlen, dass Werbung den Anstieg verursacht hat?",
            "answer": "Der Anteil stieg. Die Zahlen belegen keine Ursache.",
            "assessment_criteria": ["overall_trend", "cautious_interpretation"],
        }
        payload = {
            "criteria_met": {"overall_trend": True, "cautious_interpretation": True},
            "dimension_scores": {key: 95 for key in (
                "task_completion", "grammar", "vocabulary", "coherence", "register"
            )},
            "feedback": "Sehr gut.", "improvement": "Weiter so.",
        }
        answer = "Die Zahlen zeigen einen Anstieg, aber wegen der Werbung stieg der Anteil."
        with patch("openai.OpenAI") as client:
            client.return_value.chat.completions.create.return_value = SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))]
            )
            for lang, keyword in (("de", "Werbung"), ("ru", "рекламы"), ("en", "advertising")):
                with self.subTest(lang=lang):
                    result = _ai_feedback(answer, exercise, {"cefr": "B2"}, lang)
                    self.assertFalse(result["correct"])
                    self.assertIn("cautious_interpretation", result["missing_task_parts"])
                    self.assertLess(result["dimension_scores"]["task_completion"], 60)
                    self.assertIn(keyword, result["improvement"])

    def test_b2_advertising_guard_scopes_negation_across_contrasts(self):
        from app.services.production_feedback import _unsupported_advertising_causation
        exercise = {
            "question": "Belegen die Zahlen, dass Werbung den Anstieg verursacht hat?",
            "assessment_criteria": ["cautious_interpretation"],
        }
        cases = (
            ("Die Zahlen beweisen nichts, aber wegen der Werbung stieg der Anteil.", True),
            ("Wegen der Werbung stieg der Anteil, jedoch ist die Ursache nicht belegt.", True),
            ("Die Zahlen beweisen nicht, dass Werbung den Anstieg verursacht hat.", False),
            ("Werbung könnte eine Ursache sein, aber die Daten beweisen es nicht.", False),
            ("Die Werbung hat den Anstieg nicht verursacht.", False),
        )
        for answer, expected in cases:
            with self.subTest(answer=answer):
                self.assertEqual(_unsupported_advertising_causation(answer, exercise), expected)

    def test_b2_server_guard_flags_asserted_advertising_cause_not_uncertainty(self):
        from app.services.production_feedback import _unsupported_advertising_causation
        exercise = {
            "question": "Belegen die Zahlen, dass Werbung den Anstieg verursacht hat?",
            "assessment_criteria": ["cautious_interpretation"],
        }
        self.assertTrue(_unsupported_advertising_causation(
            "Die Werbung hat den Anstieg verursacht.", exercise
        ))
        self.assertTrue(_unsupported_advertising_causation(
            "Der Anstieg erfolgte wegen der Werbung.", exercise
        ))
        self.assertFalse(_unsupported_advertising_causation(
            "Die Werbung hat den Anstieg nicht verursacht.", exercise
        ))
        self.assertFalse(_unsupported_advertising_causation(
            "Die Zahlen beweisen nicht, dass Werbung den Anstieg verursacht hat.", exercise
        ))
        self.assertFalse(_unsupported_advertising_causation(
            "Werbung könnte eine Ursache sein, aber das ist nicht belegt.", exercise
        ))

    def test_b2_evidence_conclusion_requires_cautious_interpretation(self):
        from app.services.production_feedback import _ai_feedback
        from types import SimpleNamespace
        import json

        exercise = {
            "question": "Belegen die Zahlen, dass Werbung den Anstieg verursacht hat? Begründe.",
            "answer": "Der Anteil stieg von 25 auf 35 Prozent. Eine Ursache ist nicht belegt.",
            "data_figures": {
                "earlier": {"year": 2020, "percent": 25},
                "later": {"year": 2025, "percent": 35},
            },
            "assessment_criteria": [
                "overall_trend", "numeric_value_and_period", "cautious_interpretation",
            ],
        }
        responses = (
            (
                "2020: 25 %, 2025: 35 %. Der Anteil stieg um 10 Prozentpunkte. "
                "Die Werbung hat den Anstieg verursacht.",
                False,
            ),
            (
                "2020: 25 %, 2025: 35 %. Der Anteil stieg um 10 Prozentpunkte. "
                "Die Zahlen zeigen einen Anstieg, beweisen aber keinen Einfluss der Werbung.",
                True,
            ),
        )
        with patch("openai.OpenAI") as client:
            for answer, cautious in responses:
                with self.subTest(cautious=cautious):
                    payload = {
                        "criteria_met": {
                            "overall_trend": True,
                            "numeric_value_and_period": True,
                            "cautious_interpretation": cautious,
                        },
                        "dimension_scores": {key: 95 for key in (
                            "task_completion", "grammar", "vocabulary", "coherence", "register"
                        )},
                        "feedback": "Bewertet.", "improvement": "Weiter üben.",
                    }
                    client.return_value.chat.completions.create.return_value = SimpleNamespace(
                        choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))]
                    )
                    result = _ai_feedback(answer, exercise, {"cefr": "B2"}, "de")
                    self.assertEqual(result["correct"], cautious)
                    if not cautious:
                        self.assertIn("cautious_interpretation", result["missing_task_parts"])
                        self.assertLess(result["dimension_scores"]["task_completion"], 60)
                    else:
                        self.assertNotIn("cautious_interpretation", result["missing_task_parts"])

    def test_b2_arithmetic_guards_cover_decrease_and_stable_scenarios(self):
        from app.services.production_feedback import (
            _incorrect_percentage_point_claim, _incorrect_year_value_pair,
        )
        scenarios = [
            (
                {"earlier": {"year": 2022, "percent": 60},
                 "later": {"year": 2026, "percent": 45}},
                "2022: 45 %, 2026: 60 %.",
                "2022: 60 %, 2026: 45 %.",
                "Der Anteil sank um 12 Prozentpunkte.",
                "Der Anteil sank um 15 Prozentpunkte.",
            ),
            (
                {"earlier": {"year": 2021, "percent": 40},
                 "later": {"year": 2025, "percent": 40}},
                "2021: 35 %, 2025: 40 %.",
                "2021: 40 %, 2025: 40 %.",
                "Der Anteil änderte sich um 5 Prozentpunkte.",
                "Der Anteil änderte sich um 0 Prozentpunkte.",
            ),
        ]
        for figures, wrong_pair, correct_pair, wrong_delta, correct_delta in scenarios:
            with self.subTest(figures=figures):
                exercise = {"data_figures": figures}
                self.assertTrue(_incorrect_year_value_pair(wrong_pair, exercise))
                self.assertFalse(_incorrect_year_value_pair(correct_pair, exercise))
                self.assertTrue(_incorrect_percentage_point_claim(wrong_delta, exercise))
                self.assertFalse(_incorrect_percentage_point_claim(correct_delta, exercise))

    def test_b2_full_answer_cannot_pass_with_swapped_figures_despite_ai_approval(self):
        from app.services.production_feedback import _ai_feedback
        from types import SimpleNamespace
        import json

        exercise = {
            "question": "Beschreibe den Anstieg und bewerte die Werbungsbehauptung.",
            "answer": "2020: 25 %, 2025: 35 %. Der Anteil stieg um 10 Prozentpunkte.",
            "data_figures": {
                "earlier": {"year": 2020, "percent": 25},
                "later": {"year": 2025, "percent": 35},
            },
            "assessment_criteria": [
                "overall_trend", "numeric_value_and_period", "cautious_interpretation"
            ],
        }
        payload = {
            "criteria_met": {key: True for key in exercise["assessment_criteria"]},
            "dimension_scores": {key: 98 for key in (
                "task_completion", "grammar", "vocabulary", "coherence", "register"
            )},
            "feedback": "Ausgezeichnet.", "improvement": "Weiter so.",
        }
        answer = (
            "2020: 35 %, 2025: 25 %. Der Anteil stieg um 10 Prozentpunkte. "
            "Diese Zahlen beweisen nicht, dass Werbung die Ursache war."
        )
        with patch("openai.OpenAI") as client:
            client.return_value.chat.completions.create.return_value = SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))]
            )
            result = _ai_feedback(answer, exercise, {"cefr": "B2"}, "de")
        self.assertFalse(result["correct"])
        self.assertIn("numeric_value_and_period", result["missing_task_parts"])
        self.assertLess(result["dimension_scores"]["task_completion"], 60)
        self.assertIn("Jahre", result["improvement"])

    def test_b2_year_value_guard_rejects_swapped_figures_not_paraphrases(self):
        from app.services.production_feedback import _incorrect_year_value_pair
        exercise = {"data_figures": {
            "earlier": {"year": 2020, "percent": 25},
            "later": {"year": 2025, "percent": 35},
        }}
        self.assertTrue(_incorrect_year_value_pair("2020: 35 %, 2025: 25 %.", exercise))
        self.assertTrue(_incorrect_year_value_pair("2020 lag der Anteil bei 35 Prozent.", exercise))
        self.assertFalse(_incorrect_year_value_pair("2020: 25 %, 2025: 35 %.", exercise))
        self.assertFalse(_incorrect_year_value_pair("2020 lag der Anteil bei 25 Prozent.", exercise))
        self.assertFalse(_incorrect_year_value_pair("Zwischen 2020 und 2025 stieg der Anteil deutlich.", exercise))

    def test_percentage_point_guard_only_rejects_explicit_wrong_difference(self):
        from app.services.production_feedback import _incorrect_percentage_point_claim
        exercise = {"data_figures": {
            "earlier": {"year": 2020, "percent": 25},
            "later": {"year": 2025, "percent": 35},
        }}
        self.assertTrue(_incorrect_percentage_point_claim("Der Anstieg beträgt 15 Prozentpunkte.", exercise))
        self.assertFalse(_incorrect_percentage_point_claim("Der Anstieg beträgt 10 Prozentpunkte.", exercise))
        self.assertFalse(_incorrect_percentage_point_claim("2020 waren es 25 Prozent, 2025 35 Prozent.", exercise))
        self.assertFalse(_incorrect_percentage_point_claim("Der Anteil stieg deutlich.", exercise))

    def test_ai_grading_receives_authoritative_variant_data_figures(self):
        from app.services.production_feedback import _ai_feedback
        from types import SimpleNamespace
        import json

        figures = {
            "earlier": {"year": 2022, "percent": 60},
            "later": {"year": 2026, "percent": 45},
        }
        exercise = {
            "question": "Beschreibe den Rückgang.",
            "answer": "Der Anteil sank um 15 Prozentpunkte.",
            "data_figures": figures,
            "assessment_criteria": ["overall_trend", "numeric_value_and_period"],
        }
        payload = {
            "criteria_met": {"overall_trend": True, "numeric_value_and_period": True},
            "dimension_scores": {key: 85 for key in (
                "task_completion", "grammar", "vocabulary", "coherence", "register"
            )},
            "feedback": "Gut.", "improvement": "Weiter so.",
        }
        with patch("openai.OpenAI") as client:
            client.return_value.chat.completions.create.return_value = SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))]
            )
            _ai_feedback("Der Anteil sank um 15 Prozentpunkte.", exercise, {"cefr": "B2"}, "de")
            request = client.return_value.chat.completions.create.call_args.kwargs
            grading_input = json.loads(request["messages"][1]["content"])
            self.assertEqual(grading_input["data_figures"], figures)
            self.assertEqual(grading_input["assessment_criteria"], exercise["assessment_criteria"])

    def test_ai_criteria_must_report_each_required_judgment(self):
        from app.services.production_feedback import _ai_feedback
        from types import SimpleNamespace
        import json

        def fake_response(criteria_met):
            payload = {
                "criteria_met": criteria_met,
                "dimension_scores": {"task_completion": 95, "grammar": 95, "vocabulary": 95, "coherence": 95, "register": 95},
                "feedback": "Gut.", "improvement": "Weiter üben.",
                "corrected_answer": "Ein Beispiel."
            }
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))])

        exercise = {
            "assessment_criteria": ["overall_trend", "numeric_value_and_period"],
            "answer": "Der Anteil stieg von 36 auf 48 Prozent.",
        }
        lesson = {"cefr": "B2"}
        with patch("openai.OpenAI") as client:
            client.return_value.chat.completions.create.return_value = fake_response({
                "overall_trend": True, "numeric_value_and_period": False,
            })
            result = _ai_feedback("Der Anteil stieg.", exercise, lesson, "de")
            self.assertFalse(result["correct"])
            self.assertIn("numeric_value_and_period", result["missing_task_parts"])
            self.assertLess(result["dimension_scores"]["task_completion"], 60)
            self.assertLess(result["score"], 95)
            client.return_value.chat.completions.create.return_value = fake_response({"overall_trend": True})
            with self.assertRaises(ValueError):
                _ai_feedback("Der Anteil stieg.", exercise, lesson, "de")

    def test_missing_b2_data_criteria_provide_actionable_multilingual_guidance(self):
        from app.services.production_feedback import _ai_feedback
        from types import SimpleNamespace
        import json

        exercise = {
            "answer": "Der Anteil stieg von 25 auf 35 Prozent.",
            "assessment_criteria": ["overall_trend", "numeric_value_and_period", "cautious_interpretation"],
        }
        payload = {
            "criteria_met": {
                "overall_trend": True, "numeric_value_and_period": True,
                "cautious_interpretation": False,
            },
            "dimension_scores": {name: 95 for name in ("task_completion", "grammar", "vocabulary", "coherence", "register")},
            "feedback": "Fast richtig.", "improvement": "Weiter üben.",
            "corrected_answer": "Die Zahlen belegen keine Ursache.",
        }
        with patch("openai.OpenAI") as client:
            client.return_value.chat.completions.create.return_value = SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))]
            )
            for language, phrase in (("ru", "рекламы"), ("de", "Werbung"), ("en", "advertising")):
                with self.subTest(language=language):
                    result = _ai_feedback("Der Anteil stieg von 25 auf 35 Prozent.", exercise, {"cefr": "B2"}, language)
                    self.assertFalse(result["correct"])
                    self.assertIn("cautious_interpretation", result["missing_task_parts"])
                    self.assertIn(phrase, result["improvement"])
                    self.assertLess(result["dimension_scores"]["task_completion"], 60)

    def test_b2_data_rubric_prompt_requires_evidence_not_causation_guess(self):
        from app.services.production_feedback import _ai_feedback
        from types import SimpleNamespace
        import json

        exercise = {
            "question": "Belegen die Zahlen, dass Werbung den Anstieg verursacht hat?",
            "answer": "Die Werte belegen keine Ursache.",
            "assessment_criteria": ["overall_trend", "numeric_value_and_period", "cautious_interpretation"],
        }
        response = {
            "criteria_met": {key: True for key in exercise["assessment_criteria"]},
            "dimension_scores": {key: 90 for key in ("task_completion", "grammar", "vocabulary", "coherence", "register")},
            "feedback": "Gut.", "improvement": "Weiter.", "corrected_answer": "Die Werte belegen keine Ursache.",
        }
        with patch("openai.OpenAI") as client:
            create = client.return_value.chat.completions.create
            create.return_value = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(response)))])
            _ai_feedback("Die Zahlen zeigen einen Anstieg, aber keine Ursache.", exercise, {"cefr": "B2"}, "de")
            system_message = create.call_args.kwargs["messages"][0]["content"]
            self.assertIn("percentage points", system_message)
            self.assertIn("mark cautious_interpretation false", system_message)
            self.assertIn("independently of German grammar", system_message)

    def test_b2_complex_rubric_never_receives_unverified_local_pass(self):
        exercise = {
            "answer": "Der Anteil stieg von 36 auf 48 Prozent.",
            "model_answer": "Der Anteil stieg von 36 auf 48 Prozent.",
            "assessment_criteria": ["overall_trend", "numeric_value_and_period", "cautious_interpretation"],
            "target_patterns": ["Anteil"],
        }
        answer = "Der Anteil ist über die Jahre deutlich gestiegen, und ich denke, das ist gut."
        lesson = {"cefr": "B2", "rule": "Beschreibe die Daten."}
        with patch("app.core.config.settings.OPENAI_API_KEY", ""):
            result = asyncio.run(evaluate_production(answer, exercise, lesson, "de"))
        self.assertFalse(result["correct"])
        self.assertTrue(result["assessment_pending"])

    def test_a1_a2_free_answers_wait_for_review_without_ai(self):
        exercise = {"answer": "Ich gehe heute nach Hause.", "type": "production"}
        for level in ("A1", "A2"):
            with self.subTest(level=level), patch("app.core.config.settings.OPENAI_API_KEY", ""):
                result = asyncio.run(evaluate_production(
                    "Ich bin heute im Park und spiele mit Freunden.",
                    exercise, {"cefr": level}, "de",
                ))
                self.assertTrue(result["assessment_pending"])
                self.assertFalse(result["correct"])

    def test_a1_a2_ai_failure_does_not_fall_back_to_heuristic_grade(self):
        exercise = {"answer": "Ich gehe heute nach Hause.", "type": "production"}
        with patch("app.core.config.settings.OPENAI_API_KEY", "test-key"), patch(
            "app.services.production_feedback._ai_feedback", side_effect=RuntimeError("unavailable")
        ):
            result = asyncio.run(evaluate_production(
                "Ich bin heute im Park und spiele mit Freunden.",
                exercise, {"cefr": "A2"}, "en",
            ))
        self.assertTrue(result["assessment_pending"])
        self.assertFalse(result["correct"])

    def test_exact_model_still_passes_without_ai_for_b2_rubric(self):
        model = "Der Anteil stieg von 36 auf 48 Prozent, also um zwölf Prozentpunkte."
        exercise = {
            "answer": model, "model_answer": model,
            "assessment_criteria": ["overall_trend", "numeric_value_and_period", "cautious_interpretation"],
        }
        with patch("app.core.config.settings.OPENAI_API_KEY", ""):
            result = asyncio.run(evaluate_production(model, exercise, {"cefr": "B2"}, "de"))
        self.assertFalse(result.get("assessment_pending", False))

    def test_structured_answers_ignore_punctuation_but_do_not_auto_accept_spelling(self):
        exercise = {"answer": "Ich habe gestern gearbeitet.", "accepted_answers": ["Ich habe gestern gearbeitet."]}
        self.assertTrue(evaluate_structured_answer("ich habe gestern gearbeitet!", exercise)["correct"])
        self.assertFalse(evaluate_structured_answer("Ich habe gestern gearbeitt.", exercise)["correct"])
        self.assertFalse(evaluate_structured_answer("Gestern ich habe gearbeitet.", exercise)["correct"])
        self.assertEqual("straße", normalize_text("Straße"))

    def test_structured_feedback_reports_missing_words(self):
        result = evaluate_structured_answer("Ich gestern gearbeitet", {"answer": "Ich habe gestern gearbeitet"})
        self.assertFalse(result["correct"])
        self.assertIn("habe", result["missing_words"])
    def test_complete_target_sentence_passes(self):
        result = local_feedback(
            "Heute lerne ich Deutsch.",
            {"target_patterns": ["lerne"], "model_answer": "Heute lerne ich Deutsch."},
            "Das Verb steht auf Position zwei.",
        )
        self.assertTrue(result["correct"])
        self.assertGreaterEqual(result["score"], 70)
        self.assertEqual(
            {"task_completion", "grammar", "vocabulary", "coherence", "register"},
            set(result["dimension_scores"]),
        )

    def test_independent_wording_can_pass_without_model_match(self):
        result = local_feedback(
            "Obwohl es heute stark regnet, fahre ich trotzdem mit dem Fahrrad zur Arbeit.",
            {"target_patterns": ["obwohl"], "model_answer": "Obwohl es regnet, gehe ich spazieren."},
            "Im obwohl-Satz steht das Verb am Ende.", "de", "B1",
        )
        self.assertTrue(result["correct"])
        self.assertEqual(result["corrected_answer"], "Obwohl es heute stark regnet, fahre ich trotzdem mit dem Fahrrad zur Arbeit.")

    def test_same_short_answer_is_judged_more_strictly_at_b2(self):
        exercise = {"target_patterns": ["weil"], "model_answer": "Ich stimme zu, weil der Vorschlag sinnvoll ist."}
        self.assertTrue(local_feedback("Ich stimme zu, weil der Vorschlag sinnvoll ist.", exercise, "x", "de", "A2")["correct"])
        # An authored exact model is valid at every CEFR; test stricter B2
        # expectations using an unlisted response instead.
        self.assertTrue(local_feedback("Ich stimme zu, weil der Vorschlag sinnvoll ist.", exercise, "x", "de", "B2")["correct"])
        self.assertFalse(local_feedback("Ich stimme zu, weil das gut ist.", exercise, "x", "de", "B2")["correct"])

    def test_off_topic_english_answer_does_not_pass(self):
        result = local_feedback("This is a long but unrelated English answer for the task.", {"target_patterns": ["obwohl"], "model_answer": "Obwohl es regnet, gehe ich."}, "x", "en", "B1")
        self.assertFalse(result["correct"])
        self.assertEqual("off_topic", result["error_type"])

    def test_short_fragment_does_not_pass(self):
        result = local_feedback(
            "Ich lerne",
            {"target_patterns": ["lerne"], "model_answer": "Heute lerne ich Deutsch."},
            "Das Verb steht auf Position zwei.",
        )
        self.assertFalse(result["correct"])

    def test_misconception_feedback_is_specific_and_localized(self):
        self.assertIn("глагол", misconception_feedback("verb_not_final", "ru"))
        self.assertIn("Verb", misconception_feedback("verb_not_final", "de"))
        self.assertIn("verb", misconception_feedback("verb_not_final", "en"))
        self.assertNotEqual(
            misconception_feedback("verb_not_final", "en"),
            misconception_feedback("case_ending", "en"),
        )


if __name__ == "__main__":
    unittest.main()
