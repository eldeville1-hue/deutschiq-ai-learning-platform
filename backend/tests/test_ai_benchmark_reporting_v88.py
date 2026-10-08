import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.benchmark_ai_evaluation_v88 import measure_ai
from tests.run_ai_benchmark_v88 import main, save_report


class AiBenchmarkReportingTests(unittest.TestCase):
    def test_small_fast_sample_cannot_pass_latency_gate(self):
        async def evaluator(answer, exercise):
            return {"source": "ai"}
        rows = [{"learner_answer": "Hallo", "exercise": {}} for _ in range(2)]
        result = asyncio.run(measure_ai(rows, evaluator))
        self.assertEqual(result["successful_count"], 2)
        self.assertFalse(result["latency_gate"])

    def test_failures_counted(self):
        async def evaluator(answer, exercise):
            raise ValueError("evaluation failed")
        result = asyncio.run(measure_ai([{"learner_answer": "x", "exercise": {}}], evaluator))
        self.assertEqual(result["successful_count"], 0)
        self.assertEqual(result["error_types"]["ValueError"], 1)

    def test_missing_credentials_report_is_persisted_and_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "ai.json")
            with patch.dict("os.environ", {"OPENAI_API_KEY": ""}):
                code = asyncio.run(main(path))
            saved = json.loads(Path(path).read_text(encoding="utf-8"))
        self.assertEqual(code, 2)
        self.assertFalse(saved["measured"])
        self.assertEqual(saved["release_gate"], "blocked")
        self.assertFalse(saved["v88_structured_evaluator_coverage"])

    def test_save_report_creates_parent_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "reports" / "ai.json"
            save_report({"release_gate": "blocked"}, str(path))
            self.assertEqual(json.loads(path.read_text())["release_gate"], "blocked")


if __name__ == "__main__":
    unittest.main()
