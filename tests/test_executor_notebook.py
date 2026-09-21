from pathlib import Path

from nbghost.executor import execute_notebook

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_execute_notebook_reports_success_for_clean_notebook():
    result = execute_notebook(FIXTURES_DIR / "simple_notebook.ipynb")

    assert result["success"] is True


def test_execute_notebook_reports_failure_and_position():
    notebook_path = FIXTURES_DIR / "erroring_notebook.ipynb"

    result = execute_notebook(notebook_path)

    assert result["success"] is False
    assert result["failed_at"] == 1
    assert result["error_name"] == "ZeroDivisionError"
