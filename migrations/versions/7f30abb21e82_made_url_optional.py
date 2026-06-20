"""made url optional

Revision ID: 7f30abb21e82
Revises: 6b154cc41467
Create Date: 2026-06-20 21:09:14.872131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f30abb21e82'
down_revision: Union[str, Sequence[str], None] = '6b154cc41467'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('projects') as batch_op:
        batch_op.alter_column('url',
               existing_type=sa.VARCHAR(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('projects') as batch_op:
        batch_op.alter_column('url',
               existing_type=sa.VARCHAR(),
               nullable=False)
