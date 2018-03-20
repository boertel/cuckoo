from factory import LazyFunction

from cuckoo.db.types import GUID


class GUIDFactory(LazyFunction):
    def __init__(self, *args, **kwargs):
        LazyFunction.__init__(self, GUID.default_value, *args, **kwargs)
