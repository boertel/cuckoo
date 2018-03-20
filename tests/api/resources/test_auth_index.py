def test_user_details(client, default_login):
    response = client.get('/api/v1/users/me')
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == default_login.email
