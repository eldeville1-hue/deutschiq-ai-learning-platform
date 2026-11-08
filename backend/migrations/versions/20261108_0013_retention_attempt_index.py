"""index learner-topic retention lookups

Revision ID: 20261108_0013
Revises: 20261023_0012
"""
from alembic import op

revision = "20261108_0013"
down_revision = "20261023_0012"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "ix_exercise_attempts_user_topic_created",
        "exercise_attempts",
        ["user_id", "topic", "created_at"],
    )


def downgrade():
    op.drop_index("ix_exercise_attempts_user_topic_created", table_name="exercise_attempts")
