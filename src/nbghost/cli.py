from pathlib import Path

import typer
from rich.console import Console

from nbghost import __version__
from nbghost.loader import load_cells
from nbghost.order import find_order_issues

app = typer.Typer(
    name="nbghost",
    help="Catch hidden state and reproducibility bugs in Jupyter notebooks.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


@app.command()
def run(
    notebook: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        readable=True,
        help="Path to the .ipynb file to check.",
    ),
) -> None:
    """Check a notebook for reproducibility issues."""
    console.print(f"[bold]nbghost[/bold] v{__version__}")
    console.print(f"Target: [cyan]{notebook.resolve()}[/cyan]")
    console.print("[yellow]No checks implemented yet.[/yellow]")


@app.command(name="check-order")
def check_order(
    notebook: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        readable=True,
        help="Path to the .ipynb file to check.",
    ),
) -> None:
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


@app.command()
def version() -> None:
    """Show the installed version."""
    console.print(__version__)
