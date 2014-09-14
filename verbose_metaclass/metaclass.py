from datetime import datetime


class Calls(dict):
    pass

GLOBAL_CALLS = Calls()



class MetaVerbose(type):
    def __new__(mcs, name, bases, dict):
        def new_getattribute(self, attr):
            cls = object.__getattribute__(self, '__class__')
            key = '{}.{}'.format(cls, attr)

            if key not in GLOBAL_CALLS:
                GLOBAL_CALLS[key] = []

            GLOBAL_CALLS[key].append(datetime.utcnow())
            return super(self.__class__, self).__getattribute__(attr)

        dict['__getattribute__'] = new_getattribute
        return type.__new__(mcs, name, bases, dict)


class NewBase(object):
    __metaclass__ = MetaVerbose


def activate():
    import __builtin__
    __builtin__.object = NewBase


def get_calls():
    return GLOBAL_CALLS
