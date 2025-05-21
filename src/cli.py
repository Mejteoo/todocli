#!/usr/bin/env python3
import click
import argcomplete
from config import load_config
from db import init_db, add_task, list_tasks, mark_done, delete_task, reset_tasks

_cfg = load_config()
default_prio = _cfg["cli"]["default_priority"]


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    Todo-CLI: Zarządzaj swoimi zadaniami z terminala.

    Parametry globalne:
      --due         Termin wykonania (YYYY-MM-DD).
      --prio        Priorytet zadania: low, medium (domyślny z config), high

    Filtrowanie w `todo list`:
      --filter-prio <low|medium|high>   Pokaż tylko zadania o priorytecie.
      --due-before <YYYY-MM-DD>         Pokaż zadania przed datą.
      --all                             Pokaż także ukończone.

    Komendy:
      initdb   - inicjalizuje schemat bazy danych
      add      - dodaje nowe zadanie
      list     - wyświetla listę zadań
      done     - oznacza zadanie jako wykonane
      delete   - usuwa zadanie
      reset    - kasuje wszystkie zadania i resetuje numerację

    Przykłady:
      todo initdb
      todo add "Kup chleb" --due=2025-06-01 --prio=high
      todo list --filter-prio=medium --due-before=2025-07-01
      todo done 3
      todo reset
    """
    pass


@cli.command()
def initdb():
    """Utwórz schemat bazy danych."""
    init_db()


@cli.command()
@click.argument("description", nargs=-1)
@click.option("--due", "due_date", help="Termin (YYYY-MM-DD)")
@click.option(
    "--prio",
    "priority",
    type=click.Choice(["low", "medium", "high"]),
    default=default_prio,
    help="Priorytet",
)
def add(description, due_date, priority):
    """Dodaj nowe zadanie."""
    text = " ".join(description)
    add_task(text, due_date, priority)
    click.echo(f"Zadanie dodane z priorytetem '{priority}' ✅")


@cli.command(name="list")
@click.option(
    "--all",
    "show_all",
    is_flag=True,
    default=False,
    help="Pokaż również ukończone zadania",
)
@click.option(
    "--filter-prio",
    "priority",
    type=click.Choice(["low", "medium", "high"]),
    default=None,
    help="Filtruj po priorytecie",
)
@click.option("--due-before", help="Pokaż zadania z terminem przed YYYY-MM-DD")
def _list(show_all, priority, due_before):
    """Wyświetl zadania."""
    tasks = list_tasks(show_all, priority, due_before)
    if not tasks:
        click.echo("Brak zadań do wyświetlenia.")
        return
    for t in tasks:

        if t["is_done"]:
            status = click.style("✔", fg="green")
        else:
            status = click.style(" ", fg="bright_black")

        prio = t["priority"]
        if prio == "high":
            prio_col = click.style(prio.upper(), fg="red")
        elif prio == "medium":
            prio_col = click.style(prio.upper(), fg="yellow")
        else:
            prio_col = click.style(prio.upper(), fg="green")

        due = t["due_date"].isoformat() if t["due_date"] else "-"
        click.echo(
            f"[{status}] {t['id']:>3}: {t['description']}"
            f" (due: {due}, prio: {prio_col})"
        )


@cli.command()
@click.argument("task_id", type=int)
def done(task_id):
    """Oznacz zadanie jako wykonane."""
    try:
        mark_done(task_id)
        click.echo(
            click.style(f"Zadanie {task_id} oznaczone jako wykonane ✅", fg="green")
        )
    except ValueError as e:
        click.echo(click.style(str(e), fg="red"))


@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
    """Usuń zadanie."""
    try:
        delete_task(task_id)
        click.echo(click.style(f"Zadanie {task_id} usunięte 🗑", fg="yellow"))
    except ValueError as e:
        click.echo(click.style(str(e), fg="red"))


@cli.command()
def reset():
    """Usuń wszystkie zadania i zrestartuj numerację."""
    reset_tasks()


if __name__ == "__main__":
    argcomplete.autocomplete(cli)
    cli()
