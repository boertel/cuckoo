from celery.beat import Scheduler, ScheduleEntry


class CuckooScheduleEntry(ScheduleEntry):
    _meta = None

    def __init__(self):
        pass

    @staticmethod
    def load_definition(key, app=None, definition=None):
        pass

    @staticmethod
    def decode_definition(definition):
        pass

    @staticmethod
    def load_meta(key, app=None):
        pass

    @classmethod
    def from_key(cls, key, app=None):
        pass

    @property
    def due_at(self):
        pass

    @property
    def key(self):
        pass

    @property
    def score(self):
        pass

    @property
    def rank(self):
        pass

    def save(self):
        pass

    def delete(self):
        pass

    def _next_instance(self, last_run_at=None, only_update_last_run_at=False):
        pass

    def reschedule(self, last_run_at=None):
        pass

    def is_due(self):
        pass


class CuckooScheduler(Scheduler):
    Entry = CuckooScheduleEntry

    def __init__(self):
        pass

    def setup_schedule(self):
        pass

    def update_from_dict(self, dict_):
        pass

    def reserve(self, entry):
        pass

    @property
    def schedule(self):
        pass

    def maybe_due(self, entry, **kwargs):
        pass

    def tick(self, min=min, **kwargs):
        pass

    def close(self):
        pass

    @property
    def info(self):
        pass

    @cached_property
    def _maybe_due_kwargs(self):
        pass
