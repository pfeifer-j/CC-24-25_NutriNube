# tests/test_client.py
def test_home_route_requires_login(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_login(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    print("Response Data:", response.data)
    assert response.status_code == 200
    assert b'Successful login' in response.data

def test_failed_login(client):
    response = client.post('/login', data={
        'username': 'wronguser',
        'password': 'wrongpassword'
    })
    print(response.data)
    assert response.status_code == 401
    assert b'Invalid username or password' in response.data

def test_register(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpassword'
    })
    assert response.status_code == 201
    assert b'User registered successfully!' in response.data

def test_double_register(client, add_user):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'newpassword'
    })
    assert response.status_code == 400
    assert b'User already exists!' in response.data

def test_logout(client, login):
    response = client.post('/logout')
    assert response.status_code == 200
    assert b'Logged out successfully' in response.data

def test_dashboard_requires_login(client):
    response = client.get('/dashboard')
    assert response.status_code == 302 
