from pathlib import Path

from nbghost.loader import load_cells

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_load_cells_reads_cell_type_and_execution_count():
    notebook_path = FIXTURES_DIR / "simple_notebook.ipynb"

    cells = load_cells(notebook_path)

    assert len(cells) == 2
    assert cells[0] == {"cell_type": "code", "execution_count": 1, "source": "x = 1"}
    assert cells[1] == {"cell_type": "code", "execution_count": 2, "source": "print(x)"}
