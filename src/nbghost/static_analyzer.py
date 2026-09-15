"""Detect notebook cells that use variables defined in a later cell."""

import ast


def _collect_names(source):
    """Return (defined_names, used_names) for a single cell's source code."""
    tree = ast.parse(source)
    defined = set()
    used = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                defined.add(node.id)
            elif isinstance(node.ctx, ast.Load):
                used.add(node.id)

    return defined, used


def find_undefined_references(cells):
    """Return a list of variables used before the cell that defines them."""
    issues = []
    defined_in_cell = {}

    cell_data = []
    for position, cell in enumerate(cells):
        source = cell.get("source", "")
        defined, used = _collect_names(source)
        cell_data.append((position, defined, used))
        for name in defined:
            if name not in defined_in_cell:
                defined_in_cell[name] = position

    for position, defined, used in cell_data:
        for name in used:
            defined_at = defined_in_cell.get(name)
            if defined_at is not None and defined_at > position:
                issues.append(
                    {
                        "position": position,
                        "variable": name,
                        "defined_at": defined_at,
                    }
                )

    return issues
