import json
import logging
import unittest
from pathlib import Path

from app.core.logging_config import JsonFormatter


class ProductionHardeningTests(unittest.TestCase):
    def test_json_formatter_includes_request_context(self):
        record = logging.LogRecord("test", logging.INFO, __file__, 1, "ready", (), None)
        record.request_id = "request-1"
        record.status_code = 200
        payload = json.loads(JsonFormatter().format(record))
        self.assertEqual(payload["message"], "ready")
        self.assertEqual(payload["request_id"], "request-1")
        self.assertEqual(payload["status_code"], 200)
        self.assertNotIn("BOT_TOKEN", payload)

    def test_single_migration_head_is_defined(self):
        versions = Path(__file__).parents[1] / "migrations" / "versions"
        revisions = list(versions.glob("*.py"))
        sources = [item.read_text(encoding="utf-8") for item in revisions]
        self.assertTrue(any('revision = "20260904_0001"' in source for source in sources))
        self.assertTrue(any('revision = "20260907_0002"' in source for source in sources))
        self.assertTrue(any('down_revision = "20260904_0001"' in source for source in sources))
        self.assertTrue(all("def upgrade()" in source for source in sources))

    def test_render_blueprint_has_no_secret_values(self):
        blueprint = (Path(__file__).parents[2] / "render.yaml").read_text(encoding="utf-8")
        self.assertIn("healthCheckPath: /api/health/live", blueprint)
        for key in ("BOT_TOKEN", "DATABASE_URL", "OPENAI_API_KEY"):
            block = blueprint.split(f"- key: {key}", 1)[1].split("- key:", 1)[0]
            self.assertIn("sync: false", block)
            self.assertNotIn("value:", block)


if __name__ == "__main__":
    unittest.main()
