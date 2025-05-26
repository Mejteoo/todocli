import pytest
from db import (
    init_db,
    add_task,
    list_tasks,
    mark_done,
    delete_task,
    reset_tasks,
    get_conn,
)


@pytest.fixture(autouse=True)
def clear_db():
    init_db()
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE task RESTART IDENTITY;")
        conn.commit()
    yield
    conn.close()


def test_init_and_reset():
    init_db()
    add_task("A", None, "low")
    reset_tasks()
    assert list_tasks(show_all=True) == []


def test_add_and_list():
    add_task("Test", None, "medium")
    tasks = list_tasks()
    assert len(tasks) == 1
    assert tasks[0]["description"] == "Test"
    assert tasks[0]["priority"] == "medium"
    assert tasks[0]["is_done"] is False


def test_done_and_delete():
    add_task("X", None, "high")
    tid = list_tasks()[0]["id"]
    mark_done(tid)
    tasks_all = list_tasks(show_all=True)
    assert tasks_all[0]["is_done"] is True
    delete_task(tid)
    assert list_tasks(show_all=True) == []
