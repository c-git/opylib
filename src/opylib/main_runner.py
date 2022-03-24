from typing import Callable

from opylib.log import log, log_exception, setup_log
from opylib.notify import make_sound
from opylib.stopwatch import StopWatch


def main_runner(main: Callable, *, should_complete_notify: bool = True):
    """
    Takes care of setup, exception and wind down boilerplate code.
    Example:

    if __name__ == '__main__':
        main_runner(main)

    :param main: The function to be called that will actually do the work
    :param should_complete_notify: Controls if a completed notification is given
    :return:
    """
    setup_log()
    sw = StopWatch('MAIN')
    try:
        main()
    except Exception as e:
        log_exception(e)
    sw.end()
    log('Run COMPLETE.')
    if should_complete_notify:
        make_sound()
