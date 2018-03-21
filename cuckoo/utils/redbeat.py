import json

from redbeat.decoder import RedBeatJSONDecoder, RedBeatJSONEncoder


def from_schedule_to_dict(schedule):
    return json.dumps(schedule, cls=RedBeatJSONEncoder)


def from_dict_to_schedule(data):
    str_data = data
    return json.loads(str_data, cls=RedBeatJSONDecoder)
