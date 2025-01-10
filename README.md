# :apple: NutriNube :banana:

## Cloud Computing: Fundamentos e Infraestructuras - Prácticas

This is the repository for the project of the Cloud Computing course.

## Project (Laboratory Practices)

## :pencil2: Milestone 1: Problem Description

The primary objective of this project was to develop a fitness tracker that enables users to monitor their physical activity and track their food consumption. The application will help users achieve their health and fitness goals by providing detailed insights into their daily caloric intake and macronutrient distribution (proteins, fats, and carbohydrates). 

Users will be able to:

- Log their daily food consumption, with options to input the name of the food item, calorie count, and macro breakdown.
- Track physical activities and calculate calories burned based on various exercises.
- Set personalized health and fitness goals, allowing the app to provide tailored recommendations and feedback.

Under [Milestone 1 Documentation](/documentation/milestone1/milestone1.md) the project logic is explained.


## :pencil2: Milestone 2: Continuous Integration and Deployment

Milestone 2 focused on integrating a continuous integration (CI) pipeline to enhance code quality and deployment efficiency. Here’s a summary of the implementations:

- Continuous Integration Setup: Utilized `tox` and `pytest` for testing automation.
- Configured GitHub Actions to automate testing and ensure that all pushed code is thoroughly tested using the setup defined in the CI workflow file. 
- Flask Application Deployment using Docker
- Database Integration via Docker Compose
- Adding backendcode and according tests
- Implemented a basic frontend in HTML, CSS and JS

For detailed descriptions of the methods and configurations employed, refer to the [Milestone 2 Documentation](/documentation/milestone2/milestone2.md).


## :pencil2: Milestone 3: Microservice Design

Milestone 3 centered on designing and implementing a microservice architecture using `Flask`. This involved developing a RESTful API to efficiently manage user data, including food logs, fitness activities, and personal goals. Key enhancements included the integration of `marshmallow` for robust data validation and `fluent` for comprehensive logging. The microservice was containerized using Docker to separate containers for the application, logging, and the PostgreSQL database. In Addition, the tests have been refined. Here’s a summary of the implementations:
- Developed a RESTful API using `Flask` to manage routes. 
- Integrated `marshmallow` for data validation and serialization.
- Implemented `fluent` for logging application activity.
- Containerized the application with Docker, including separate containers for the app, logging, and PostgreSQL database.
- Refined and expanded test coverage to ensure API reliability.

For detailed descriptions of the methods and configurations employed, refer to the [Milestone 3 Documentation](/documentation/milestone3/milestone3.md).


## :pencil2: Milestone 4: Containerization and Cluster Deployment

Milestone 4 focused on further containerizing the application, deploying it as a cluster, and automating its build and deployment processes. The key aspects of this milestone include:

- The `Dockerfile` was improved for the application container, including all dependencies required for the application to run the container image.
- The `docker-compose.yml` file was alterd to manage a cluster of containers, including the application container, the PostgreSQL database container, and the Fluentd container for logging.
- The repository is configured to automatically build and deploy the container whenever updates are pushed to GitHub. This process is managed through GitHub Actions.
- Test were added to ensure that the Docker Compose cluster is correctly built and all containers are running in a healthy state. This test is automated and runs as part of the GitHub Actions pipeline.

For detailed descriptions of the methods and configurations employed, refer to the [Milestone 4 Documentation](/documentation/milestone4/milestone4.md).


## :pencil2: Milestone 5: Deployment on a PaaS

Milestone 5 focused on deploying the NutriNube application to the cloud using Render.com, a PaaS chosen for its easy GitHub integration and free service. Key aspects of milestone include:

- Automatic deployment upon each commit via Render's automatic deployment.
- Minor configuration adjustments to fit deployment requirements.
- Ensuring application functionality in the cloud.
- Performance testing remains a future task.

For detailed explanations, see the [Milestone 5 Documentation](/documentation/milestone5/milestone5.md)..
