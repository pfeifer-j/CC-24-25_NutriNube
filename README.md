# :apple: NutriNube :banana:

## Cloud Computing: Fundamentos e Infraestructuras - Prácticas

This is the repository for the project of the Cloud Computing course.

## Project (Laboratory Practices)

## :pencil2: Milestone 1: Problem Description

The primary objective of this project is to develop a fitness tracker that enables users to monitor their physical activity and track their food consumption. The application will help users achieve their health and fitness goals by providing detailed insights into their daily caloric intake and macronutrient distribution (proteins, fats, and carbohydrates). 

Users will be able to:

- Log their daily food consumption, with options to input the name of the food item, calorie count, and macro breakdown.
- Track physical activities and calculate calories burned based on various exercises.
- Set personalized health and fitness goals, allowing the app to provide tailored recommendations and feedback.

Using the following link you can access the [Milestone 1 Documentation](/documentation/milestone1/milestone1.md) where the project logic is explained.


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

Milestone 3 centered on designing and implementing a microservice architecture using `flask`. This involved developing a RESTful API to efficiently manage user data, including food logs, fitness activities, and personal goals. Key enhancements included the integration of `marshmallow` for robust data validation and `fluent` for comprehensive logging. The microservice was containerized using Docker to separate containers for the application, logging, and the PostgreSQL database. In Addition, the tests have been refined. 

For detailed descriptions of the methods and configurations employed, refer to the [Milestone 3 Documentation](/documentation/milestone3/milestone3.md).