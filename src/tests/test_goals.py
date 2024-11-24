# tests/test_goals.py
def test_update_goals(client, login):
    response = client.post('/api/update-goal', json={
        'calorie_goal': 2000,
        'protein_goal': 150,
        'fat_goal': 70,
        'carbs_goal': 300
    })
    assert response.status_code == 200
    assert b'Goals updated successfully!' in response.data

def test_daily_summary(client, login):
    response = client.get('/daily-summary?date=2023-10-01')
    assert response.status_code == 200
    summary = response.get_json()
    assert 'calories_goal' in summary
    assert 'total_calories_consumed' in summary

def test_update_goals_without_login(client):
    response = client.post('/api/update-goal', json={
        'calorie_goal': 2000,
        'protein_goal': 150,
        'fat_goal': 70,
        'carbs_goal': 300
    })
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_update_goals_invalid_user(client, login):
    client.post('/logout')
    with client.session_transaction() as session:
        session['username'] = 'nonexistentuser'

    response = client.post('/api/update-goal', json={
        'calorie_goal': 1800,
        'protein_goal': 100,
        'fat_goal': 60,
        'carbs_goal': 250
    })
    assert response.status_code == 404
    assert b'User not found' in response.data

def test_update_partial_goals(client, login):
    response = client.post('/api/update-goal', json={
        'protein_goal': 160
    })
    assert response.status_code == 400

def test_update_goals_malformed_json(client, login):
    response = client.post('/api/update-goal', data="Invalid JSON",
                           content_type='application/json')
    assert response.status_code == 400

def test_update_goals_invalid_values(client, login):
    response = client.post('/api/update-goal', json={
        'calorie_goal': -1000,
        'protein_goal': 150,
        'fat_goal': 70,
        'carbs_goal': 300
    })
    assert response.status_code == 400