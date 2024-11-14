# tests/test_fitness.py
def test_add_fitness(client, login):
    response = client.post('/api/fitness', json={
        'date': '2023-10-15',  # Example date
        'exercise': 'Running',
        'kcal_burned': 300
    })
    assert response.status_code == 201

def test_delete_fitness(client, login):
    response = client.post('/api/fitness', json={
        'date': '2023-10-15',  # Example date
        'exercise': 'Running',
        'kcal_burned': 300
    })
    assert response.status_code == 201
    fitness_id = response.get_json().get('id')
    assert fitness_id is not None

    response = client.delete('/api/fitness', json={'fitness_id': fitness_id})
    assert response.status_code == 200