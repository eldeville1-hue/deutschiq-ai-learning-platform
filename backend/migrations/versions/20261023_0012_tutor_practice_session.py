"""persist tutor practice state

Revision ID: 20261023_0012
Revises: 20261003_0011
"""
from alembic import op
import sqlalchemy as sa

revision = "20261023_0012"
down_revision = "20261003_0011"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tutor_practice_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("exercise_text", sa.Text(), nullable=False),
        sa.Column("state", sa.String(length=24), nullable=False, server_default="awaiting_attempt"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "language", name="uq_tutor_practice_user_lang"),
    )
    op.create_index("ix_tutor_practice_sessions_user_id", "tutor_practice_sessions", ["user_id"])


def downgrade():
    op.drop_index("ix_tutor_practice_sessions_user_id", table_name="tutor_practice_sessions")
    op.drop_table("tutor_practice_sessions")
