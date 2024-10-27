# tests/test_fitness.py
def test_add_fitness(client, login):
    response = client.post('/api/fitness', json={
        'exercise': 'Running',
        'kcal_burned': 300
    })
    assert response.status_code == 201
    assert b'Exercise added successfully!' in response.data

def test_delete_fitness(client, login):
    response = client.post('/api/fitness', json={
        'exercise': 'Running',
        'kcal_burned': 300
    })
    fitness_id = response.get_json().get('id', 1) 

    response = client.delete('/api/fitness', json={
        'fitness_id': fitness_id
    })
    assert response.status_code == 200
    assert b'Exercise deleted successfully!' in response.data