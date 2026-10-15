"""Fail startup if the connected database is not at the Alembic head."""
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text
from app.core.config import settings


def main() -> None:
    script = ScriptDirectory.from_config(Config("alembic.ini"))
    heads = set(script.get_heads())
    if len(heads) != 1:
        raise RuntimeError(f"Expected one migration head, got {len(heads)}")
    engine = create_engine(settings.DATABASE_URL)
    try:
        with engine.connect() as connection:
            actual = set(connection.execute(text("SELECT version_num FROM alembic_version")).scalars())
        if actual != heads:
            raise RuntimeError(f"Database migration mismatch: actual={sorted(actual)}, expected={sorted(heads)}")
        print(f"Database migration verified: {next(iter(heads))}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
