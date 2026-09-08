"""Add metered speech practice for v18."""

from alembic import op
import sqlalchemy as sa

revision = "20260907_0003"
down_revision = "20260907_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "speech_usage",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("usage_date", sa.String(length=10), nullable=False),
        sa.Column("requests_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("audio_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("user_id", "usage_date", name="uq_speech_usage_user_date"),
    )
    op.create_index("ix_speech_usage_user_id", "speech_usage", ["user_id"])
    op.create_index("ix_speech_usage_usage_date", "speech_usage", ["usage_date"])


def downgrade() -> None:
    op.drop_table("speech_usage")
