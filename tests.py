import unittest

from verbose_metaclass.metaclass import activate, get_calls, init_calls


def setup_module():
    activate()


class TestVerboseMetaclass(unittest.TestCase):
    def setUp(self):
        class Sample(object):
            def check_call(self, arg=None):
                print(arg)

        self.sample_cls = Sample
        init_calls()

    def test_calling_function_adds_a_new_call(self):
        self.sample_cls().check_call(arg='Hello')
        calls = get_calls()
        self.assertIn('Sample.check_call', calls)

    def test_sort_by_time(self):
        obj = self.sample_cls()
        obj.check_call(arg=1)
        obj.check_call()
        self.assertEqual(len(get_calls().order_by_time()), 2)
