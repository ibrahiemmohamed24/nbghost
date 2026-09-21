"""Run commands inside an isolated Docker container."""

import json

import docker


def run_in_container(image, command):
    """Run a command in a fresh container from the given image and return its output."""
    client = docker.from_env()
    output = client.containers.run(image, command, remove=True)
    return output.decode("utf-8")


def execute_notebook(notebook_path, image="nbghost-runner"):
    """Run a notebook top to bottom inside an isolated container and report the result."""
    notebook_path = notebook_path.resolve()
    client = docker.from_env()

    output = client.containers.run(
        image,
        ["/data/notebook.ipynb"],
        volumes={str(notebook_path): {"bind": "/data/notebook.ipynb", "mode": "ro"}},
        remove=True,
    )

    return json.loads(output.decode("utf-8"))
