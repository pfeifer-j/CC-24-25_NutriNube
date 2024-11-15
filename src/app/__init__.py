# app/__init__.py
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from fluent import asynchandler as fluentasynchandler
from fluent import event
import logging
import os
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.secret_key = os.urandom(24)
    
    # Setup Fluentd Logging
    handler = fluentasynchandler.FluentHandler('app', host='localhost', port=24224)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    # Add a simple formatter
    format_string = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    
    app.logger.info({
        'event': 'fluentd_setup',
        'message': 'Fluentd logger setup successfully!'
    })
    
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://pfeiferj:NutriNube@db:5432/flaskdb')
    
    db.init_app(app)

    # Import models
    from .models.models import User, FoodLog, FitnessLog, UserSchema, FoodLogSchema, FitnessLogSchema
    
    # Create database tables
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
        app.logger.debug({ 
            'event': 'request_received',
            'method': request.method,
            'url': request.url,
            'headers': dict(request.headers)
        })

    return app