from datetime import datetime
from dateutil.rrule import DAILY
from celery.schedules import crontab
from redbeat.schedules import rrule

from cuckoo.api.schemas import RRuleSchema, CrontabSchema
from cuckoo.api.schemas.fields import ScheduleField


class ObjectWithSchedule(object):
    def __init__(self, schedule):
        self.schedule = schedule


def test_schedule_field_rrule_serialize():
    # to client/frontend
    # TODO(boertel) redbeat strip microsecond
    now = datetime.utcnow().replace(microsecond=0)
    schedule = rrule(DAILY, interval=30, dtstart=now)

    obj = ObjectWithSchedule(schedule=schedule)
    field = ScheduleField({'rrule': RRuleSchema})
    data = field.serialize('schedule', obj)
    assert data['type'] == 'rrule'
    assert data['freq'] == 'DAILY'
    assert data['interval'] == 30
    assert data['dtstart'] == now


def test_schedule_field_rrule_deserialize():
    # from client/frontend
    data = {
        'type': 'rrule',
        'freq': 'DAILY',
        'interval': 30,
        'dtstart': 1451480362,
        'until': None,
    }

    field = ScheduleField({'rrule': RRuleSchema})
    data = field.deserialize(data)
    assert isinstance(data, rrule)
    assert data.freq == DAILY
    assert data.interval == 30
    assert isinstance(data.dtstart, datetime)
    assert data.dtstart.year == 2015


def test_schedule_field_crontab_serialize():
    # to client/frontend
    schedule = crontab(minute='4', hour='*')
    obj = ObjectWithSchedule(schedule=schedule)
    field = ScheduleField({'crontab': CrontabSchema})
    data = field.serialize('schedule', obj)
    assert data['type'] == 'crontab'
    assert data['minute'] == '4'
    assert data['hour'] == '*'
