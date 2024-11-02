# :pushpin: Milestone 2: Continuous Integration and Deployment :pushpin:

## :book: NutriNube :book:  
Version 0.1.0

---

## Project Overview

In this milestone, I focused on implementing continuous integration (CI) and deployment processes for the NutriNube project, aimed at enhancing code quality and efficiency. I automated the testing and deployment pipeline using tools like `tox`, `pytest`, Docker, and GitHub Actions. This milestone also involved integrating a PostgreSQL database using Docker and implementing a simple frontend to ensure my tests run correctly. For changes made during the previous phase, see Milestone 1.

---

## 1. Continuous Integration Setup with `tox` and `pytest`

1.1 Why Choose `tox`?

- `tox` offers an easy setup for automated testing through the [tox.ini](/tox.ini) file. It integrates well with GitHub Actions to execute tests seamlessly.
- One of `tox`'s strengths is its ability to automatically create and manage virtual environments. This is especially useful for testing across different environments and Python versions.

1.2 Setting Up `tox`

To implement `tox` in the project:

1. Install `tox`:  

   
```bash
   pip install tox
```


2. Create [tox.ini](/tox.ini) File:  

```ini
   [tox]
   envlist = py312

   [testenv]
   deps =
       pytest
       pytest-flask
       pytest-mock
       flask
       flask_cors
       flask_sqlalchemy
   setenv =
       PYTHONPATH = {toxinidir}/src
       FLASK_ENV = testing
   commands = pytest {toxinidir}/src/tests
```


3. Running tests with `tox` is straightforward. Execute the following while in the same directory as the [tox.ini](/tox.ini) file:

   
```bash
   tox
```
   


1.3 Why Choose `pytest`?

- `pytest` offers an intuitive syntax for writing tests, reducing boilerplate code.
- It automatically locates and runs tests, simplifying the testing process.
- It produces clear outputs, helping in debugging.
- It works wonderfully in combination with `tox`!

Example of a simple test:

```python
def test_addition():
    assert 1 + 1 == 2
```

---

First, I got the testing environment to run with this simple test, which always returns `True`. Later, I implemented the actual tests.

## 2. Continuous Integration with GitHub Actions

2.1 Setting Up CI Workflow
#### Why Choose `GitHub CI`?

- Since we host our project on GitHub, it's the easiest way to integrate CI for our purpose.

1. Create a Workflow File: Develop [.github/workflows/ci.yml](/.github/workflows/ci.yml) to define automated CI workflows:

   
```yaml
   name: CI

   on:
     push:
       branches:
         - main
     pull_request:
       branches:
         - main

   jobs:
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

       - name: Run tests
         run: tox
   ```


   It's important to correctly define all dependencies, versions, and `tox` as the test environment.

2. I ensured this YAML file is committed to the repository, enabling automated workflow execution on each push.

3. Now, I can use the GitHub Actions tab to view and manage the workflow executions and results.

<p align="center">
  <img src="/images/github_actions_running.png" alt="GitHub Actions are running.">
</p>

## 3. Flask Application Deployment with Docker

3.1 Docker Containerization

Firstly, I got the environment up and running. I significantly changed the actual code afterward.

1. Create [app.py](/src/app/app.py):

   
```python
   from flask import Flask

   app = Flask(__name__)

   @app.route('/')
   def home():
       return "Hello, Docker!"

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
 ```  


2. Generate [requirements.txt](/src/app/requirements.txt):

   
```
   Flask
``` 


3. Construct a [Dockerfile](/src/app/Dockerfile):

   
```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY . /app
   RUN pip install --no-cache-dir -r requirements.txt
   EXPOSE 5000
   CMD ["python", "app.py"]
 ```  


4. Build & Test Docker Image:

   
```bash
   docker build -t pfeifer-j/flask-api .
   docker tag pfeifer-j/flask-api:latest
   docker push pfeifer-j/flask-api:latest
```   


5. Check if the application is running:

<p align="center">
  <img src="/images/docker_console_output.png" alt="Console output of my application in Docker">
</p>

## 4. Adding Database Support with Docker Compose

4.1 Docker Compose for Service Integration

I chose PostgreSQL because I already have experience working with it. It's quite easy to use and robust.

1. Set Up [docker-compose.yml](/src/app/docker-compose.yml):

   
```yaml
   version: '3.8'

   services:
     app:
       build: .
       ports:
         - "5000:5000"
       volumes:
         - .:/app
       depends_on:
         - db
       environment:
         - DATABASE_URL=postgresql://flaskuser:flaskpassword@db:5432/flaskdb

     db:
       image: postgres:13
       environment:
         POSTGRES_USER: flaskuser
         POSTGRES_PASSWORD: flaskpassword
         POSTGRES_DB: flaskdb
       volumes:
         - db_data:/var/lib/postgresql/data

   volumes:
     db_data:
 ```  


   Later I changed this to not use passwords in plain text but to store them in GitHub secrets.

#### Here is how to add Passwords to GitHub Secrets:

1. Go to your GitHub repository's settings.
2. Navigate to "Secrets and variables" > "Actions".
3. Add secrets. Example: `POSTGRES_USER`, `POSTGRES_PASSWORD`.

<p align="center">
  <img src="/images/github_secrets.png" alt="GitHub Secrets">
</p>

2. Update [__init__.py](/src/app/__init__.py) and [app.py](/src/app/app.py)` for Database:

``` python
   # app/__init__.py
   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy
   from flask_cors import CORS
   import os

   db = SQLAlchemy()

   def create_app():
       app = Flask(__name__)
       CORS(app)
       app.secret_key = os.urandom(24)

       # Configure the database
       app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
       app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
       db.init_app(app)

       with app.app_context():
           from . import models
           db.create_all()

       from .routes import init_routes
       init_routes(app)

       return app
   
```
And also:

```python
   # app/app.py
   from app import create_app

   app = create_app()

   if __name__ == '__main__':
       app.run(debug=True)
```   


3. After updating my [requirements.txt](/src/app/requirements.txt), I ran the Docker Compose:

   
```bash
   docker-compose up --build
 ```  


4. Test the application's interaction with the PostgreSQL database to ensure data persistence and API endpoints' efficiency.

<p align="center">
  <img src="/images/docker_postgres_output.png" alt="Console output while interacting with the app">
</p>

## 5. Adding the Backend of My Application

Under `./src/app/app`, I started to implement the application. The application is split into:

- HTML, CSS, and JS Frontend
- Python backend with routes and data models

In the following milestones, I will explain how I set up the working application in detail, but this is out of scope for Milestone 2, which focuses on testing. While creating the backend logic of my app, I also updated all the tests, which execute correctly and contain logical code:

<p align="center">
  <img src="/images/tests_working.png" alt="Executing the tests work">
</p>

## 6. Preview of the Frontend

<p align="center">
  <img src="/images/frontend_login.png" alt="Registration and Login">
</p>

<p align="center">
  <img src="/images/frontend_goal.png" alt="Adding a goal">
</p>

<p align="center">
  <img src="/images/frontend_food.png" alt="Adding a food">
</p>

<p align="center">
  <img src="/images/frontend_activity.png" alt="Adding an activity">
</p>

<p align="center">
  <img src="/images/frontend_summary.png" alt="Summary">
</p>
