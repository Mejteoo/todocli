# Podsumowanie projektu **todo-cli**

## 1. Założenia projektu

* Lekki **CLI** (Command Line Interface) do zarządzania zadaniami „to-do” w terminalu
* Dane przechowywane w **PostgreSQL**
* Możliwość: dodawania, listowania, oznaczania wykonania, usuwania i resetowania zadań
* Prosta konfiguracja, migracje bazy, testy automatyczne i pakowanie jako instalowalny pakiet Python

---

## 2. Kolejne kroki i dlaczego je wykonaliśmy

1. **Struktura projektu**
   Utworzyliśmy katalog główny `todo-cli/` z podfolderami:

   * `src/` – kod źródłowy (moduły `cli.py`, `db.py`, `config.py`)
   * `tests/` – testy automatyczne
   * pliki `pyproject.toml`, `README.md`, `LICENSE`, `.github/workflows/ci.yml`

2. **Warstwa bazy danych**

   * `src/db.py` – funkcje do:

     * Inicjalizacji schematu tabeli `task`
     * Dodawania, listowania, oznaczania i usuwania zadań
     * Resetu tabeli (TRUNCATE + RESTART IDENTITY)
   * Użycie **psycopg2-binary** do połączeń z PostgreSQL
   * Stosujemy **migracje** przez **Alembic**, by wersjonować zmiany w schemacie bazy

3. **Interfejs CLI**

   * `src/cli.py` z biblioteką **Click**:

     * Grupa komend (`click.group()`) i komendy `add`, `list`, `done`, `delete`, `reset`, `initdb`
     * Kolorowanie wyjścia (`click.style`) dla lepszej czytelności statusów i priorytetów
   * Konfiguracja połączenia i domyślnych wartości w `src/config.py` czytanym z `~/.todo/config.toml`

4. **Testy automatyczne**

   * `pytest` + `pytest-cov`:

     * Testy dla każdej funkcji w `db.py` (dodawanie, listowanie, done, delete, reset)
     * Fixture `clear_db()` czyści tabelę przed każdym testem
   * Po co? Zapewniają, że zmiany w kodzie nie psują istniejącej funkcjonalności

5. **Migracje bazy**

   * **Alembic**:

     * Tworzy folder `alembic/` z plikami `env.py` i migracjami w `versions/`
     * Ręcznie dodaliśmy migrację tworzącą tabelę `task` i indeks
     * Użycie `alembic upgrade head` i `alembic stamp head`
   * Po co? Wersjonowanie schematu, możliwość rollbacku i bezpieczne rozwijanie bazy

6. **Pakowanie**

   * **`pyproject.toml`** (PEP 517):

     * Definicja metadanych pakietu, zależności i entry-point `todo = "cli:cli"`
     * Dzięki temu `pip install -e .` instaluje konsolową komendę `todo`

7. **Dokumentacja**

   * W pliku `README.md` opis instalacji, konfiguracji, użycia, testów i migracji
   * Licencja **Unlicense** w pliku `LICENSE`, pozwalająca na dowolne użycie i modyfikację kodu

8. **CI/CD**

   * GitHub Actions (`.github/workflows/ci.yml`):

     * Checkout, setup Python, instalacja `.[test]`, uruchomienie `black --check`, `flake8`, `pytest --cov`, budowanie paczki
   * Po co? Automatyczne sprawdzanie jakości kodu i testów przy każdym pushu

---

## 3. Opis użytych narzędzi i bibliotek

| Narzędzie              | Co robi / po co go wybraliśmy?                                                     |
| ---------------------- | ---------------------------------------------------------------------------------- |
| **Python 3.10+**       | Język projektu. Nowoczesny, popularny w backendzie i CLI.                          |
| **PostgreSQL**         | Relacyjna baza danych: przechowujemy zadania i ich stan.                           |
| **psycopg2-binary**    | Sterownik do łączenia się z PostgreSQL w Pythonie.                                 |
| **Click**              | Prosta biblioteka do budowy CLI: grupowanie komend, flagi, kolorowanie, help.      |
| **toml**               | Parsowanie plików `config.toml` do konfiguracji: DSN bazy, domyślny priorytet.     |
| **Alembic**            | Narzędzie do migracji bazy: wersjonowanie schematu SQL, obsługa upgrade/downgrade. |
| **pytest**             | Framework do testów jednostkowych, fixture’y, raporty.                             |
| **pytest-cov**         | Pokrycie testów (coverage report).                                                 |
| **black**              | Formatter kodu: spójny styl, unikamy dyskusji o wcięciach.                         |
| **flake8**             | Linter: wyłapia błędy stylu i potencjalne błędy logiczne.                          |
| **setuptools & wheel** | Narzędzia do budowania pakietu Python (`pyproject.toml`).                          |
| **GitHub Actions**     | CI/CD: automatyczne uruchamianie lint, testów i budowanie przy pushu.              |

---
