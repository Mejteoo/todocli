#!/usr/bin/env bash
set -euo pipefail

# 0. Myślimy, skąd skrypt jest wywoływany
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
echo "🔧 Pracujemy w: $PWD"

# 1. Próbujemy połączyć się z PostgreSQL
PG_HOST="${PGHOST:-localhost}"
PG_PORT="${PGPORT:-5432}"
PG_USER="${PGUSER:-todo_user}"
PG_DB="${PGDATABASE:-todo_db}"
PG_PW="${PGPASSWORD:-secret}"

if ! PGPASSWORD="$PG_PW" psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" -c '\q' &>/dev/null; then
  echo "⚙️  PostgreSQL niedostępny. Uruchamiam Dockera z Postgresem..."
  # Usuń stary kontener, jeśli istnieje
  docker rm -f todo-postgres 2>/dev/null || true
  docker run -d --name todo-postgres \
    -e POSTGRES_USER="$PG_USER" \
    -e POSTGRES_PASSWORD="$PG_PW" \
    -e POSTGRES_DB="$PG_DB" \
    -p "$PG_PORT:5432" \
    postgres:13

  echo "⌛ Czekam na start PostgreSQL..."
  until PGPASSWORD="$PG_PW" psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" -c '\q' &>/dev/null; do
    sleep 1
  done
  echo "✅ PostgreSQL działa w Dockerze"
else
  echo "✅ Połączenie z PostgreSQL jest OK"
fi

# 2. Tworzymy i aktywujemy venv
if [ ! -d "venv" ]; then
  echo "✅ Tworzę virtualenv..."
  python3 -m venv venv
fi
# shellcheck disable=SC1091
source venv/bin/activate

# 3. Instalacja zależności
echo "🔄 Uaktualniam pip, setuptools i wheel..."
pip install --upgrade pip setuptools wheel

echo "📦 Instaluję aplikację w trybie editable z testami..."
pip install -e .[test]

# 4. Konfiguracja config.toml
CONFIG_DIR="$HOME/.todo"
CONFIG_FILE="$CONFIG_DIR/config.toml"
if [ ! -f "$CONFIG_FILE" ]; then
  echo "🛠️  Tworzę domyślny plik konfiguracyjny: $CONFIG_FILE"
  mkdir -p "$CONFIG_DIR"
  cat > "$CONFIG_FILE" <<EOF
[database]
dsn = "dbname=$PG_DB user=$PG_USER password=$PG_PW host=$PG_HOST port=$PG_PORT"

[cli]
default_priority = "medium"
EOF
else
  echo "ℹ️  Plik konfiguracyjny już istnieje: $CONFIG_FILE"
fi

# 5. Migracje Alembica
echo "🚀 Wykonuję migracje bazy danych..."
alembic upgrade head

# 6. Uruchamiam testy
echo "🧪 Uruchamiam testy..."
pytest --maxfail=1 --disable-warnings -q --cov=src

echo "🎉 Instalacja i konfiguracja zakończone sukcesem!"
