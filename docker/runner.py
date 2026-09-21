import json
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main():
    notebook_path = Path(sys.argv[1])
    nb = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(nb, timeout=120)

    try:
        client.execute()
    except Exception:
        pass  # The real signal is in the cell outputs, checked below.

    for position, cell in enumerate(nb.cells):
        if cell.get("cell_type") != "code":
            continue
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                print(json.dumps({
                    "success": False,
                    "failed_at": position,
                    "error_name": output.get("ename"),
                    "error_value": output.get("evalue"),
                }))
                return

    print(json.dumps({"success": True}))


if __name__ == "__main__":
    main()
