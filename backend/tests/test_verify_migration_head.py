"""Regression tests for fail-closed migration-head verification."""
import unittest
from unittest.mock import MagicMock, patch
from scripts.verify_migration_head import main


class VerifyMigrationHeadTests(unittest.TestCase):
    @patch("scripts.verify_migration_head.create_engine")
    @patch("scripts.verify_migration_head.ScriptDirectory.from_config")
    def test_current_head_is_accepted(self, directory, create_engine):
        directory.return_value.get_heads.return_value = ["rev_latest"]
        connection = MagicMock()
        connection.execute.return_value.scalars.return_value = ["rev_latest"]
        create_engine.return_value.connect.return_value.__enter__.return_value = connection
        main()
        create_engine.return_value.dispose.assert_called_once()

    @patch("scripts.verify_migration_head.create_engine")
    @patch("scripts.verify_migration_head.ScriptDirectory.from_config")
    def test_stale_database_revision_is_rejected(self, directory, create_engine):
        directory.return_value.get_heads.return_value = ["rev_latest"]
        connection = MagicMock()
        connection.execute.return_value.scalars.return_value = ["rev_old"]
        create_engine.return_value.connect.return_value.__enter__.return_value = connection
        with self.assertRaisesRegex(RuntimeError, "Database migration mismatch"):
            main()
        create_engine.return_value.dispose.assert_called_once()

    @patch("scripts.verify_migration_head.create_engine")
    @patch("scripts.verify_migration_head.ScriptDirectory.from_config")
    def test_multiple_heads_are_rejected(self, directory, create_engine):
        directory.return_value.get_heads.return_value = ["rev_a", "rev_b"]
        with self.assertRaisesRegex(RuntimeError, "Expected one migration head"):
            main()
        create_engine.assert_not_called()


if __name__ == "__main__":
    unittest.main()
