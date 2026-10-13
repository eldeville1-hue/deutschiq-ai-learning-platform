"""add persistent real-device beta acceptance checks

Revision ID: 20261002_0010
Revises: 20260922_0009
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "20261002_0010"
down_revision = "20260922_0009"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    if not inspect(connection).has_table("beta_acceptance_checks"):
        op.create_table(
            "beta_acceptance_checks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("check_id", sa.String(length=64), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("notes", sa.String(length=500), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    indexes = {item["name"] for item in inspect(connection).get_indexes("beta_acceptance_checks")}
    if "ix_beta_acceptance_checks_check_id" not in indexes:
        op.create_index("ix_beta_acceptance_checks_check_id", "beta_acceptance_checks", ["check_id"], unique=True)


def downgrade():
    op.drop_index("ix_beta_acceptance_checks_check_id", table_name="beta_acceptance_checks")
    op.drop_table("beta_acceptance_checks")
