from datetime import datetime
try:
    import __builtin__
    builtin_module = __builtin__
except ImportError:
    import builtins
    builtin_module = builtins

original_object = builtin_module.object


class Calls(dict):
    def order_by_time(self):
        all_events = []
        for method, calls in self.items():
            all_events.extend((method, c) for c in calls)

        return sorted(all_events, key=lambda x: x[1])

GLOBAL_CALLS = Calls()


class MetaVerbose(type):
    def __new__(mcs, name, bases, dict):
        return type.__new__(mcs, name, bases, dict)


class NewBase(original_object):
    __metaclass__ = MetaVerbose

    def __getattribute__(self, attr):
        cls = original_object.__getattribute__(self, '__class__')
        key = '{}.{}'.format(cls.__name__, attr)

        if key not in GLOBAL_CALLS:
            GLOBAL_CALLS[key] = []

        GLOBAL_CALLS[key].append(datetime.utcnow())
        return original_object.__getattribute__(self, attr)


def activate():
    builtin_module.object = NewBase


def init_calls():
    global GLOBAL_CALLS
    GLOBAL_CALLS = Calls()


def get_calls():
    return GLOBAL_CALLS
