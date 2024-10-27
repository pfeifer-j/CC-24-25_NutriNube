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