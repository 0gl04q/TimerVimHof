"""Add TrainingProfile and BreathingCycle

Revision ID: a72102b7f569
Revises: 4cf56ceaf4d3
Create Date: 2024-10-27 15:13:09.093534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a72102b7f569'
down_revision: Union[str, None] = '4cf56ceaf4d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###