import os
import sys


def restart_script():
    """
    Restarts the currently running python script (Current process is replaced)

    Warning: Ensure if you are using multiple thread that the other threads are
        either already stopped or running as daemons

    src: https://www.codegrepper.com/code-examples/python/restart+python
            +script+from+itself
    """
    os.execl(sys.executable, sys.executable, *sys.argv)
