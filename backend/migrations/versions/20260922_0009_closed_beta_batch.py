"""create the first real closed-beta invitation batch

Revision ID: 20260922_0009
Revises: 20260922_0008
"""
import json
import secrets

from alembic import op
import sqlalchemy as sa


revision = "20260922_0009"
down_revision = "20260922_0008"
branch_labels = None
depends_on = None

BATCH_PREFIX = "Closed beta v51 tester"
BATCH_SIZE = 15


def upgrade():
    connection = op.get_bind()
    created = []
    for index in range(1, BATCH_SIZE + 1):
        label = f"{BATCH_PREFIX} {index:02d}"
        existing = connection.execute(
            sa.text("SELECT code FROM beta_invites WHERE label = :label LIMIT 1"),
            {"label": label},
        ).scalar_one_or_none()
        code = existing or secrets.token_hex(6).upper()
        if not existing:
            connection.execute(
                sa.text(
                    "INSERT INTO beta_invites (code, label, max_uses, uses, active) "
                    "VALUES (:code, :label, 1, 0, true)"
                ),
                {"code": code, "label": label},
            )
        created.append({"label": label, "code": code})
    print("BETA_INVITE_BATCH_V51=" + json.dumps(created, separators=(",", ":")))


def downgrade():
    connection = op.get_bind()
    connection.execute(
        sa.text("DELETE FROM beta_invites WHERE label LIKE :prefix AND uses = 0"),
        {"prefix": f"{BATCH_PREFIX}%"},
    )
