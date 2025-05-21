
# todo-cli

**Prosty CLI To-Do zarządzany przez PostgreSQL**

---

## Spis treści

1. [Opis](#opis)  
2. [Wymagania](#wymagania)  
3. [Instalacja](#instalacja)  
4. [Konfiguracja](#konfiguracja)  
5. [Użycie](#użycie)  
6. [Komendy](#komendy)  
7. [Testy](#testy)  
8. [Migracje](#migracje)  
9. [Licencja](#licencja)  

---

## Opis

`todo-cli` to lekki interfejs w terminalu do zarządzania zadaniami „to-do” z użyciem bazy PostgreSQL.  
Pozwala na dodawanie, listowanie, oznaczanie jako wykonane oraz usuwanie zadań, a także na pełne czyszczenie listy.

---

## Wymagania

- Python ≥ 3.10  
- PostgreSQL  
- `click==8.2.0`  
- `psycopg2-binary==2.9.10`  
- `toml==0.10.2`  

---

## Instalacja

1. Sklonuj repozytorium i przejdź do katalogu:

    ```bash
    git clone https://github.com/Mejteoo/todocli.git
    cd todocli
    ```

2. Utwórz i aktywuj wirtualne środowisko:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Zainstaluj pakiet w trybie edycji (editable):

    ```bash
    pip install -e .
    ```

4. Przygotuj bazę i schemat:

    ```bash
    todo initdb
    ```

---

## Konfiguracja

Domyślne ustawienia są wczytywane z pliku:

```bash
~/.todo/config.toml
```

Przykładowy `config.toml`:

```toml
[database]
dsn = "dbname=todo_db user=todo_user password=secret host=localhost port=5432"

[cli]
default_priority = "medium"
```

---

## Użycie

```bash
# wyświetlenie pomocy
todo --help

# inicjalizacja bazy
todo initdb

# dodanie zadania
todo add "Kupić mleko" --due=2025-06-01 --prio=high

# listowanie zadań
todo list

# oznaczenie zadania jako wykonane
todo done <ID>

# usunięcie zadania
todo delete <ID>

# zresetowanie listy (usuwa wszystkie zadania i restartuje ID)
todo reset
```

---

## Komendy

| Komenda  | Opis                                                         |
| -------- | ------------------------------------------------------------ |
| `initdb` | Tworzy (lub aktualizuje) schemat w bazie                     |
| `add`    | Dodaje nowe zadanie                                          |
| `list`   | Wyświetla listę zadań (opcjonalnie wszystkie lub filtrowane) |
| `done`   | Oznacza zadanie jako wykonane                                |
| `delete` | Usuwa zadanie                                                |
| `reset`  | Czyści wszystkie zadania i restartuje numerację              |

---

## Testy

Uruchom testy z `pytest`:

```bash
pytest --cov=src
```

---

## Migracje

Migracje zarządzane są przy pomocy Alembic:

```bash
# Zarejestruj aktualny stan bazy jako „head”
alembic stamp head

# Gdy zmieniasz schemat:
alembic revision -m "opis zmiany"
alembic upgrade head
```

---

## Licencja

Ten projekt jest dostępny na licencji MIT. Zobacz też plik `LICENSE` po pełny tekst.
