"""persist production assessment evidence

Revision ID: 20260922_0008
Revises: 20260922_0007
"""
from alembic import op
import sqlalchemy as sa

revision = "20260922_0008"
down_revision = "20260922_0007"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("exercise_attempts", sa.Column("production_score", sa.Integer(), nullable=True))
    op.add_column("exercise_attempts", sa.Column("assessment", sa.JSON(), nullable=True))


def downgrade():
    op.drop_column("exercise_attempts", "assessment")
    op.drop_column("exercise_attempts", "production_score")
