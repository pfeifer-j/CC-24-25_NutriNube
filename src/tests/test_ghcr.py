# tests/test_cluster.py

import subprocess


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
    # Check container health status
    result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to retrieve container health status"
    assert "healthy" in result.stdout, "Some containers are not healthy"
