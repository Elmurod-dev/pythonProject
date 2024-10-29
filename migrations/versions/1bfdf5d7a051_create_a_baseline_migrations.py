"""Create a baseline migrations

Revision ID: 1bfdf5d7a051
Revises: 5a443d442adb
Create Date: 2024-10-28 19:35:00.929759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bfdf5d7a051'
down_revision: Union[str, None] = '5a443d442adb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
