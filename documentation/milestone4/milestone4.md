# :pushpin: Milestone 4: Containerization and Deployment :pushpin:

## :book: NutriNube :book:  
Version 2.1.0

---

## Description of the Milestone

In this milestone, the application is containerized using Docker, enabling easier deployment and scalability. A few of these steps have already been performed in [the previous milestones](/documentation/milestone2/milestone2.md), but I will summarize it for this milestone again. A `Dockerfile` is created for the application, and the containers are orchestrated using a `docker-compose.yml` file. The Docker containers are configured, built, and uploaded to GitHub Container Registry (GHCR), with an automated build process set up using GitHub Actions. Additionally, a test to validate the functionality of the containerized cluster is implemented. The goal of this milestone is to ensure the application can be deployed in a containerized environment with automatic updates and proper configuration.

---

## 1. Container Cluster Structure Documentation

### 1.1 Cluster Overview

The container cluster structure is organized to ensure scalability, maintainability, and proper isolation of services. The main components of the cluster include:
  
- The Main Application Container contains the core application logic, developed with `Flask` in this case. It exposes the API to the frontend and other services. The application includes all dependencies required to run the API.
- The Database Container hosts the PostgreSQL database, responsible for storing the application's data.
- The FluentD Logging Container handles logging. It uses `Fluentd` ensures that logs from the `nutri_nube` application are captured and stored efficiently.

These containers are connected in a common network (`nutri_nube_network`) that allows them to communicate seamlessly.

---

### 1.2 Main Application

The main application container is responsible for hosting the logic and APIs of the NutriNube application. The container is configured to expose port `5000` for HTTP requests, and it includes the following key configurations:

- The container is built from the root of the repository, utilizing the `Dockerfile` to include necessary dependencies and setup.
- The `DATABASE_URL` environment variable connects the application to the PostgreSQL database service (`db`), ensuring it has access to the required data.
- A health check is configured to ensure the application is responding correctly by making an HTTP request to `localhost:5000`. If the service is down or unresponsive, Docker will attempt to restart the container.
- The container is configured to send logs to the `Fluentd` container using the `fluentd` logging driver.

Configuration:
```yaml
    nutri_nube:
      image: ghcr.io/pfeifer-j/nutrinube:2.0.0
      build:
        context: .
        dockerfile: Dockerfile
      container_name: nutri_nube_app
      ports:
        - "5000:5000"
      volumes:
        - ./src/app:/app
      environment:
        - DATABASE_URL=postgresql://pfeiferj:NutriNube@db:5432/flaskdb
      command: ["flask", "run", "--host=0.0.0.0"]
      depends_on:
        - fluentd
        - db
      logging:
        driver: "fluentd"
        options:
          fluentd-address: "fluentd:24224"
          tag: httpd.access
          fluentd-async-connect: "true"
          fluentd-retry-wait: 1s
          fluentd-max-retries: 30
      networks:
        - nutri_nube_network
```


---

### 1.3 Database

The database container is responsible for managing the persistent data used by the application. Key features of the database container include:
- The container is configured using environment variables to set up the PostgreSQL user, password, and database name (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB).
- The database uses Docker volumes to persist data, ensuring that the data survives container restarts or re-creations. The nutri_nube_db volume is mapped to the PostgreSQL data directory.

Configuration:

```yaml
    db:
      image: postgres:13
      container_name: nutri_nube_db
      environment:
        POSTGRES_USER: db_user
        POSTGRES_PASSWORD: db_password
        POSTGRES_DB: flaskdb
      volumes:
        - nutri_nube_db:/var/lib/postgresql/data
      networks:
        - nutri_nube_network
```

---

### 1.3 FluentD Logging

The FluentD container is responsible for aggregating logs from the nutri_nube application. It is built from a custom Dockerfile that sets up FluentD to collect and forward logs from the containers. Key configurations for the FluentD container include:
- The container mounts configuration files from the fluentd/conf directory and a log volume (nutri_nube_logs) to ensure that logs are stored persistently.
- A health check is implemented to ensure FluentD is running properly by making an HTTP request to its default port (24224). If the service is unhealthy, Docker will attempt to restart the container. This is, because this service has to be started before the main application can start. 

Configuration:
```yaml

    fluentd:
      build: ./fluentd
      container_name: nutri_nube_logger
      ports:
        - "24224:24224"
        - "24224:24224/udp"
      volumes:
        - ./fluentd/conf:/fluentd/etc
        - nutri_nube_logs:/fluentd/log
      networks:
        - nutri_nube_network
      healthcheck:
        test: ["CMD", "curl", "-f", "http://localhost:24224"]
        interval: 10s
        timeout: 5s
        retries: 3
        start_period: 5s

```

---

## 2. Continous Integration in GitHub Actions

## 2.1 Adding Credentials to GitHub Secrets

To securely authenticate and push Docker images to GHCR, credentials such as a Docker token must be added to GitHub Secrets. These secrets are securely stored and used in CI/CD pipelines to avoid hardcoding sensitive information in the repository.

