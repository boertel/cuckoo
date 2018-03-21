from cuckoo.models import Job


def test_create_valid_job_with_interval(client, default_login, default_application):
    url = '/api/v1/apps/{}/jobs'.format(default_application.id)
    name = 'architecture meeting'
    response = client.post(url, json={
        'name': name,
        'url': 'http://localhost/meeting',
        'schedule': {
            'type': 'interval',
            'every': 60,
        }
    })
    assert response.status_code == 200
    data = response.json()
    assert data['id']
    assert data['name'] == name

    job = Job.query.filter(Job.id == data['id']).first()
    assert job
    assert job.name == name
    assert job.schedule.seconds == 60
    assert job.schedule.relative is False
