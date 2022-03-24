import os
import shutil
from unittest import TestCase

from opylib.files_folders import mkdir
from opylib.log import log_exception, setup_log
from tests.config_tests import TestsConfig


class Test(TestCase):
    def test_setup_log_and_change_dir(self):
        # Test to confirm that error file is created in the correct place even
        # if the working directory gets changed during execution

        if not TestsConfig.get_instance().no_skip:
            return

        # Setup Logging
        log_fn = 'testLog/logfile.log'
        setup_log(log_fn)

        # Ensure log file created
        self.assertTrue(os.path.exists(log_fn))

        # Get absolute path and ensure the folder part is valid
        log_fn = os.path.abspath(log_fn)
        log_dir = os.path.dirname(log_fn)
        self.assertTrue(os.path.exists(log_dir))

        # Create new directory and change it to be the current working dir
        org_dir = os.getcwd()
        new_dir = os.path.join(log_dir, 'other_dir/')
        mkdir(new_dir)
        os.chdir(new_dir)

        # Register an exception to create the error logger
        log_exception(Exception('NOT AN ERROR PART OF TESTS'))

        # Ensure the log file was still created in the correct place
        self.assertTrue(os.path.exists(os.path.join(log_dir, 'ERRORS.log')))

        # Remove directory used for testing
        os.chdir(org_dir)  # Restore original directory before deleting
        shutil.rmtree(log_dir)
