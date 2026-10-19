"""Server-side regression checks for B2 data-description variants."""
import unittest

from fastapi import HTTPException
from app.api.endpoints.lesson import CheckAnswerRequest, resolve_practice_variant
from app.content.b2_curriculum import B2_CURRICULUM, build_b2_content


def data_exercise():
    row = next(row for row in B2_CURRICULUM if row[2] == "data_description")
    lesson = build_b2_content(row)
    return next(item for item in lesson["exercises"] if item["id"] == "data_description-dialogue")


class B2PracticeVariantTests(unittest.TestCase):
    def test_selected_variants_use_server_owned_figures_and_model(self):
        original = data_exercise()
        cases = [
            ("data_description-decrease", 60, 45, -15, "sank"),
            ("data_description-stable", 40, 40, 0, "unverändert"),
        ]
        for variant_id, earlier, later, delta, term in cases:
            with self.subTest(variant=variant_id):
                selected = resolve_practice_variant(original, original, variant_id, "en")
                figures = selected["data_figures"]
                self.assertEqual(figures["earlier"]["percent"], earlier)
                self.assertEqual(figures["later"]["percent"], later)
                self.assertEqual(figures["later"]["percent"] - figures["earlier"]["percent"], delta)
                self.assertIn(term, selected["answer"])
                self.assertEqual(selected["accepted_answers"], [selected["answer"]])
                self.assertNotEqual(selected["question"], original["question"])

    def test_transfer_prompts_require_grounded_comparison_in_all_languages(self):
        original = data_exercise()
        cases = [
            ("data_description-decrease", {2022: 60, 2026: 45}, {
                "ru": ("процентных пунктах", "Не выдумывай причины"),
                "de": ("Prozentpunkten", "Erfinde keine Ursachen"),
                "en": ("percentage points", "Do not invent causes"),
            }),
            ("data_description-stable", {2021: 40, 2025: 40}, {
                "ru": ("изменился ли", "Не выдумывай тенденцию"),
                "de": ("verändert hat", "Erfinde keinen Trend"),
                "en": ("whether the share changed", "Do not invent a trend"),
            }),
        ]
        for variant_id, year_values, language_markers in cases:
            for language, markers in language_markers.items():
                with self.subTest(variant=variant_id, language=language):
                    selected = resolve_practice_variant(original, original, variant_id, language)
                    prompt = selected["question"]
                    for year, value in year_values.items():
                        self.assertIn(str(year), prompt)
                        self.assertIn(str(value), prompt)
                        self.assertIn(str(year), selected["answer"])
                        self.assertIn(str(value), selected["answer"])
                    for marker in markers:
                        self.assertIn(marker, prompt)
                    self.assertEqual(selected["data_figures"]["earlier"]["percent"], next(iter(year_values.values())))
                    self.assertEqual(selected["data_figures"]["later"]["percent"], list(year_values.values())[1])

    def test_evidence_scenario_separates_trend_from_unproven_cause(self):
        original = data_exercise()
        for language, marker in (
            ("ru", "реклам"),
            ("de", "Werbung"),
            ("en", "advertising"),
        ):
            with self.subTest(language=language):
                selected = resolve_practice_variant(original, original, "data_description-evidence", language)
                self.assertIn(marker, selected["question"])
                self.assertIn("25", selected["question"])
                self.assertIn("35", selected["question"])
                self.assertEqual(selected["data_figures"]["later"]["percent"] - selected["data_figures"]["earlier"]["percent"], 10)
                self.assertIn("nicht", selected["answer"])
                self.assertIn("Werbung", selected["answer"])

    def test_invalid_variant_is_rejected(self):
        original = data_exercise()
        with self.assertRaises(HTTPException) as raised:
            resolve_practice_variant(original, original, "fake-data-variant", "en")
        self.assertEqual(raised.exception.status_code, 422)

    def test_variant_not_allowed_for_guided_retry(self):
        original = data_exercise()
        with self.assertRaises(HTTPException) as raised:
            resolve_practice_variant(original, original, "data_description-stable", "en", retry=True)
        self.assertEqual(raised.exception.status_code, 422)

    def test_check_answer_request_accepts_variant_identifier(self):
        request = CheckAnswerRequest(
            user_id=1, lesson_id=77, exercise_index=3,
            answer="Der Anteil blieb unverändert.", session_id="test-session",
            practice_variant_id="data_description-stable",
        )
        self.assertEqual(request.practice_variant_id, "data_description-stable")


if __name__ == "__main__":
    unittest.main()
