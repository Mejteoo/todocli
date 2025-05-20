import os
import toml
from pathlib import Path

CONFIG_PATH = Path.home() / ".todo" / "config.toml"

DEFAULT_CONFIG = {
    "database": {
        "dsn": (
            f"dbname={os.environ.get('PGDATABASE', 'todo_db')} "
            f"user={os.environ.get('PGUSER', 'todo_user')} "
            f"password={os.environ.get('PGPASSWORD', 'secret')} "
            f"host={os.environ.get('PGHOST', 'localhost')} "
            f"port={os.environ.get('PGPORT', '5432')}"
        )
    },
    "cli": {"default_priority": "medium"},
}

def load_config():
    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG
    data = toml.loads(CONFIG_PATH.read_text())
    cfg = DEFAULT_CONFIG.copy()
    for section, values in data.items():
        if section in cfg:
            cfg[section].update(values)
        else:
            cfg[section] = values
    return cfg
