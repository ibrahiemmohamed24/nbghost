"""Load notebook cells from a .ipynb file."""

import json
from pathlib import Path


def load_cells(notebook_path):
    """Read a .ipynb file and return a list of {cell_type, execution_count, source} dicts."""
    with open(notebook_path, encoding="utf-8") as f:
        notebook = json.load(f)

    cells = []
    for cell in notebook.get("cells", []):
        source = cell.get("source", [])
        if isinstance(source, list):
            source = "".join(source)

        cells.append(
            {
                "cell_type": cell.get("cell_type"),
                "execution_count": cell.get("execution_count"),
                "source": source,
            }
        )

    return cells

