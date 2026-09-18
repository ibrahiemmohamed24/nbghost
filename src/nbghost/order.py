"""Detect notebooks where cells were executed out of their written order."""


def find_order_issues(cells):
    """Return a list of ordering issues found in the given notebook cells."""
    issues = []
    previous_count = 0

    for position, cell in enumerate(cells):
        execution_count = cell.get("execution_count")
        if execution_count is None:
            continue

        if execution_count < previous_count:
            issues.append(
                {
                    "position": position,
                    "execution_count": execution_count,
                }
            )
        else:
            previous_count = execution_count

    return issues

