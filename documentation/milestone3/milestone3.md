# :pushpin: Milestone 3: Microservice Design :pushpin:

## :book: NutriNube :book:  
Version 0.2.0

---

## Description of the Milestone

In this milestone, a microservice using `Flask` has been designed and implemented based on the functionality developed in [the previous milestone](/documentation/milestone2/milestone2.md). An API following REST conventions has been created to manage food logs, fitness logs, and user goals while integrating logging and validation. Furthermore, with more complex routes the tests have been adjusted accordingly.

---

## 1. API Framework

1.1 Why Choose `Flask` as a Framework

`Flask` was chosen for building the microservice due to its simplicity, flexibility, and active community. Key advantages include:

- Ideal for microservices that require rapid development without overhead.
- Values simplicity and flexibility.
- Lightweight and modular design, perfect for smaller projects like this one. 
- Easily integrates with libraries like `Marshmallow` for data validation and `Fluent` for logging.

Key `Flask` Features Utilized:
- Route handling for defining API endpoints.
- Built-in support for unit testing.
- Easy-to-extend architecture.

1.2 API Design and Routes

The project is organized in a modular way to maintain clean code:

```plaintext
app/
  ├── __init__.py    # Initializes the application and extensions
  ├── app.py         # Starts the application
  ├── ...
  ├── models         # Defines data models
  ├── routes         # Defines API routes
  └── ...
```

The following routes have been implemented in [routes.py](/src/app/routes.py):
#### For routing:
1. `/` - Home route: Displays the dashboard.
2. `/register` - Registration route: Registers a new user.
3. `/login` - Login route: Used for user authentication.
4. `/logout` - Logout route: Logs out the current user.
5. `/dashboard` - Dashboard route: Displays the dashboard.
6. `/goals` - Goals route: Manages user goals.
7. `/foods` - Food route: Manages food log entries.
8. `/activities` - Activities route: Displays the activities page.
9. `/summary` - Summary route: Displays summary page.
10. `/daily-summary` - Daily summary route: Provides a summary data of daily food and fitness logs.

#### For managing data:
11. `/api/update-goal` - API route: Updates user goals.
12. `/api/food` - API route: Adds food log entries.
13. `/api/food` - API route: Deletes food log entries.
14. `/api/fitness` - API route: Adds fitness log entries.
15. `/api/fitness` - API route: Deletes fitness log entries.

Example Implementation for the `/api/food` Route:
```python
@app.route('/api/food', methods=['POST'])
@login_required
def add_food():
    # Logic for adding food
```

A detailed description of the routes can be found in [the api guide](/documentation/milestone3/api_guide.md).

## 2. Implementation of Schemas with `marshmallow`

`Marshmallow` is utilized for serialization and validation of input data. It ensures incoming data meets specified criteria before processing and automatically generates error messages for incorrect data formats.
To use `marshmallow` we need to implement schemas.

Example Model Schema:
```python
# FitnessLog Schema
class FitnessLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FitnessLog
        include_fk = True
        load_instance = True
```

When adding a fitness log, input data is validated using:
```python
# Load the incoming JSON data
incoming_data = request.get_json()

# Prepare data for the schema load
data = {
    'user_id': user.id,
    'date': incoming_data.get('date'),
    'exercise': incoming_data.get('exercise'),
    'kcal_burned': incoming_data.get('kcal_burned')
}

# Validate and deserialize the data
schema = FitnessLogSchema()
validated_data = schema.load(data, session=db.session) 
```

Handling Validation Errors:
```python
except ValidationError as err:
    current_app.logger.warning({
        'event': 'add_fitness_validation_failed',
        'errors': err.messages,
        'ip': request.remote_addr
    })
    return jsonify(err.messages), 400
```

## 3. Logging Implementation with `Fluent`

`Fluent` is utilized for logging application activity, both to a file and standard output.
To use `Fluent`, it has to be configured and a Dockerfile has to be added.

Content of [fluent.conf](/src/app/fluentd/conf/fluent.conf):
```plaintext
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<match *.*>
  @type file
  path /fluentd/log/app_nutri_nube.log 
  append true
</match>

<match *.*>
  @type stdout
</match>
```

Content of [fluent.conf](/src/app/fluentd/Dockerfile):
```yaml
# fluentd/Dockerfile
FROM fluent/fluentd:v1.12.0-debian-1.0

USER root
USER fluent

COPY conf/fluent.conf /fluentd/etc/
CMD ["fluentd", "-c", "/fluentd/etc/fluent.conf"]
```

The [docker-compose.yml](/src/app/docker-compose.yml) has been adjusted to run `Fluent` in a separate container while defining the network structure and its own volume:

```yaml
# docker-compose.yml
networks:
  nutri_nube_network:
    driver: bridge

services:
  nutri_nube:
    build: .
    container_name: nutri_nube_app
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://pfeiferj:NutriNube@db:5432/flaskdb
    command: flask run --host=0.0.0.0
    depends_on:
      - fluentd
      - db
    logging:
      driver: "fluentd"
      options:
        fluentd-address: "localhost:24224"
        tag: httpd.access
    networks:
      - nutri_nube_network

  db:
    image: postgres:13
    container_name: nutri_nube_db
    environment:
      POSTGRES_USER: pfeiferj
      POSTGRES_PASSWORD: NutriNube
      POSTGRES_DB: flaskdb
    volumes:
      - nutri_nube_db:/var/lib/postgresql/data
    networks:
      - nutri_nube_network

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

volumes:
  nutri_nube_db:
  nutri_nube_logs:
```

Additionally, the [requirements.txt](/src/app/requirements.txt) was updated:
```plaintext
Flask
Flask-Cors
Flask-SQLAlchemy
flask-marshmallow
psycopg2-binary
fluent-logger
marshmallow
marshmallow-sqlalchemy
```

## 4. Testing and Validation

Part of this milestone is to update the tests, but in my case, I already implemented testing in [milestone 2](/documentation/milestone2/milestone2.md).

My tests can be found under [/src/tests](/src/tests). I implemented test for:
- Registration and Logging
- Accessing pages without authentification
- Setting goals
- Adding and deleting food entries
- Adding and deleting fitness entries

## 5. Future Implementations

This milestone successfully established a functioning microservice using `Flask`, `Marshmallow` for data validation, and `Fluent` for logging. The project is implemented in a containerized fashion using three different containers for the application logic, logging, and database. Future plans include enhancing the already working frontend, which was initially implemented as a prototype in [milestone 2](/documentation/milestone2/milestone2.md).
.

## 6. Optional Frontend Design

1. Registration and Login:
   <p align="center">
     <img src="/images/frontend_login.png" alt="Registration and Login">
   </p>

2. Adding a Goal:
   <p align="center">
     <img src="/images/frontend_goal.png" alt="Adding a goal">
   </p>

3. Adding a Food:
   <p align="center">
     <img src="/images/frontend_food.png" alt="Adding a food">
   </p>

4. Adding an Activity:
   <p align="center">
     <img src="/images/frontend_activity.png" alt="Adding an activity">
   </p>

5. Reviewing the Summary:
   <p align="center">
     <img src="/images/frontend_summary.png" alt="Summary">
   </p>
