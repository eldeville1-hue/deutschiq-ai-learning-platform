"""Create or adopt the complete DeutschIQ v15 schema safely."""

from alembic import op
import sqlalchemy as sa

from app.models.base import Base
from app.models.badge import UserBadge  # noqa: F401
from app.models.diagnostic import DiagnosticMistake, DiagnosticResult  # noqa: F401
from app.models.learning import ExerciseAttempt, LearningSession, TopicMastery  # noqa: F401
from app.models.lesson import Lesson  # noqa: F401
from app.models.payment import Payment  # noqa: F401
from app.models.progress import UserProgress  # noqa: F401
from app.models.tutor import TutorMessage, TutorUsage  # noqa: F401
from app.models.user import User  # noqa: F401

revision = "20260904_0001"
down_revision = None
branch_labels = None
depends_on = None


def _columns(inspector: sa.Inspector, table: str) -> set[str]:
    if table not in inspector.get_table_names():
        return set()
    return {column["name"] for column in inspector.get_columns(table)}


def upgrade() -> None:
    connection = op.get_bind()

    # create_all is deliberately used only in the baseline revision. It adopts
    # legacy installations without attempting to recreate existing tables.
    Base.metadata.create_all(bind=connection)
    inspector = sa.inspect(connection)

    user_columns = _columns(inspector, "users")
    if "diagnostic_completed" not in user_columns:
        op.add_column(
            "users",
            sa.Column(
                "diagnostic_completed",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        )
        connection.execute(
            sa.text(
                "UPDATE users SET diagnostic_completed = TRUE "
                "WHERE id IN (SELECT DISTINCT user_id FROM diagnostic_results)"
            )
        )

    inspector = sa.inspect(connection)
    attempt_columns = _columns(inspector, "exercise_attempts")
    if "session_id" not in attempt_columns:
        op.add_column(
            "exercise_attempts",
            sa.Column(
                "session_id",
                sa.String(length=36),
                sa.ForeignKey("learning_sessions.id", ondelete="CASCADE"),
                nullable=True,
            ),
        )
        op.create_index(
            "ix_exercise_attempts_session_id",
            "exercise_attempts",
            ["session_id"],
            unique=False,
        )


def downgrade() -> None:
    # A baseline adoption must never destroy an existing learner database.
    pass
