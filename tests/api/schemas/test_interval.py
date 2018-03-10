from cuckoo.api.schemas import IntervalSchema


def test_interval_schema_dump():
    # to client/frontend
    obj = {
        '__type__': 'interval',
        'every': 60,    # seconds
    }
    schema = IntervalSchema()
    response = schema.dump(obj)
    assert response.errors == {}
    data = response.data
    assert data['type'] == 'interval'
    assert data['every'] == 60
    assert data['relative'] is False


def test_interval_schema_load():
    # from client/frontend
    data = {
        'type': 'interval',
        'every': 60,
    }
    schema = IntervalSchema()
    response = schema.load(data)
    assert response.errors == {}
    data = response.data
    assert data['__type__'] == 'interval'
    assert data['every'] == 60
    assert data['relative'] is False
