# :pushpin: Milestone 3: Microservice Design :pushpin:

## :book: NutriNube :book:  
Version 2.0.0

---

## Description of the Milestone

In this milestone, a microservice using `Flask` has been designed and implemented based on the functionality developed in [the previous milestone](/documentation/milestone2/milestone2.md). An API following REST conventions has been created to manage food logs, fitness logs, and user goals while integrating logging and validation. Furthermore, with more complex routes the tests have been adjusted accordingly.

---

## 1. API Framework

1.1 Why Choose `Flask` as a Framework?

`Flask` is a nice choice for building microservices, offering the following advantages:
- `Flask` provides a minimalist, lightweight core, perfect for smaller projects like this one.
- It has a strong community with good documentation.
- `Flask` easily integrates with data validation libraries like `Marshmallow` and logging tools like `Fluent`.

Key `Flask` Features Utilized:
- Route Handling: Efficiently manage API endpoints with built-in routing capabilities.
- Unit Testing Support: Designed with testing in mind, providing easy setup for unit tests to ensure robust application behavior.
- Extensible Architecture: Allows for straightforward integration of third-party extensions.

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

The following routes are the most important ones that have been implemented under [/src/app/routes](/src/app/routes):
#### For routing:
1. `/` - Home route: Displays the dashboard.
2. `/register` - Registration route: Registers a new user.
3. `/login` - Login route: Used for user authentication.
4. `/logout` - Logout route: Logs out the current user.
5. `/goals` - Goals route: Manages user goals.
6. `/foods` - Food route: Manages food log entries.
7. `/activities` - Activities route: Displays the activities page.
8. `/summary` - Summary route: Displays summary page.

#### For managing data:
9. `/api/update-goal` - API route: Updates user goals.
10. `/api/food` - API route: Manages food log entries.
11. `/api/fitness` - API route: Manages fitness log entries.

Example Implementation for the `/api/food` Route:
```python
@app.route('/api/food', methods=['POST'])
@login_required
def add_food():
    # Logic for adding food
```

A detailed description of all the routes can be found in [the api guide](/documentation/milestone3/api_guide.md).

## 2. Implementation of Schemas with `marshmallow`
2.1 Why Choose `marshmallow`?

`Marshmallow` is a good choice for handling serialization and validation since it offers a nice featureset:
  - Automatically validates incoming data against defined schemas.
  - Generates detailed error messages when data does not meet specified criteria.
  - Enables deserialization of incoming JSON data back into objects.
  - Provides seamless integration with `SQLAlchemy` models through extensions.
  - Supported by an active community with comprehensive documentation.

2.2 How to use `marshmallow`

To use `marshmallow` we need to implement schemas.

Example Model Schema:
```python
# FitnessLog Schema
class FitnessLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FitnessLog
        include_fk = True
        load_instance = True
    ...
    @validates('calories')
    def validate_calories(self, value):
        if value is None or value < 0:
            raise ValidationError('Calories must not be negative.')
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
3.1 Why Choose `fluent`?

`Fluent` is a robust choice for logging application activity due to the following features:
- Logs can be directed to various destinations, including files, standard output, and external logging systems like `Docker`.
- Offers a consistent interface for collecting logs across multiple services and environments.
- Allows configuration for collecting, filtering, and outputting logs.
- Supported by a strong community and resources.

3.2 How to use `fluent`

To use `Fluent`, it has to be configured and a Dockerfile has to be added.

Content of [fluent.conf](/src/app/fluentd/conf/fluent.conf):
```plaintext
# fluentd/conf/fluent.conf
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<match app.**>
  @type stdout
  <format>
    @type json
  </format>
  <store>
    @type file
    path /fluentd/log/app.log
    append true
  </store>
</match>

<match httpd.access>
  @type stdout
  <format>
    @type json
  </format>
  <store>
    @type file
    path /fluentd/log/httpd_access.log
    append true
  </store>
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

## 5. Optional Frontend
To launch the application with the frontend, use Docker by running the following commands:

```bash
cd .\src\app\
docker-compose up --build
docker-compose restart
```
Once the build process is complete, you can access the website at [localhost:5000](http://localhost:5000/).

Below is a preview of the frontend:

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
