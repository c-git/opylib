import atexit
import logging
import os.path
import sys
from datetime import datetime

from opylib.files_folders import mkdir

_logger = logging.getLogger()

# Store directory where log was created.
# Needs to be converted to absolute path in setup in case working directory
# changes during execution. Used later for location to create file for errors
_log_dir: str = 'log/'


def log(msg, log_level=None):
    global _logger
    if log_level is None:
        log_level = logging.INFO
    if log_level >= logging.ERROR:
        _ErrorsStats.register_error_occurrence()
    _logger.log(log_level, msg)


def log_exception(err: Exception):
    global _logger
    _ErrorsStats.register_error_occurrence()
    _logger.exception(err)


def setup_log(filename=None, *, only_std_out=False,
              fmt_std_out='%(asctime)s %(levelname)s: %(message)s',
              fmt_file='%(asctime)s %(levelname)s: %(message)s',
              fmt_err='%(asctime)s %(levelname)s: %(message)s',
              error_notification_callback: callable = None):
    """
    Setups up logging handlers. Only needs to be called once

    :param filename: The file to save logs to
    :param only_std_out: If True does not log to file
    :param fmt_std_out: Format to use for Standard Out
    :param fmt_file: Format to use for file logging
    :param fmt_err: Format to use for Errors
    :param error_notification_callback: Called at the end of execution if
    there were errors
    :return:
    """
    global _logger, _log_dir

    if _logger.hasHandlers():
        log(f'{"!" * 20} REUSING LOG {"!" * 92}')
        return

    if filename is None:
        filename = \
            f'{_log_dir}run {datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log'
    _log_dir = os.path.abspath(os.path.dirname(filename))

    mkdir(_log_dir)
    if not only_std_out:
        # Set up a file handler
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(
            logging.Formatter(fmt_file))
        file_handler.setLevel(logging.DEBUG)
        _logger.addHandler(file_handler)

    # Set up standard output
    std_stream_handler = logging.StreamHandler(sys.stdout)
    std_stream_handler.setFormatter(
        logging.Formatter(fmt_std_out))
    std_stream_handler.setLevel(logging.DEBUG)
    _logger.addHandler(std_stream_handler)

    # Set up error output
    err_stream_handler = logging.StreamHandler(sys.stderr)
    err_stream_handler.setFormatter(
        logging.Formatter(fmt_err))
    err_stream_handler.setLevel(logging.ERROR)
    _logger.addHandler(err_stream_handler)

    atexit.register(_check_error)

    if error_notification_callback is not None:
        _ErrorsStats.register_notification_callback(error_notification_callback)

    # Set default log level accepted
    _logger.setLevel(logging.INFO)  # Increased to stop matplotlib
    log('\n<<<<<<<<<<<<<<<<<<<<<< LOG SETUP >>>>>>>>>>>>>>>>>>>>>>')


def set_log_level(level):
    global _logger
    _logger.setLevel(level)


def _check_error():
    """
    See if any errors occurred and add warning to end of output
    NB: Expected to be called at or near end of execution to give user easy
    location to if an error occurred
    :return:
    """
    if _ErrorsStats.has_occurred():
        log(f'!!! {_ErrorsStats.COUNT} ERRORS OCCURRED !!!', logging.ERROR)
        _ErrorsStats.notify_err()


class _ErrorsStats:
    COUNT = 0  # Tracks how many errors occurred

    @classmethod
    def register_error_occurrence(cls):
        # add new logger if first error
        if not cls.has_occurred():
            _register_special_error_logger()
        cls.COUNT += 1

    @classmethod
    def has_occurred(cls):
        return cls.COUNT > 0

    @classmethod
    def notify_err(cls):
        from opylib import notify
        notify.notify_err()

    @classmethod
    def register_notification_callback(cls, callback):
        cls.notify_err = callback


def _register_special_error_logger():
    global _logger
    error_handler = logging.FileHandler(os.path.join(_log_dir, 'ERRORS.log'))
    error_handler.setFormatter(
        logging.Formatter('%(asctime)s %(message)s'))
    error_handler.setLevel(logging.ERROR)
    _logger.addHandler(error_handler)
