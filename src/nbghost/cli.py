from pathlib import Path

import typer
from rich.console import Console

from nbghost import __version__
from nbghost.loader import load_cells
from nbghost.order import find_order_issues
from nbghost.static_analyzer import find_undefined_references

app = typer.Typer(
    name="nbghost",
    help="Catch hidden state and reproducibility bugs in Jupyter notebooks.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()

NOTEBOOK_ARG = typer.Argument(
    ...,
    exists=True,
    dir_okay=False,
    readable=True,
    help="Path to the .ipynb file to check.",
)


@app.command()
def run(notebook: Path = NOTEBOOK_ARG) -> None:
    """Check a notebook for reproducibility issues."""
    console.print(f"[bold]nbghost[/bold] v{__version__}")
    console.print(f"Target: [cyan]{notebook.resolve()}[/cyan]")
    console.print("[yellow]No checks implemented yet.[/yellow]")


@app.command(name="check-order")
def check_order(notebook: Path = NOTEBOOK_ARG) -> None:
    """Check whether a notebook's cells were executed out of their written order."""
    cells = load_cells(notebook)
    issues = find_order_issues(cells)

    if not issues:
        console.print("No ordering issues found.")
        return

    for issue in issues:
        console.print(
            f"Cell at position {issue['position']} "
            f"(execution_count={issue['execution_count']}) "
            f"ran out of order."
        )
    raise typer.Exit(code=1)


@app.command(name="check-refs")
def check_refs(notebook: Path = NOTEBOOK_ARG) -> None:
    """Check whether a notebook uses variables before the cell that defines them."""
    cells = load_cells(notebook)
    issues = find_undefined_references(cells)

    if not issues:
        console.print("No undefined reference issues found.")
        return

    for issue in issues:
        console.print(
            f"Cell at position {issue['position']} uses '{issue['variable']}' "
            f"which is not defined until cell at position {issue['defined_at']}."
        )
    raise typer.Exit(code=1)


@app.command()
def version() -> None:
    """Show the installed version."""
    console.print(__version__)

