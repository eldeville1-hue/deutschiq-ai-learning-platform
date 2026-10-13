"""Add retention signals for the v17 learning engine."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "20260907_0002"
down_revision = "20260904_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # The baseline migration can create tables from current model metadata.
    # On a fresh database these retention fields may therefore already exist.
    connection = op.get_bind()
    inspector = inspect(connection)
    columns = {column["name"] for column in inspector.get_columns("topic_mastery")}
    additions = (
        ("correct_total", sa.Column("correct_total", sa.Integer(), nullable=False, server_default="0")),
        ("lapse_count", sa.Column("lapse_count", sa.Integer(), nullable=False, server_default="0")),
        ("stability_days", sa.Column("stability_days", sa.Float(), nullable=False, server_default="1")),
        ("last_answer_at", sa.Column("last_answer_at", sa.DateTime(timezone=True), nullable=True)),
    )
    for name, column in additions:
        if name not in columns:
            op.add_column("topic_mastery", column)

    if not inspector.has_table("product_events"):
        op.create_table(
            "product_events",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
            sa.Column("event_name", sa.String(length=64), nullable=False),
            sa.Column("properties", sa.JSON(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        )
    indexes = {index["name"] for index in inspect(connection).get_indexes("product_events")}
    if "ix_product_events_user_id" not in indexes:
        op.create_index("ix_product_events_user_id", "product_events", ["user_id"])
    if "ix_product_events_event_name" not in indexes:
        op.create_index("ix_product_events_event_name", "product_events", ["event_name"])


def downgrade() -> None:
    op.drop_table("product_events")
    op.drop_column("topic_mastery", "last_answer_at")
    op.drop_column("topic_mastery", "stability_days")
    op.drop_column("topic_mastery", "lapse_count")
    op.drop_column("topic_mastery", "correct_total")
