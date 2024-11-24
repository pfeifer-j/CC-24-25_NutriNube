# tests/test_fitness.py
def test_add_fitness_success(client, login):
    """Test adding a valid fitness log."""
    response = client.post('/api/fitness', json={
        'date': '2023-10-15',
        'exercise': 'Running',
        'kcal_burned': 300
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Exercise added successfully!'
    assert 'id' in data

def test_add_fitness_missing_fields(client, login):
    """Test adding fitness log with missing required fields."""
    response = client.post('/api/fitness', json={
        'exercise': 'Running'
    })
    assert response.status_code == 400
    assert b'date' in response.data
    assert b'kcal_burned' in response.data

def test_add_fitness_invalid_data(client, login):
    """Test adding fitness log with invalid data types."""
    response = client.post('/api/fitness', json={
        'date': '2023-10-15',
        'exercise': 'Running',
        'kcal_burned': 'not-a-number'
    })
    assert response.status_code == 400
    assert b'kcal_burned' in response.data

def test_add_fitness_unauthenticated(client):
    """Test adding fitness log without being logged in should redirect to login."""
    response = client.post('/api/fitness', json={
        'date': '2023-10-15',
        'exercise': 'Cycling',
        'kcal_burned': 200
    })
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_delete_fitness_success(client, login):
    """Test deleting an existing fitness log."""
    response = client.post('/api/fitness', json={
        'date': '2023-10-15',
        'exercise': 'Running',
        'kcal_burned': 300
    })
    assert response.status_code == 201
    fitness_id = response.get_json().get('id')
    assert fitness_id is not None

    response = client.delete('/api/fitness', json={'fitness_id': fitness_id})
    assert response.status_code == 200
    assert b'Exercise deleted successfully!' in response.data

def test_delete_fitness_not_found(client, login):
    """Test deleting a fitness log that does not exist."""
    response = client.delete('/api/fitness', json={'fitness_id': 99999})
    assert response.status_code == 404
    assert b'Exercise not found or unauthorized' in response.data

def test_delete_fitness_unauthorized(client, login):
    """Test deleting another user's fitness log."""
    response = client.post('/api/fitness', json={
        'date': '2023-10-15',
        'exercise': 'Swimming',
        'kcal_burned': 250
    })
    assert response.status_code == 201
    fitness_id = response.get_json().get('id')
    assert fitness_id is not None
    
    client.get('/logout')
    client.post('/register', data={
        'username': 'otheruser',
        'password': 'password'
    })
    client.post('/login', data={
        'username': 'otheruser',
        'password': 'password'
    })

    response = client.delete('/api/fitness', json={'fitness_id': fitness_id})
    assert response.status_code == 404