# tests/conftest.py
import pytest
from app import create_app, db
@pytest.fixture
def app():
    """Set up the Flask application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Provide a test client for making requests."""
    return app.test_client()

@pytest.fixture
def add_user(client):
    """Create a new user for testing purposes."""
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201, "User should be registered successfully."

@pytest.fixture
def login(client, add_user):
    """Log in a user for tests requiring authentication."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200, "User should log in successfully."