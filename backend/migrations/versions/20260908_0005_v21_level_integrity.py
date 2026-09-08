"""Normalize levels assigned without sufficient CEFR-band evidence."""
from alembic import op

revision = "20260908_0005"
down_revision = "20260908_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # The previous 15-question client contained no C1 questions and only one
    # B2 question, so B2/C1 assignments from that flow were not defensible.
    op.execute("UPDATE users SET current_level = 'B1' WHERE current_level IN ('B2', 'C1', 'C2')")


def downgrade() -> None:
    # The source level cannot be reconstructed safely.
    pass
