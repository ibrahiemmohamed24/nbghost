"""Run commands inside an isolated Docker container."""

import docker


def run_in_container(image, command):
    """Run a command in a fresh container from the given image and return its output."""
    client = docker.from_env()
    output = client.containers.run(image, command, remove=True)
    return output.decode("utf-8")
