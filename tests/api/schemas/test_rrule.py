from datetime import datetime
from dateutil.rrule import DAILY

from cuckoo.api.schemas import RRuleSchema


def test_rrule_schema_dump():
    obj = {
        '__type__': 'rrule',
        'freq': DAILY,
        'interval': 30,
        # 'dtstart': datetime.utcnow(),
        'dtstart': 1523664000,  # TODO(boertel) should be a datetime obj here?
    }
    schema = RRuleSchema()
    response = schema.dump(obj)
    assert response.errors == {}
    data = response.data
    assert data['type'] == 'rrule'
    assert data['freq'] == 'DAILY'
    assert data['interval'] == 30
    assert isinstance(data['dtstart'], str)
    assert data['dtstart'] == '2018-04-14T00:00:00Z'


def test_rrule_schema_load():
    data = {
        'type': 'rrule',
        'freq': 'DAILY',
        'interval': 30,
        'dtstart': '2018-04-14T00:00:00',
    }
    schema = RRuleSchema()
    response = schema.load(data)
    assert response.errors == {}
    obj = response.data
    assert obj['__type__'] == 'rrule'
    assert obj['freq'] == DAILY
    assert isinstance(obj['dtstart'], int)
    assert obj['dtstart'] == 1523664000
