import logging
import threading
from typing import Dict, List, Tuple

from opylib.log import log


def _prep_args_and_kwargs(args, kwargs) -> Tuple[List, Dict]:
    """
    Clean up / Catch possible problems with parameters
    :param args: The args value to be cleaned up
    :param kwargs: The kwargs value to be cleaned up
    :return: Cleaned args and kwargs
    """
    if args is None:
        args = []
    if not isinstance(args, list):
        log(f'Expected args to be of type list but got {type(args)}. '
            f'Object has been wrapped in list to prevent error!!!',
            logging.WARNING)
        args = [args]
    if kwargs is None:
        kwargs = {}
    if not isinstance(kwargs, dict):
        raise TypeError(f'Dict required but got kwargs as {type(kwargs)}')

    return args, kwargs


def set_timeout(timeout: float, function: callable, args: list = None,
                kwargs: dict = None) -> threading.Timer:
    """
    Wrapper for library thread timer. Easy to find for future reference and
    sets timer to be a daemon so that it will stop if the main thead
    terminates.

    NB: The interval the timer will wait before executing its action may not
    be exactly the same as the interval specified by the user.

    :param timeout: Number of seconds to delay before running the timer
    :param function: The function to be called
    :param args: The positional arguments for the function
    :param kwargs: The key word arguments for the function
    :return: The timer object so that calling cancel on it will stop the timer
    """
    args, kwargs = _prep_args_and_kwargs(args, kwargs)

    timer = threading.Timer(timeout, function, args, kwargs)

    # So it won't prevent program termination because it hasn't run
    timer.daemon = True

    timer.start()
    return timer


def set_interval(interval: float, function: callable, args: list = None,
                 kwargs: dict = None) -> threading.Event:
    """
    Repeated timer every interval seconds.

    NB: The interval the timer will wait before executing its action may not
    be exactly the same as the interval specified by the user.

    :param interval: Number of seconds to delay before running the timer
        each time
    :param function: The function to be called
    :param args: The positional arguments for the function
    :param kwargs: The key word arguments for the function
    :return: A thread event able to cancel the timer (e.g. result.set())
    """
    args, kwargs = _prep_args_and_kwargs(args, kwargs)

    class MyThread(threading.Thread):
        def __init__(self, event):
            threading.Thread.__init__(self)
            self.stopped = event

        def run(self):
            while not self.stopped.wait(interval):
                function(*args, **kwargs)  # call a function

    stop_event = threading.Event()
    t = MyThread(stop_event)
    t.daemon = True
    t.start()
    return stop_event
