import os
import sys


def restart_script():
    """
    Restarts the currently running python script (Current process is replaced)

    src: https://www.codegrepper.com/code-examples/python/restart+python
            +script+from+itself
    """
    os.execl(sys.executable, sys.executable, *sys.argv)
