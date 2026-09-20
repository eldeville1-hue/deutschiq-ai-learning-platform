"""Keep AI tutor conversations separate for each interface language."""
from alembic import op
import sqlalchemy as sa

revision = "20260920_0006"
down_revision = "20260908_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "tutor_messages",
        sa.Column("language", sa.String(length=8), server_default="legacy", nullable=False),
    )
    op.create_index("ix_tutor_messages_language", "tutor_messages", ["language"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_tutor_messages_language", table_name="tutor_messages")
    op.drop_column("tutor_messages", "language")
