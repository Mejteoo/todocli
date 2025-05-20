import toml
from pathlib import Path

# Default path
CONFIG_PATH = Path.home() / ".todo" / "config.toml"
# git add .
# git commit -m "Initial commit (force push)"
# git push -f origin main
# Default value
DEFAULT_CONFIG = {
    "database": {
        "dsn": "dbname=todo_db user=todo_user password=secret host=localhost port=5432"
    },
    "cli": {"default_priority": "medium"},
}


def load_config():
    """
    Wczytuje konfigurację z pliku config.toml.
    Jeśli plik nie istnieje, zwraca DEFAULT_CONFIG.
    """
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
