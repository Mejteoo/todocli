#!/usr/bin/env bash
set -euo pipefail

# Przechodzimy do katalogu skryptu
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
echo "🔧 Pracujemy w: $PWD"

# 1. Tworzymy i aktywujemy virtualenv
if [ ! -d "venv" ]; then
  echo "✅ Tworzę virtualenv..."
  python3 -m venv venv
fi
# shellcheck disable=SC1091
source venv/bin/activate

echo "🔄 Aktualizuję pip, setuptools i wheel..."
pip install --upgrade pip setuptools wheel

# 2. Instalujemy aplikację i zależności testowe
echo "📦 Instaluję projekt w trybie editable i testy..."
pip install -e .[test]

# 3. Instalujemy argcomplete dla automatycznego uzupełniania TAB
echo "⚡ Instaluję argcomplete i rejestruję uzupełnianie..."
pip install argcomplete
# Enable global completion for bash
activate-global-python-argcomplete --user

echo "🎉 Gotowe! Środowisko przygotowane."
