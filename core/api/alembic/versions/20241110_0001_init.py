"""initial tenant usage tables

Revision ID: 20241110_0001
Revises: 
Create Date: 2025-11-10 13:05:00
"""

from alembic import op
import sqlalchemy as sa

revision = "20241110_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tenant",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("plan", sa.String(length=10), nullable=False, server_default="trial"),
    )
    op.create_table(
        "usage",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.String(), sa.ForeignKey("tenant.id"), nullable=False),
        sa.Column("tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("requests", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_table("usage")
    op.drop_table("tenant")
