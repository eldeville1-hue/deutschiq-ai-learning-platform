"""Store privacy-safe voice learning signals for v19."""
from alembic import op
import sqlalchemy as sa

revision = "20260908_0004"
down_revision = "20260907_0003"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table("speech_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lesson_id", sa.Integer(), sa.ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True),
        sa.Column("modality", sa.String(length=16), nullable=False),
        sa.Column("match_score", sa.Integer(), nullable=True),
        sa.Column("recognized_words", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("ix_speech_attempts_user_id", "speech_attempts", ["user_id"])
    op.create_index("ix_speech_attempts_lesson_id", "speech_attempts", ["lesson_id"])
    op.create_index("ix_speech_attempts_modality", "speech_attempts", ["modality"])

def downgrade() -> None:
    op.drop_table("speech_attempts")
