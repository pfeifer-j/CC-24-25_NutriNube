from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from fluent.asynchandler import FluentHandler
import logging
import os
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.secret_key = os.urandom(24)
    
    # Set up logging
    setup_logging(app)

    # Log a message indicating that Fluentd logger setup was successful
    app.logger.info({
        'event': 'fluentd_setup',
        'message': 'Fluentd logger setup successfully!'
    })
    
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    db.init_app(app)

    # Import models
    from .models.models import User, FoodLog, FitnessLog, UserSchema, FoodLogSchema, FitnessLogSchema
    
    # Create database tables within the app context
    with app.app_context():
        db.create_all()

    # Import and initialize route modules
    from .routes.routes_auth import init_auth_routes
    from .routes.routes_navigation import init_navigation_routes
    from .routes.routes_food import init_food_routes
    from .routes.routes_fitness import init_fitness_routes
    from .routes.routes_summary import init_summary_routes
    from .routes.routes_goals import init_goals_routes
    
    # Initialize routes
    init_auth_routes(app)
    init_navigation_routes(app)
    init_food_routes(app)
    init_fitness_routes(app)
    init_summary_routes(app)
    init_goals_routes(app)

    @app.before_request
    def log_request_info():
        # Log incoming requests as structured data
        app.logger.debug({
            'event': 'request_received',
            'method': request.method,
            'url': request.url,
            'headers': dict(request.headers)
        })

    return app

def setup_logging(app):
    class StructuringFilter(logging.Filter):
        def filter(self, record):
            # Ensure every log message is a dictionary
            if not isinstance(record.msg, dict):
                record.msg = {'message': str(record.msg)}
            return True

    # Set up Fluentd logging handler
    try:
        fluent_handler = FluentHandler('app', host=os.environ.get('FLUENTD_HOST', 'localhost'), port=24224)
        fluent_handler.setFormatter(logging.Formatter())
        fluent_handler.addFilter(StructuringFilter())
        app.logger.addHandler(fluent_handler)
        app.logger.info({
            'event': 'fluentd_setup',
            'message': 'Fluentd logger setup successfully!'
        })
    except Exception as e:
        app.logger.warning({
            'event': 'fluentd_setup',
            'message': f"Could not connect to Fluentd: {e}"
        })

    # Set up a console handler for local debugging and fallback logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    console_handler.addFilter(StructuringFilter())
    app.logger.addHandler(console_handler)

    # Set the log level for the app
    app.logger.setLevel(logging.INFO)
