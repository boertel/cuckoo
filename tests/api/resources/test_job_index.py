from datetime import datetime, timezone
from cuckoo.models import Job


def test_create_valid_job_with_interval(client, default_login, default_application):
    url = '/api/v1/apps/{}/jobs'.format(default_application.id)
    name = 'import/export'
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


def test_create_valid_job_with_crontab(client, default_login, default_application):
    url = '/api/v1/apps/{}/jobs'.format(default_application.id)
    name = 'import/export'
    response = client.post(url, json={
        'name': name,
        'url': 'http://localhost/meeting',
        'schedule': {
            'type': 'crontab',
            'hour': '1',
        }
    })
    assert response.status_code == 200
    data = response.json()
    assert data['id']
    assert data['name'] == name

    job = Job.query.filter(Job.id == data['id']).first()
    assert job
    assert job.name == name
    assert job.schedule.hour == {1}


def test_create_valid_job_with_rrule_with_datetime(client, default_login, default_application):
    url = '/api/v1/apps/{}/jobs'.format(default_application.id)
    name = 'import/export'
    response = client.post(url, json={
        'name': name,
        'url': 'http://localhost/meeting',
        'schedule': {
            'type': 'rrule',
            'freq': 'DAILY',
            'interval': 30,
            'dtstart': '2018-04-14T00:00:00',
        }
    })
    assert response.status_code == 200
    data = response.json()
    assert data['id']
    assert data['name'] == name

    job = Job.query.filter(Job.id == data['id']).first()
    assert job
    assert job.name == name
    assert type(job.schedule.dtstart) == datetime
    assert job.schedule.dtstart == datetime(2018, 4, 14, 0, 0, tzinfo=timezone.utc)
