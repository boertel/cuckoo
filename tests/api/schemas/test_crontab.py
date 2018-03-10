from cuckoo.api.schemas import CrontabSchema


def test_crontab_schema_dump():
    # to client/frontend
    obj = {
        '__type__': 'crontab',
        'minute': 4,
        'hour': '*',
    }
    schema = CrontabSchema()
    response = schema.dump(obj)
    assert response.errors == {}
    data = response.data
    assert data['type'] == 'crontab'
    assert data['minute'] == '4'
    assert data['hour'] == '*'


def test_crontab_schema_load():
    # from client/frontend
    data = {
        'type': 'crontab',
        'minute': '4',
        'hour': '*',
    }
    schema = CrontabSchema()
    response = schema.load(data)
    assert response.errors == {}
    data = response.data
    assert data['__type__'] == 'crontab'
    assert data['hour'] == '*'
