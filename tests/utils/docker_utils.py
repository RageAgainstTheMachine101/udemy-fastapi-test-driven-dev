import os
import time

import docker


def is_container_ready(container):
    container.reload()
    return container.status == "running"


def wait_for_stable_status(
    container,
    probes: int = 5,
    interval: int = 1,
    timeout: int = 30,
):
    """Waits for a container to be in a stable 'running' state.

    Args:
        container: The docker container object.
        probes (int): The number of consecutive successful 'running' checks required.
        interval (int): The time in seconds to wait between checks.
        timeout (int): The maximum time in seconds to wait for stabilization.

    Returns:
        bool: True if the container stabilizes, False otherwise.
    """
    start_time = time.time()
    stable_count = 0
    print(f"Waiting for container '{container.name}' to stabilize...")

    while time.time() - start_time < timeout:
        container.reload()
        if container.status == "running":
            stable_count += 1
            print(f"Container is ready. Stability probe {stable_count}/{probes}...")
        elif container.status in ["exited", "dead"]:
            print(f"Container has failed with status: '{container.status}'.")
            try:
                logs = container.logs().decode("utf-8")
                print(f"Container logs:\n{logs}")
            except Exception as e:
                print(f"Could not retrieve container logs: {e}")
            return False
        else:
            print(
                f"Container is not ready (status: {container.status}). "
                f"Resetting stability count."
            )
            stable_count = 0

        if stable_count >= probes:
            print(f"Container '{container.name}' is stable.")
            return True

        time.sleep(interval)

    print(f"Timeout reached. Container '{container.name}' did not stabilize.")
    return False


def start_db_container():
    client = docker.from_env()
    scripts_dir = os.path.abspath("./scripts")
    container_name = "test-db"

    try:
        existing_container = client.containers.get(container_name)
        print(f"Container '{container_name} exists. Stopping and removing...")
        existing_container.stop()
        existing_container.remove()
        print((f"Container '{container_name} stopped and removed"))
    except docker.errors.NotFound:
        print(f"Container '{container_name}' does not exist.")

    # Define container configuration
    container_config = {
        "name": container_name,
        "image": "postgres:16.1-alpine3.19",
        "detach": True,
        "ports": {"5433": "5434"},
        "environment": {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
            "POSTGRES_DB": "test_db",
            "POSTGRES_PORT": "5434",
        },
        "volumes": [f"{scripts_dir}:/docker-entrypoint-initdb.d"],
        "network_mode": "dev-network",
    }

    # Start Container
    container = client.containers.run(**container_config)

    if not wait_for_stable_status(container, timeout=60):
        raise RuntimeError("Container did not stabilize within the specified time")

    return container
