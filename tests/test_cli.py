from pathlib import Path

from typer.testing import CliRunner

from nbghost.cli import app

FIXTURES_DIR = Path(__file__).parent / "fixtures"
runner = CliRunner()


def test_check_order_exits_zero_on_clean_notebook():
    notebook_path = FIXTURES_DIR / "simple_notebook.ipynb"

    result = runner.invoke(app, ["check-order", str(notebook_path)])

    assert result.exit_code == 0
    assert "No ordering issues found" in result.stdout


def test_check_order_exits_one_on_out_of_order_notebook():
    notebook_path = FIXTURES_DIR / "broken_notebook.ipynb"

    result = runner.invoke(app, ["check-order", str(notebook_path)])

    assert result.exit_code == 1
    assert "position 2" in result.stdout


def test_check_refs_exits_zero_on_clean_notebook():
    notebook_path = FIXTURES_DIR / "simple_notebook.ipynb"

    result = runner.invoke(app, ["check-refs", str(notebook_path)])

    assert result.exit_code == 0
    assert "No undefined reference issues found" in result.stdout


def test_check_refs_exits_one_on_notebook_with_undefined_reference():
    notebook_path = FIXTURES_DIR / "messy_notebook.ipynb"

    result = runner.invoke(app, ["check-refs", str(notebook_path)])

    assert result.exit_code == 1
    assert "young_survival_rate" in result.stdout
