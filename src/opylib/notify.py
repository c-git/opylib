import logging
import os
import sys
from time import sleep

from opylib.log import log

if sys.platform.startswith('linux'):
    try:
        # noinspection PyUnresolvedReferences,PyPackageRequirements
        from google.colab import output


        def make_sound():
            output.eval_js(
                'new Audio('
                '"https://upload.wikimedia.org/wikipedia/commons/0/05'
                '/Beep-09.ogg").play()')


        def notify_err():
            make_sound()

    except ModuleNotFoundError:
        def make_sound():
            os.system('spd-say "Process finished"')


        def notify_err():
            sleep(2)  # Delay before running to late end of program finish playing
            os.system('spd-say "Errors detected"')

elif sys.platform.startswith('darwin'):
    def make_sound():
        os.system('say "Process finished"')


    def notify_err():
        sleep(2)  # Delay before running to late end of program finish playing
        os.system('say "Errors detected"')

elif sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
    import winsound


    def make_sound():
        for i in range(1, 5):
            winsound.Beep(i * 400, 200)
        for i in range(5, 1, -1):
            winsound.Beep(i * 400, 200)


    def notify_err():
        for i in range(2):
            winsound.Beep(2000, 500)
            winsound.Beep(400, 200)
else:
    def make_sound():
        log(Exception(f'No Sound because unexpected OS: {sys.platform}'),
            logging.WARN)


    def notify_err():
        make_sound()
