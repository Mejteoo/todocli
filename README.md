
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
8. [Licencja](#licencja)
9. [Koniec](#Koniec)

---

## Opis

`todo-cli` to lekki interfejs w terminalu do zarządzania zadaniami „to-do” z użyciem bazy PostgreSQL.  
Pozwala na dodawanie, listowanie, oznaczanie jako wykonane oraz usuwanie zadań, a także na pełne czyszczenie listy.

---

## Wymagania

- Python ≥ 3.10  
- PostgreSQL  
- Wszystkie paczki pythona z requirements.txt  

---

## Instalacja

1. Zainstaluj narzędzia systemowe, sklonuj repozytorium i przejdź do katalogu:

    ```bash
    sudo dnf install -y git python3 python3-pip python3-virtualenv postgresql postgresql-server postgresql-contrib
    ```
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

4. Przygotuj bazę (postgresql) i schemat:

    ```bash
    sudo postgresql-setup --initdb
    ```
    Ustaw w pliku konfiguracyjnym `pg_hba.conf` wartości na trust tak jak na screenie w .screeny/edytuj-iwpisz-trust.png

   Stwórz użytkownika i bazę danych:
   
   <sup>Skorzystaj z użytkownika i bazy danych z przykładowego pliku `~/.todo/config.toml` </sup>
    ```bash
    sudo -u postgres psql -c "CREATE USER todo_user WITH PASSWORD 'secret';"
    sudo -u postgres psql -c "CREATE DATABASE todo_db OWNER todo_user;"

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
jeśli tego pliku nie ma to utwórz go w tamtej ścieżce.
```bash
mkdir -p ~/.todo
cat > ~/.todo/config.toml <<EOF
[database]
dsn = "dbname=todo_db user=todo_user password=secret host=localhost port=5432"

[cli]
default_priority = "medium"
EOF
```
Aby autouzupełnianie działało należy wpisać te komendy, które dodają go do powłoki bash:
```bash
echo 'eval "$(register-python-argcomplete todo)"' >> ~/.bashrc && source ~/.bashrc
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

<sub>
Przed uruchomieniem testów pobierz narzędzia testowe:
</sub>
    
```bash
    pip install -e .["test"]
```

Aby testy zadziałały użyj:
```bash
    pytest --cov=src

```
---

## Licencja

Ten projekt jest dostępny na licencji MIT. Zobacz też plik `LICENSE` po pełny tekst.

---
## Koniec
lorum ipsum
test



---


