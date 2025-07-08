"""auditing

Revision ID: a0eaf598177c
Revises: 0909f24dfb8a
Create Date: 2025-07-08 12:05:08.162174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0eaf598177c'
down_revision: Union[str, None] = '0909f24dfb8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False))
    op.add_column('users', sa.Column('created_by', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('updated_by', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('users', 'updated_by')
    op.drop_column('users', 'created_by')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
