"""Store privacy-safe voice learning signals for v19."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "20260908_0004"
down_revision = "20260907_0003"
branch_labels = None
depends_on = None

def upgrade() -> None:
    connection = op.get_bind()
    if not inspect(connection).has_table("speech_attempts"):
        op.create_table("speech_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lesson_id", sa.Integer(), sa.ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True),
        sa.Column("modality", sa.String(length=16), nullable=False),
        sa.Column("match_score", sa.Integer(), nullable=True),
        sa.Column("recognized_words", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    indexes = {item["name"] for item in inspect(connection).get_indexes("speech_attempts")}
    for name, columns in (
        ("ix_speech_attempts_user_id", ["user_id"]),
        ("ix_speech_attempts_lesson_id", ["lesson_id"]),
        ("ix_speech_attempts_modality", ["modality"]),
    ):
        if name not in indexes:
            op.create_index(name, "speech_attempts", columns)

def downgrade() -> None:
    op.drop_table("speech_attempts")
