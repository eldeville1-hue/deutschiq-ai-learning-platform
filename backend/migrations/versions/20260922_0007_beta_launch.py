"""closed beta invites and enrollment

Revision ID: 20260922_0007
Revises: 20260920_0006
"""
from alembic import op
import sqlalchemy as sa

revision = "20260922_0007"
down_revision = "20260920_0006"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("beta_invites", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("code", sa.String(32), nullable=False), sa.Column("label", sa.String(80), nullable=False), sa.Column("max_uses", sa.Integer(), nullable=False), sa.Column("uses", sa.Integer(), nullable=False), sa.Column("active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.UniqueConstraint("code"))
    op.create_index("ix_beta_invites_code", "beta_invites", ["code"], unique=True)
    op.create_table("beta_enrollments", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("invite_id", sa.Integer(), sa.ForeignKey("beta_invites.id", ondelete="SET NULL")), sa.Column("goal", sa.String(40)), sa.Column("study_minutes", sa.Integer()), sa.Column("consent", sa.Boolean(), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.UniqueConstraint("user_id", name="uq_beta_enrollment_user"))
    op.create_index("ix_beta_enrollments_user_id", "beta_enrollments", ["user_id"])


def downgrade():
    op.drop_table("beta_enrollments")
    op.drop_table("beta_invites")

