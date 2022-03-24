import logging
from unittest import TestCase

from opylib.log import log
from opylib.main_runner import main_runner
from tests.config_tests import TestsConfig


def test_main():
    log('Test Main Run')


def test_main_with_exception():
    log('Test Main Run with exception')
    raise Exception('MAIN EXCEPTION')


class Test(TestCase):
    def test_main_runner(self):
        with self.assertLogs():
            main_runner(test_main)
        if TestsConfig.get_instance().no_skip:
            with self.assertLogs(level=logging.ERROR):
                main_runner(test_main_with_exception)
