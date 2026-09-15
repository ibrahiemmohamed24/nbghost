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
