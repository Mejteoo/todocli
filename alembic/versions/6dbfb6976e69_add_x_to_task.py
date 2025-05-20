"""add X to task

Revision ID: 6dbfb6976e69
Revises: <d24a0d444833>
Create Date: 2025-05-19 20:40:11.967770

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6dbfb6976e69"
down_revision: Union[str, None] = "<d24a0d444833>"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
