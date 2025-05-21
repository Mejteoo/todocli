#!/usr/bin/env bash
set -euo pipefail

# Przechodzimy do katalogu skryptu
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$SCRIPT_DIR"

echo "🔧 Pracujemy w: $PWD"

# 1. Tworzymy i aktywujemy venv
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# 2. Instalacja zależności
pip install --upgrade pip setuptools wheel
pip install -e .[test]

# 3. Konfiguracja config.toml
CONFIG_FILE="$HOME/.todo/config.toml"
if [ ! -f "$CONFIG_FILE" ]; then
  mkdir -p "$(dirname "$CONFIG_FILE")"
  cat > "$CONFIG_FILE" <<EOF
[database]
dsn = "dbname=todo_db user=todo_user password=secret host=localhost port=5432"

[cli]
default_priority = "medium"
EOF
fi

# 4. Migracje Alembica
alembic upgrade head

# 5. Testy
pytest --maxfail=1 --disable-warnings -q --cov=src

echo "🎉 Instalacja i konfiguracja zakończona sukcesem!"
