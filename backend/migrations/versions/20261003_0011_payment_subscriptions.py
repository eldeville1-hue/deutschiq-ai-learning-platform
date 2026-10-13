"""harden Telegram Stars subscription ledger

Revision ID: 20261003_0011
Revises: 20261002_0010
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "20261003_0011"
down_revision = "20261002_0010"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    existing = {item["name"] for item in inspect(connection).get_columns("payments")}
    columns = (
        sa.Column("telegram_payment_charge_id", sa.String(length=128), nullable=True),
        sa.Column("invoice_payload", sa.String(length=160), nullable=True),
        sa.Column("subscription_expires_at", sa.DateTime(), nullable=True),
        sa.Column("is_recurring", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_first_recurring", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("refunded_at", sa.DateTime(), nullable=True),
    )
    for column in columns:
        if column.name not in existing:
            op.add_column("payments", column)
    indexes = {item["name"] for item in inspect(connection).get_indexes("payments")}
    if "ix_payments_telegram_payment_charge_id" not in indexes:
        op.create_index("ix_payments_telegram_payment_charge_id", "payments", ["telegram_payment_charge_id"], unique=True)
    if "ix_payments_invoice_payload" not in indexes:
        op.create_index("ix_payments_invoice_payload", "payments", ["invoice_payload"], unique=False)

def downgrade():
    op.drop_index("ix_payments_invoice_payload", table_name="payments")
    op.drop_index("ix_payments_telegram_payment_charge_id", table_name="payments")
    for name in ("refunded_at", "is_first_recurring", "is_recurring", "subscription_expires_at", "invoice_payload", "telegram_payment_charge_id"):
        op.drop_column("payments", name)