### Steps to Add Credentials:
1. Navigate to your **GitHub repository**.
2. Open the **Settings** tab.
3. In the left sidebar, select **Secrets and Variables**, then click **Actions**.
4. Click the **New repository secret** button.
5. Add the following secret:
   - **Name**: `DOCKER_TOKEN`
   - **Value**: A GitHub Personal Access Token (PAT) with appropriate permissions to push images to GHCR.
     - You can generate this token in your GitHub account by following these steps:
       1. Go to **Settings** in your GitHub account.
       2. Under **Developer settings**, select **Personal Access Tokens**.
       3. Click **Generate new token**.
       4. Select the appropriate **scopes** (I chose `write:packages` and `read:packages`).
       5. Generate and copy the token.

6. Save the token.

Once the secret is added, it can be securely referenced in GitHub Actions workflows using the syntax: `${{ secrets.DOCKER_TOKEN }}`.

---

### 2.2 Updating CI.yml


The CI pipeline is defined in the [ci.yml](../../.github/workflows/ci.yml) file. This configuration sets up a two-job pipeline: **test** and **build_and_push**. The pipeline is triggered on `push` or `pull_request` events to the `main` branch. The jobs are described as follows:

```yaml
name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

permissions:
  contents: read
  packages: write

```

#### `test` Job:
This job runs on the latest Ubuntu environment and performs the following steps:
1. It uses the `actions/checkout@v3` action to clone the repository into the runner.
2. The `actions/setup-python@v4` action is used to set up Python.
3. The `pip` command is used to upgrade `pip` and install `tox`, which is used for running tests in the project.
4. Docker Compose is installed, enabling the setup and orchestration of multiple containers.
5. The command `docker-compose -f docker-compose.yml up -d` starts the containers defined in the `docker-compose.yml` file, allowing the tests to be executed against the live environment.
6. Finally, `tox` is used to run the tests defined in the project, ensuring that the code passes all tests before proceeding.

```yaml
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install tox

    - name: Install Docker Compose
      run: |
        sudo curl -L "https://github.com/docker/compose/releases/download/v2.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        docker-compose --version

    - name: Start Docker services
      run: |
        docker-compose -f docker-compose.yml up -d

    - name: Run tests
      run: tox
```



#### `build_and_push` Job:
This job depends on the successful completion of the `test` job and performs the following steps:
1. Similar to the `test` job, the `actions/checkout@v3` action is used to clone the repository into the runner.
2. The `docker/setup-buildx-action@v2` is used to enable multi-platform builds in Docker, optimizing the process of building Docker images.
3. The `docker login` command authenticates with GitHub Container Registry using the `DOCKER_TOKEN` secret. This allows pushing Docker images to GHCR securely.
4. Docker Compose is installed again to ensure that it’s available for building and pushing the Docker image.
5. The command `docker-compose -f docker-compose.yml build` builds the Docker image based on the configurations defined in `docker-compose.yml`.
6. The final step pushes the built image to the GitHub Container Registry under the tag `ghcr.io/pfeifer-j/nutrinube:2.0.0`.

The CI pipeline ensures that the application code is tested, built, and then deployed to GitHub Packages automatically with every change made to the `main` branch.



```yaml
  build_and_push:
    runs-on: ubuntu-latest
    needs: test

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Login to GitHub Container Registry
      run: |
        echo "${{ secrets.DOCKER_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin

    - name: Install Docker Compose
      run: |
        sudo curl -L "https://github.com/docker/compose/releases/download/v2.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        docker-compose --version

    - name: Build Docker image
      run: |
        docker-compose -f docker-compose.yml build 

    - name: Push Docker image to GitHub Packages (GHCR)
      run: |
        docker push ghcr.io/pfeifer-j/nutrinube:2.0.0
```

---


## 3. Testing the Cluster

### Overview

My tests can be found under [/src/tests/test_ghcr.py](../../src/tests/test_ghcr.py). These tests are designed to ensure the proper functionality of the containerized application within the Docker Compose cluster. They check if the Docker Compose setup is correctly built, if all the containers are running, and if the services are healthy. The tests verify that the cluster is properly initialized and that all its components are working as expected before the application is deployed or pushed further into production.

### Test 1: `test_cluster_build`

This test ensures that the Docker Compose cluster is correctly built and that all containers are up and running.

**Steps performed in the test:**
1. The test initiates the cluster by running `docker-compose up -d`. This command builds and starts all the services defined in the `docker-compose.yml` file in detached mode.
2. After the cluster has started, the test uses `docker-compose ps` to retrieve the status of the containers. This command checks whether the containers are up and running.
   - The first assertion checks if the return code of the `docker-compose up -d` command is 0 (indicating success).
   - The second assertion verifies that the containers are actually running by checking the output of `docker-compose ps`.

### Test 2: `test_health_check`

This test verifies that all services in the Docker Compose cluster are healthy. It checks the health status of the services after the cluster is up and running:

1. Similar to `test_cluster_build`, the test runs `docker-compose ps` to fetch the current status of all containers.
2. The test checks if the containers are healthy by searching for the word `"healthy"` in the output. It retries up to `max_retries` times (3 by default), waiting for `wait_time` seconds (5 seconds) between attempts.
   - If the `"healthy"` status is found in the output, the test passes, confirming that all containers are in a healthy state.
   - If, after the maximum number of retries, some containers are still not healthy, the test fails with a message that indicates the problem and the total waiting time.


---
