"""usage events table

Revision ID: 20241110_0002
Revises: 20241110_0001
Create Date: 2025-11-10 13:25:00
"""

from alembic import op
import sqlalchemy as sa

revision = "20241110_0002"
down_revision = "20241110_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "usageevent",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.String(), sa.ForeignKey("tenant.id"), nullable=False),
        sa.Column("source", sa.String(), nullable=False, server_default="ai-service"),
        sa.Column("tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("latency_ms", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("usageevent")
