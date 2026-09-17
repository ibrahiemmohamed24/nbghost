from nbghost.static_analyzer import find_undefined_references


def test_variable_defined_before_use_has_no_issues():
    cells = [
        {"cell_type": "code", "source": "x = 5"},
        {"cell_type": "code", "source": "print(x)"},
    ]

    issues = find_undefined_references(cells)

    assert issues == []


def test_variable_used_before_defined_is_flagged():
    cells = [
        {"cell_type": "code", "source": "print(x)"},
        {"cell_type": "code", "source": "x = 5"},
    ]

    issues = find_undefined_references(cells)

    assert issues == [{"position": 0, "variable": "x", "defined_at": 1}]


def test_builtin_and_unknown_names_are_not_flagged():
    cells = [
        {"cell_type": "code", "source": "print(len([1, 2, 3]))"},
    ]

    issues = find_undefined_references(cells)

    assert issues == []


def test_import_defines_the_imported_name():
    cells = [
        {"cell_type": "code", "source": "import pandas as pd"},
        {"cell_type": "code", "source": "pd.DataFrame()"},
    ]

    issues = find_undefined_references(cells)

    assert issues == []


def test_import_used_before_the_import_cell_is_flagged():
    cells = [
        {"cell_type": "code", "source": "df = pd.DataFrame()"},
        {"cell_type": "code", "source": "import pandas as pd"},
    ]

    issues = find_undefined_references(cells)

    assert issues == [{"position": 0, "variable": "pd", "defined_at": 1}]


def test_function_local_variable_does_not_leak_to_notebook_scope():
    cells = [
        {"cell_type": "code", "source": "def f():\n    x = 1\n    return x"},
        {"cell_type": "code", "source": "print(x)"},
        {"cell_type": "code", "source": "x = 5"},
    ]

    issues = find_undefined_references(cells)

    assert issues == [{"position": 1, "variable": "x", "defined_at": 2}]


def test_list_comprehension_variable_does_not_leak_to_notebook_scope():
    cells = [
        {"cell_type": "code", "source": "squares = [n * n for n in range(5)]"},
        {"cell_type": "code", "source": "print(n)"},
        {"cell_type": "code", "source": "n = 10"},
    ]

    issues = find_undefined_references(cells)

    assert issues == [{"position": 1, "variable": "n", "defined_at": 2}]
