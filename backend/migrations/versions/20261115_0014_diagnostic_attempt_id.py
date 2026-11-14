"""Deduplicate diagnostic submissions by client attempt ID.

Revision ID: 20261115_0014
Revises: 20261108_0013
"""
from alembic import op
import sqlalchemy as sa

revision = "20261115_0014"
down_revision = "20261108_0013"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("diagnostic_results", sa.Column("attempt_id", sa.String(length=64), nullable=True))
    op.create_index("ix_diagnostic_results_attempt_id", "diagnostic_results", ["attempt_id"], unique=True)


def downgrade():
    op.drop_index("ix_diagnostic_results_attempt_id", table_name="diagnostic_results")
    op.drop_column("diagnostic_results", "attempt_id")
