"""Replace is_superuser with role

Revision ID: 5f6a1b2c3d4e
Revises: fe56fa70289e
Create Date: 2026-04-22 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5f6a1b2c3d4e"
down_revision = "fe56fa70289e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user",
        sa.Column("role", sa.String(length=20), nullable=False, server_default="member"),
    )
    op.execute(
        "UPDATE \"user\" SET role = CASE WHEN is_superuser THEN 'admin' ELSE 'member' END"
    )
    op.alter_column("user", "role", server_default=None)
    op.drop_column("user", "is_superuser")


def downgrade():
    op.add_column(
        "user",
        sa.Column(
            "is_superuser",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.execute("UPDATE \"user\" SET is_superuser = (role = 'admin')")
    op.alter_column("user", "is_superuser", server_default=None)
    op.drop_column("user", "role")
