import unittest

from verbose_metaclass.metaclass import activate, get_calls


def setup_module():
    activate()


class TestVerboseMetaclass(unittest.TestCase):
    def test_calling_function_adds_a_new_call(self):
        class Sample(object):
            def check_call(self, arg):
                print(arg)

        Sample().check_call(arg='Hello')
        calls = get_calls()
        self.assertIn('Sample.check_call', calls)
