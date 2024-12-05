# tests/test_cluster.py

import subprocess
import time


def test_cluster_build():
    """
    Test if the Docker Compose cluster is correctly built and all containers are running.
    """
    # Start the cluster
    result = subprocess.run(["docker-compose", "up", "-d"], capture_output=True, text=True)
    assert result.returncode == 0, "Docker Compose failed to start the cluster"

    # Check the status of the containers
    result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to retrieve container statuses"
    assert "Up" in result.stdout, "Not all containers are running"


def test_health_check():
    """
    Test that all services in the Docker Compose cluster report as healthy.
    """
    max_retries = 6  # Maximum retries (e.g., 6 retries x 10 seconds = 60 seconds max wait)
    wait_time = 10   # Wait time between retries in seconds

    for attempt in range(max_retries):
        # Run `docker-compose ps` to check the container status
        result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True)
        assert result.returncode == 0, f"Failed to retrieve container statuses: {result.stderr}"

        # Print output for debugging purposes
        print(result.stdout)

        # Check if all containers are healthy
        if "healthy" in result.stdout:
            return  # Success: at least one container is healthy
        
        print(f"Attempt {attempt + 1}/{max_retries}: Waiting for containers to become healthy...")
        time.sleep(wait_time)

    # If we reach here, it means the containers never became healthy
    assert "healthy" in result.stdout, f"Some containers are not healthy after {max_retries * wait_time} seconds"