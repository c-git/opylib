import logging
import os
import sys
from time import sleep

from opylib.log import log

if sys.platform.startswith('linux'):
    try:
        # noinspection PyUnresolvedReferences
        from google.colab import output


        def make_sound(_):
            output.eval_js(
                'new Audio('
                '"https://upload.wikimedia.org/wikipedia/commons/0/05'
                '/Beep-09.ogg").play()')


        def notify_err(_):
            make_sound()

    except ModuleNotFoundError:
        def make_sound(sleep_time=3):
            os.system('spd-say "Process finished"')
            sleep(sleep_time)


        def notify_err(sleep_time=0):
            os.system('spd-say "Errors detected"')
            sleep(sleep_time)

elif sys.platform.startswith('darwin'):
    def make_sound(sleep_time=3):
        os.system('say "Process finished"')
        sleep(sleep_time)


    def notify_err(sleep_time=0):
        os.system('say "Errors detected"')
        sleep(sleep_time)

elif sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
    import winsound


    def make_sound(_=None):
        for i in range(1, 5):
            winsound.Beep(i * 400, 200)
        for i in range(5, 1, -1):
            winsound.Beep(i * 400, 200)


    def notify_err(_=None):
        for i in range(2):
            winsound.Beep(2000, 500)
            winsound.Beep(400, 200)
else:
    def make_sound(_=None):
        log(Exception(f'No Sound because unexpected OS: {sys.platform}'),
            logging.WARN)


    def notify_err(_=None):
        make_sound()
