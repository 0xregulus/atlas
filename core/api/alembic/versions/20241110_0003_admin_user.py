"""admin user table

Revision ID: 20241110_0003
Revises: 20241110_0002
Create Date: 2025-11-10 14:05:00
"""

from alembic import op
import sqlalchemy as sa

revision = "20241110_0003"
down_revision = "20241110_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "adminuser",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("adminuser")
