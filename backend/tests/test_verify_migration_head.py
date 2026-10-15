"""Regression tests for production migration-head verification."""
from unittest.mock import MagicMock, patch
import pytest
from scripts.verify_migration_head import main


def test_current_head_is_accepted():
    with patch("scripts.verify_migration_head.ScriptDirectory.from_config") as directory, patch("scripts.verify_migration_head.create_engine") as create_engine:
        directory.return_value.get_heads.return_value = ["rev_latest"]
        connection = MagicMock()
        connection.execute.return_value.scalars.return_value = ["rev_latest"]
        create_engine.return_value.connect.return_value.__enter__.return_value = connection
        main()
        create_engine.return_value.dispose.assert_called_once()


def test_stale_database_revision_is_rejected():
    with patch("scripts.verify_migration_head.ScriptDirectory.from_config") as directory, patch("scripts.verify_migration_head.create_engine") as create_engine:
        directory.return_value.get_heads.return_value = ["rev_latest"]
        connection = MagicMock()
        connection.execute.return_value.scalars.return_value = ["rev_old"]
        create_engine.return_value.connect.return_value.__enter__.return_value = connection
        with pytest.raises(RuntimeError, match="Database migration mismatch"):
            main()
        create_engine.return_value.dispose.assert_called_once()


def test_multiple_heads_are_rejected_without_database_connection():
    with patch("scripts.verify_migration_head.ScriptDirectory.from_config") as directory, patch("scripts.verify_migration_head.create_engine") as create_engine:
        directory.return_value.get_heads.return_value = ["rev_a", "rev_b"]
        with pytest.raises(RuntimeError, match="Expected one migration head"):
            main()
        create_engine.assert_not_called()
