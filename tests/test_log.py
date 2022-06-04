import os
import shutil
from typing import Tuple
from unittest import TestCase

from opylib.files_folders import mkdir
from opylib.log import log_exception, setup_log
from tests.config_tests import TestsConfig


class Test(TestCase):
    def assert_exists(self, fn: str):
        self.assertTrue(os.path.exists(fn),
                        msg=f'"{os.path.abspath(fn)}" expected to exist')

    def assert_not_exists(self, fn: str):
        self.assertFalse(os.path.exists(fn),
                         msg=f'"{os.path.abspath(fn)}" should NOT exist')

    def test_setup_log_and_change_dir(self):
        # Test to confirm that error file is created in the correct place even
        # if the working directory gets changed during execution

        if not TestsConfig.get_instance().no_skip:
            return

        base_log_dir, log_fn, err_log_fn = self.start_logging(False)

        # Ensure log files are created
        self.assert_exists(log_fn)
        self.assert_exists(err_log_fn)

        # Get absolute path and ensure the folder part is valid
        log_fn = os.path.abspath(log_fn)
        log_dir = os.path.dirname(log_fn)
        self.assertTrue(os.path.exists(log_dir))
        err_log_fn = os.path.abspath(err_log_fn)
        err_log_dir = os.path.dirname(log_fn)
        self.assertTrue(os.path.exists(err_log_dir))

        # Create new directory and change it to be the current working dir
        org_dir = os.getcwd()
        new_dir = os.path.join(log_dir, 'other_dir/')
        mkdir(new_dir)
        os.chdir(new_dir)

        # Register an exception to create the error logger
        self.assertEqual(os.path.getsize(err_log_fn), 0)  # Ensure log empty
        log_exception(Exception('NOT AN ERROR PART OF TESTS'))
        self.assertNotEqual(os.path.getsize(err_log_fn), 0)  # Ensure log grew

        # Remove directory used for testing
        os.chdir(org_dir)  # Restore original directory before deleting
        shutil.rmtree(base_log_dir)
        self.assert_not_exists(base_log_dir)

    def start_logging(self, only_std_out: bool) -> Tuple[str, str, str]:
        base_log_test_dir = 'testLog/'
        log_fn = base_log_test_dir + 'logfile.log'
        err_log_fn = base_log_test_dir + 'eTestLog/ERRORS.log'

        # Ensure log files do not already exist
        self.assert_not_exists(log_fn)
        self.assert_not_exists(err_log_fn)

        setup_log(log_fn, only_std_out=only_std_out, error_filename=err_log_fn)
        return base_log_test_dir, log_fn, err_log_fn
