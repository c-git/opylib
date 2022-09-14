from time import sleep
from unittest import TestCase

from opylib.db_cache import DBCache
from tests.config_tests import TestsConfig


class Test(TestCase):

    def helper_purge(self, *, do_purge=False, do_delay=False, num_changes=2,
                     delay=3):
        """
        Exactly one of `do_purge` or `do_delay` must be set to true

        :param do_purge: If True uses purge for testing
        :param do_delay: If True uses purge for testing
        :param num_changes: How many times the variables is changed and tested
        :param delay: The amount of delay set on the cache
        """
        # Ensure exactly on of the options is set
        assert do_purge != do_delay

        # Setup
        backing = {}
        test_key = 'TestKey'
        test_value = 1
        cache = DBCache(backing, save_cache_delay=delay)
        self.assertNotIn(test_key, backing)
        self.assertNotIn(test_key, cache)

        def purge_or_delay():
            if do_purge:
                assert not do_delay
                cache.purge()
            else:
                assert do_delay
                sleep(delay)

        # Clear possible allowed initial write
        cache['random'] = 'a random value'

        # Insert test key and value and ensure not in backing
        cache[test_key] = test_value
        self.assertNotIn(test_key, backing)
        self.assertIn(test_key, cache)

        # Purge and confirm in backing
        purge_or_delay()
        self.assertIn(test_key, backing)
        self.assertIn(test_key, cache)

        # Change value and test purge again
        for _ in range(num_changes):
            test_value += 1
            cache[test_key] = test_value
            self.assertEqual(cache[test_key], test_value)
            self.assertNotEqual(backing[test_key], test_value)

            # Purge and ensure updated
            purge_or_delay()
            self.assertEqual(cache[test_key], test_value)
            self.assertEqual(backing[test_key], test_value)

    def test_purge(self):
        self.helper_purge(do_purge=True)

    def test_auto_purge(self):
        if TestsConfig.get_instance().no_skip:
            self.helper_purge(do_delay=True)
