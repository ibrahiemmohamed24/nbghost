from pathlib import Path

from nbghost.executor import execute_notebook

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_execute_notebook_reports_success_for_clean_notebook():
    result = execute_notebook(FIXTURES_DIR / "simple_notebook.ipynb")

    assert result["success"] is True
