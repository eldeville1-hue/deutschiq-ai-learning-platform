"""Persist checkpoint submission receipts.

Revision ID: 20261127_0015
Revises: 20261115_0014
"""
from alembic import op
import sqlalchemy as sa

revision = "20261127_0015"
down_revision = "20261115_0014"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "checkpoint_receipts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("attempt_id", sa.String(64), nullable=False),
        sa.Column("request_hash", sa.String(64), nullable=False),
        sa.Column("response", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("user_id", "attempt_id", name="uq_checkpoint_receipt_user_attempt"),
    )


def downgrade():
    op.drop_table("checkpoint_receipts")
