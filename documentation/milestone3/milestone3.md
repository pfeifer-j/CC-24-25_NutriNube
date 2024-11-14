# :pushpin: Milestone 3: Microservice Design :pushpin:

## :book: NutriNube :book:  
Version 0.2.0

---

## Description of the Milestone

In this milestone, a microservice using `Flask` has been designed and implemented based on the functionality developed in the previous milestone. An API following REST conventions has been created to manage food logs, fitness logs, and user goals while integrating logging and validation.

---

## 1. API Framework

1.1 Why Choose `Flask` as a Framework
`Flask` was chosen for building the microservice due to its simplicity, flexibility, and active community. Key advantages include:

- Ideal for microservices that require rapid development without overhead.
- Lightweight and modular design.
- Easily integrates with libraries like `Marshmallow` for data validation and `Fluent` for logging.

Key `Flask` Features Utilized:
- Route handling for defining API endpoints.
- Built-in support for unit testing.
- Easy-to-extend architecture.

1.2 API Design and Routes

The project is organized in a modular way to maintain clean code:

plaintext
app/
│   ├── __init__.py       # Initializes the application and extensions
│   ├── models.py         # Defines data models
│   ├── routes.py         # Defines API routes
│   └── ...


The following routes have been implemented in routes.py:

1. `GET /goals`: Retrieves all user goals.
2. `POST /api/food`: Adds a new food log entry.
3. `POST /api/fitness`: Adds a new fitness log entry.
4. `POST /login`: Authenticates a user.
5. `POST /register`: Registers a new user and checks for duplicate usernames.

Example Implementation for the `/api/food` Route:
python
@app.route('/api/food', methods=['POST'])
@login_required
def add_food():
    # Logic for adding food


A detailed description of the routes can be found in api_guide.md.

## 2. Implementation of Schemas with `Marshmallow`

`Marshmallow` is utilized for serialization and validation of input data:

- Ensures incoming data meets specified criteria before processing.
- Automatically generates error messages for incorrect data formats.

Example Model Schema:
python
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


When adding a food log, input data is validated using:
python
schema = UserSchema()
data = schema.load(request.form, session=db.session, partial=True)


Handling Validation Errors:
python
except ValidationError as err:
    current_app.logger.warning({
        'event': 'registration_attempt',
        'message': 'Invalid data provided',
        'ip': request.remote_addr,
        'errors': err.messages
    })
    return jsonify(err.messages), 400


## 3. Logging Implementation with `Fluent`

`Fluent` is utilized for logging application activity, both to a file and standard output.

Fluent Configuration:

To use `Fluent`, it has to be configured correctly and added to Docker. Under src/app/fluentd/conf/fluent.conf:

plaintext
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


Docker Compose for Logging:

The `docker-compose.yml` has been adjusted to run `Fluent` in a separate container while defining the network structure:

yaml
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


Additionally, the `requirements.txt` was updated:
plaintext
Flask
Flask-Cors
Flask-SQLAlchemy
flask-marshmallow
psycopg2-binary
fluent-logger
marshmallow
marshmallow-sqlalchemy


## 4. Testing and Validation

Part of this milestone is to update the tests, but in my case, I already implemented testing for Milestone 2.

My tests can be found here.

## 5. Future Implementations

This milestone successfully established a functioning microservice using `Flask`, `Marshmallow` for data validation, and `Fluent` for logging. The project is implemented in a containerized fashion using three different containers for the application logic, logging, and database. Future plans include enhancing the already working frontend, which was initially implemented as a prototype in Milestone 2 Documentation.

## 6. Preview of the Frontend

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