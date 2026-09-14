from pathlib import Path

import typer
from rich.console import Console

from nbghost import __version__

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


@app.command()
def version() -> None:
    """Show the installed version."""
    console.print(__version__)