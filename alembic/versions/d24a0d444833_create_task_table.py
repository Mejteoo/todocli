"""create task table

Revision ID: <d24a0d444833>
Revises:
Create Date: YYYY-MM-DD HH:MM:SS.mmmmmm

"""

from alembic import op
import sqlalchemy as sa


# --- zostaw te dwie linie niezmienione ---
revision = "<d24a0d444833>"
down_revision = None
branch_labels = None
depends_on = None
# ------------------------------------------


def upgrade():
    # tworzymy tabelę task
    op.create_table(
        "task",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")
        ),
        sa.Column("due_date", sa.Date, nullable=True),
        sa.Column(
            "priority",
            sa.Enum("low", "medium", "high", name="task_priority"),
            nullable=False,
        ),
        sa.Column("is_done", sa.Boolean, nullable=False, server_default=sa.false()),
    )
    # indeks na (priority, is_done)
    op.create_index("idx_task_prio_done", "task", ["priority", "is_done"])


def downgrade():
    # wycofanie migracji: usuwamy indeks i tabelę
    op.drop_index("idx_task_prio_done", table_name="task")
    op.drop_table("task")
    # usuwamy typ ENUM
    op.execute("DROP TYPE task_priority")
