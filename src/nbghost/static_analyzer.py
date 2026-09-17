"""Detect notebook cells that use variables defined in a later cell."""

import ast


class _TopLevelNameCollector(ast.NodeVisitor):
    """Collect defined/used names at a cell's top level, respecting scope.

    Names inside function bodies, lambdas, and comprehensions are local
    to those scopes and must not leak into the notebook-level namespace.
    """

    def __init__(self):
        self.defined = set()
        self.used = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)

    def visit_Import(self, node):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)

    def visit_FunctionDef(self, node):
        self.defined.add(node.name)
        # Do not descend: parameters and body are local to the function.

    def visit_AsyncFunctionDef(self, node):
        self.defined.add(node.name)

    def visit_ClassDef(self, node):
        self.defined.add(node.name)
        # Do not descend: the class body is its own scope.

    def visit_Lambda(self, node):
        pass  # Anonymous; nothing to define, and body is local.

    def visit_ListComp(self, node):
        pass  # The loop variable is local to the comprehension.

    def visit_SetComp(self, node):
        pass

    def visit_DictComp(self, node):
        pass

    def visit_GeneratorExp(self, node):
        pass


def _collect_names(source):
    """Return (defined_names, used_names) for a single cell's source code."""
    tree = ast.parse(source)
    collector = _TopLevelNameCollector()
    for statement in tree.body:
        collector.visit(statement)
    return collector.defined, collector.used


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
