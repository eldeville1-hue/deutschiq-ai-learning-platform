import unittest
from pathlib import Path


class BetaAcceptanceMigrationTests(unittest.TestCase):
    def test_migration_is_chained_and_creates_unique_persistent_checks(self):
        migration = Path(__file__).resolve().parents[1] / "migrations" / "versions" / "20261002_0010_beta_acceptance.py"
        source = migration.read_text(encoding="utf-8")
        self.assertIn('down_revision = "20260922_0009"', source)
        self.assertIn('"beta_acceptance_checks"', source)
        self.assertIn('unique=True', source)


if __name__ == "__main__":
    unittest.main()
