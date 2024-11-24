# tests/test_food.py
def test_add_food_success(client, login):
    """Test adding a valid food log."""
    response = client.post('/api/food', json={
        'date': '2023-10-15',
        'food': 'Banana',
        'calories': 105,
        'protein': 1.3,
        'fat': 0.3,
        'carbs': 27
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Food added successfully!'
    assert 'id' in data


def test_add_food_missing_fields(client, login):
    """Test adding food with missing required fields."""
    response = client.post('/api/food', json={
        'food': 'Banana',
        'calories': 105
    })
    assert response.status_code == 400
    assert b'date' in response.data

    
def test_add_food_invalid_data(client, login):
    """Test adding food with invalid data types."""
    response = client.post('/api/food', json={
        'date': '2023-10-15',
        'food': 'Banana',
        'calories': 'not-a-number',
        'protein': 1.3,
        'fat': 0.3,
        'carbs': 27
    })
    assert response.status_code == 400
    assert b'calories' in response.data


def test_add_food_unauthenticated(client):
    """Test adding food without being logged in should redirect to the login page."""
    response = client.post('/api/food', json={
        'date': '2023-10-15',
        'food': 'Banana',
        'calories': 105,
        'protein': 1.3,
        'fat': 0.3,
        'carbs': 27
    })
    assert response.status_code == 302


def test_delete_food_success(client, login):
    """Test deleting an existing food log."""
    response = client.post('/api/food', json={
        'date': '2023-10-15',
        'food': 'Apple',
        'calories': 95,
        'protein': 0.5,
        'fat': 0.3,
        'carbs': 25
    })
    assert response.status_code == 201
    food_id = response.get_json()['id']

    response = client.delete('/api/food', json={'food_id': food_id})
    assert response.status_code == 200
    assert b'Food deleted successfully!' in response.data


def test_delete_food_not_found(client, login):
    """Test deleting a food log that does not exist."""
    response = client.delete('/api/food', json={'food_id': 99999})
    assert response.status_code == 404
    assert b'Food item not found or unauthorized' in response.data


def test_delete_food_unauthorized(client, login):
    """Test deleting another user's food log."""
    response = client.post('/api/food', json={
        'date': '2023-10-15',
        'food': 'Grapes',
        'calories': 62,
        'protein': 0.6,
        'fat': 0.2,
        'carbs': 16
    })
    assert response.status_code == 201
    food_id = response.get_json()['id']

    client.get('/logout')
    client.post('/register', data={
        'username': 'otheruser',
        'password': 'password'
    })
    client.post('/login', data={
        'username': 'otheruser',
        'password': 'password'
    })

    response = client.delete('/api/food', json={'food_id': food_id})
    assert response.status_code == 404