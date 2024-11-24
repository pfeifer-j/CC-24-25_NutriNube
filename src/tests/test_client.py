# tests/test_client.py
def test_home_route_requires_login(client):
    """Test that accessing the home route redirects to the login page if not logged in."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_login(client):
    """Test successful login with valid credentials."""
    client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert b'Successful login' in response.data


def test_failed_login(client):
    """Test failed login with invalid credentials."""
    response = client.post('/login', data={
        'username': 'wronguser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b'Invalid username or password' in response.data


def test_register(client):
    """Test user registration with valid data."""
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpassword'
    })
    assert response.status_code == 201
    assert b'User registered successfully!' in response.data


def test_double_register(client, add_user):
    """Test attempting to register an already existing user."""
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'newpassword'
    })
    assert response.status_code == 400
    assert b'User already exists!' in response.data


def test_logout(client, login):
    """Test successful logout."""
    response = client.post('/logout')
    assert response.status_code == 200
    assert b'Logged out successfully' in response.data


def test_dashboard_requires_login(client):
    """Test that accessing the dashboard redirects to the login page if not logged in."""
    response = client.get('/dashboard')
    assert response.status_code == 302


def test_login_missing_fields(client):
    """Test login with missing username."""
    response = client.post('/login', data={
        'username': '',
        'password': 'somepassword'
    })
    assert response.status_code == 400
    assert b'Username and password are required' in response.data


def test_register_missing_fields(client):
    """Test registration with missing username."""
    response = client.post('/register', data={
        'username': '',
        'password': 'somepassword'
    })
    assert response.status_code == 400
    assert b'Username and password must be provided.' in response.data


def test_logout_protected_access(client, login):
    """Test that logged out users cannot access protected routes."""
    response = client.get('/dashboard')
    assert response.status_code == 200
    
    client.post('/logout')
    response = client.get('/dashboard')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']