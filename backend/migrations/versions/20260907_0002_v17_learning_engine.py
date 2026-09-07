"""Add retention signals for the v17 learning engine."""

from alembic import op
import sqlalchemy as sa

revision = "20260907_0002"
down_revision = "20260904_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("topic_mastery", sa.Column("correct_total", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("topic_mastery", sa.Column("lapse_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("topic_mastery", sa.Column("stability_days", sa.Float(), nullable=False, server_default="1"))
    op.add_column("topic_mastery", sa.Column("last_answer_at", sa.DateTime(timezone=True), nullable=True))
    op.create_table(
        "product_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_name", sa.String(length=64), nullable=False),
        sa.Column("properties", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_product_events_user_id", "product_events", ["user_id"])
    op.create_index("ix_product_events_event_name", "product_events", ["event_name"])


def downgrade() -> None:
    op.drop_table("product_events")
    op.drop_column("topic_mastery", "last_answer_at")
    op.drop_column("topic_mastery", "stability_days")
    op.drop_column("topic_mastery", "lapse_count")
    op.drop_column("topic_mastery", "correct_total")
