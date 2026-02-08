"""Fix missing name column in users table

Revision ID: 0004
Revises: 0003
Create Date: 2026-01-21 10:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = '0004'
down_revision: Union[str, None] = '0003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if name column exists before adding it (to avoid errors if already present)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('users')]

    if 'name' not in columns:
        op.add_column('users', sa.Column('name', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'name')