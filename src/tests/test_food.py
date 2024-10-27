# tests/test_food.py
def test_add_food(client, login):
    response = client.post('/api/food', json={
        'food': 'Apple',
        'calories': 95,
        'protein': 0.5,
        'fat': 0.3,
        'carbs': 25
    })
    assert response.status_code == 201
    assert b'Food added successfully!' in response.data

def test_delete_food(client, login):
    response = client.post('/api/food', json={
        'food': 'Apple',
        'calories': 95,
        'protein': 0.5,
        'fat': 0.3,
        'carbs': 25
    })
    food_id = response.get_json().get('id', 1)

    response = client.delete('/api/food', json={
        'food_id': food_id
    })
    assert response.status_code == 200
    assert b'Food deleted successfully!' in response.data