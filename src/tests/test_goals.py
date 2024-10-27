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