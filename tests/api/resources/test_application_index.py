from cuckoo.models import Application


def test_create_application(client, default_login):
    response = client.post('/api/v1/apps', json={
        'name': 'Test App',
    })
    assert response.status_code == 200
    data = response.json()
    assert data['id']
    assert data['name'] == 'Test App'

    app = Application.query.filter(Application.id == data['id']).first()
    assert app
    assert app.name == data['name']
