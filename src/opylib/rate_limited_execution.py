import logging

from opylib.log import log
from opylib.timer import set_timeout


class RateLimitedExecution:
    """
    Designed to run a functions with a maximum frequency.
    Will only run the first request per function until that function has
    been run. Uses a singleton so that the client classes do not need to
    keep a reference to the instance because of challenges with serialising
    classes that have references to threads. (Error msg: "TypeError:
    cannot pickle '_thread.lock' object")
    """
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RateLimitedExecution()
        return cls._instance

    def __init__(self):
        self.pending = {}

    def _execute(self, function: callable, args: list, kwargs: dict):
        self.pending.pop(function)
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        function(*args, **kwargs)

    def register(self, timeout: float, function: callable, args: list = None,
                 kwargs: dict = None) -> bool:
        """
        Registers function if it is not currently pending
        :param timeout: Number of seconds to delay before running the timer
        :param function: The function to be called
        :param args: The positional arguments for the function
        :param kwargs: The key word arguments for the function
        :return: True if was not already pending otherwise False
        """
        if self.is_pending(function):
            log(f'[RateLimit] Request to register ignored. Already pending '
                f'{function}', logging.DEBUG)
            return False
        else:
            self.pending[function] = \
                set_timeout(timeout, self._execute, [function, args, kwargs])
            log(f'[RateLimit] Registered {function} with {timeout} second '
                f'timeout', logging.DEBUG)
            return True

    def is_pending(self, function: callable):
        return function in self.pending

    def cancel(self, function: callable) -> bool:
        """
        Attempts to cancel the function call.
        :param function: The function to cancel the call to
        :return: True if the function was pending else False
        """
        if self.is_pending(function):
            self.pending[function].cancel()
            self.pending.pop(function)
            log(f'[RateLimit] Canceled {function}', logging.DEBUG)
            return True
        else:
            log(f'[RateLimit] Not Pending. Did NOT cancel {function}',
                logging.DEBUG)
            return False
