"""create_user_table

Revision ID: 0909f24dfb8a
Revises: 
Create Date: 2025-07-05 19:45:19.143213

"""
from typing import Sequence, Union

from alembic import op
import sqlmodel as sa


# revision identifiers, used by Alembic.
revision: str = '0909f24dfb8a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """DO $$ BEGIN\n    CREATE TYPE role AS ENUM ('admin', 'user');\nEXCEPTION\n    WHEN duplicate_object THEN null;\nEND $$;""")

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.Column('role', sa.String(), nullable=False, server_default='user'),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.execute("""DO $$ BEGIN\n    DROP TYPE role;\nEXCEPTION\n    WHEN duplicate_object THEN null;\nEND $$;""")
