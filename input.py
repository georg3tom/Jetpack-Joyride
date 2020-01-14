class TimeoutExpired(Exception):
    pass


def alarm_handler(signum, frame):
    raise TimeoutExpired


class _Getch:
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import signal
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.setitimer(signal.ITIMER_REAL, 0.6)
        try:
            char = self.getget()
        except TimeoutExpired:
            char = None
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return char

    def getget(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
