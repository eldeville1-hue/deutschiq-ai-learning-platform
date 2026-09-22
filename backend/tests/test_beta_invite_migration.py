import ast
import unittest
from pathlib import Path


class BetaInviteMigrationTests(unittest.TestCase):
    def test_first_batch_is_single_use_random_and_not_committed_as_codes(self):
        migration = Path(__file__).resolve().parents[1] / "migrations" / "versions" / "20260922_0009_closed_beta_batch.py"
        source = migration.read_text(encoding="utf-8")
        tree = ast.parse(source)

        self.assertIn('BATCH_SIZE = 15', source)
        self.assertIn('secrets.token_hex(6)', source)
        self.assertIn('max_uses, uses, active', source)
        self.assertIn('VALUES (:code, :label, 1, 0, true)', source)
        self.assertEqual("20260922_0009", next(node.value.value for node in tree.body if isinstance(node, ast.Assign) and any(getattr(target, "id", "") == "revision" for target in node.targets)))
        self.assertNotRegex(source, r'code\s*=\s*"[A-F0-9]{8,}"')


if __name__ == "__main__":
    unittest.main()
