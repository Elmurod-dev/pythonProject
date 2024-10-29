"""Create a baseline migrations

Revision ID: f4b81487cada
Revises: 78b0dc8a7c07
Create Date: 2024-10-28 21:41:54.577772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4b81487cada'
down_revision: Union[str, None] = '78b0dc8a7c07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('market', sa.Column('address', sa.TEXT(), nullable=False))
    op.drop_column('market', 'longitude')
    op.drop_column('market', 'latitude')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('market', sa.Column('latitude', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.add_column('market', sa.Column('longitude', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.drop_column('market', 'address')
    # ### end Alembic commands ###