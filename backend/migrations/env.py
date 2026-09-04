from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.models.base import Base

# Import every model so Alembic sees the complete metadata graph.
from app.models.badge import UserBadge  # noqa: F401
from app.models.diagnostic import DiagnosticMistake, DiagnosticResult  # noqa: F401
from app.models.learning import ExerciseAttempt, LearningSession, TopicMastery  # noqa: F401
from app.models.lesson import Lesson  # noqa: F401
from app.models.payment import Payment  # noqa: F401
from app.models.progress import UserProgress  # noqa: F401
from app.models.tutor import TutorMessage, TutorUsage  # noqa: F401
from app.models.user import User  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("%", "%%"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
