# From http://code.activestate.com/recipes/483752-timelimit-tell-a-function-to-time-out-after-a-time/

import threading
import sys


class TimeoutError(Exception):
    pass


class ExecutionError(Exception):
    pass


def timelimit(timeout):
    def internal(function):
        def internal2(*args, **kw):
            class Calculator(threading.Thread):
                def __init__(self):
                    threading.Thread.__init__(self)
                    self.result = None
                    self.error = None

                def run(self):
                    try:
                        self.result = function(*args, **kw)
                    except Exception:
                        self.error = sys.exc_info()[0]

            c = Calculator()
            c.start()
            c.join(timeout)
            if c.isAlive():
                raise TimeoutError
            elif c.error:
                raise ExecutionError
            return c.result

        return internal2

    return internal
