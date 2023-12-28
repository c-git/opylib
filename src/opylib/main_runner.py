import sys
from typing import Callable, Optional

from opylib.log import log, log_exception, setup_log, have_errors_occurred
from opylib.notify import make_sound
from opylib.stopwatch import StopWatch


def main_runner(main: Callable, *, should_complete_notify: bool = True, exit_code_on_error: Optional[int | str] = 1):
    """
    Takes care of setup, exception and wind down boilerplate code.
    Example:

    if __name__ == '__main__':
        main_runner(main)

    :param main: The function to be called that will actually do the work
    :param should_complete_notify: Controls if a completed notification is given
    :param exit_code_on_error: If set and the program has errors then it will forward the value passed to sys.exit
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

    if exit_code_on_error is not None and have_errors_occurred():
        sys.exit(exit_code_on_error)
