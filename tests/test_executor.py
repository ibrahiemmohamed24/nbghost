from nbghost.executor import run_in_container


def test_can_run_a_simple_command_in_a_container():
    output = run_in_container("python:3.11-slim", ["python", "-c", "print('ok')"])

    assert output.strip() == "ok"
