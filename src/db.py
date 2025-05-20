import psycopg2
from psycopg2.extras import RealDictCursor
from config import load_config

# From dsn config
_config = load_config()
DSN = _config["database"]["dsn"]


def get_conn():
    return psycopg2.connect(DSN, cursor_factory=RealDictCursor)


def init_db():
    create_sql = """
    CREATE TABLE IF NOT EXISTS task (
        id SERIAL PRIMARY KEY,
        description TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        due_date DATE,
        priority VARCHAR(10) CHECK (priority IN ('low','medium','high')),
        is_done BOOLEAN DEFAULT FALSE
    );
    CREATE INDEX IF NOT EXISTS idx_task_prio_done ON task(priority, is_done);
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(create_sql)
        conn.commit()
    print("Schema initialized.")


def add_task(description: str, due_date: str | None, priority: str):
    insert_sql = (
        "INSERT INTO task (description, due_date, priority) VALUES (%s, %s, %s);"
    )
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(insert_sql, (description, due_date, priority))
        conn.commit()


def list_tasks(
    show_all: bool = False, priority: str | None = None, due_before: str | None = None
) -> list[dict]:
    sql = "SELECT id, description, due_date, priority, is_done FROM task"
    clauses, params = [], []
    if not show_all:
        clauses.append("is_done = FALSE")
    if priority:
        clauses.append("priority = %s")
        params.append(priority)
    if due_before:
        clauses.append("due_date <= %s")
        params.append(due_before)
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY due_date NULLS LAST, priority DESC, created_at"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def mark_done(task_id: int):
    update_sql = "UPDATE task SET is_done = TRUE WHERE id = %s;"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(update_sql, (task_id,))
        if cur.rowcount == 0:
            raise ValueError(f"Task with id={task_id} does not exist.")
        conn.commit()


def delete_task(task_id: int):
    delete_sql = "DELETE FROM task WHERE id = %s;"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(delete_sql, (task_id,))
        if cur.rowcount == 0:
            raise ValueError(f"Task with id={task_id} does not exist.")
        conn.commit()


def reset_tasks():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE task RESTART IDENTITY;")
        conn.commit()
    print("All tasks reset. IDs restarted.")
