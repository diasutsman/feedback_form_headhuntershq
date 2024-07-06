"""create feedback table

Revision ID: 25cada2a9640
Revises: 
Create Date: 2024-07-06 22:04:47.771979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25cada2a9640'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('feedback',
        sa.Column('id', sa.Integer(), nullable=False, index=True, autoincrement=True, primary_key=True),
        sa.Column('score', sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('feedback')
