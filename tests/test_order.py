from nbghost.order import find_order_issues


def test_clean_notebook_has_no_issues():
    cells = [
        {"cell_type": "code", "execution_count": 1},
        {"cell_type": "code", "execution_count": 2},
        {"cell_type": "code", "execution_count": 3},
    ]

    issues = find_order_issues(cells)

    assert issues == []


def test_out_of_order_notebook_flags_the_misplaced_cell():
    cells = [
        {"cell_type": "code", "execution_count": 1},
        {"cell_type": "code", "execution_count": 3},
        {"cell_type": "code", "execution_count": 2},
    ]

    issues = find_order_issues(cells)

    assert issues == [{"position": 2, "execution_count": 2}]


def test_markdown_and_unexecuted_cells_are_ignored():
    cells = [
        {"cell_type": "code", "execution_count": 1},
        {"cell_type": "markdown"},
        {"cell_type": "code", "execution_count": None},
        {"cell_type": "code", "execution_count": 2},
    ]

    issues = find_order_issues(cells)

    assert issues == []
