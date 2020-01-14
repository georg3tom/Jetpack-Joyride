import os
import sys
import signal
from colorama import init
from input import _Getch as getch
from classes import Board, Din


if __name__ == "__main__":
    os.system('clear')
    objboard = Board(23, 400)
    din = Din(18, 5)
    din.screen(objboard)
    din.printscore()
    objboard.screen(0)

    while True:
        char = getch()()

        if char == 'q':
            sys.exit()

        elif char == 'w':
            din.clear(objboard)
            din.reposition(-2, 0)

        elif char == 'a':
            din.clear(objboard)
            din.reposition(0, -1)

        elif char == 'd':
            din.clear(objboard)
            din.reposition(0, 1)

        din.gravity(objboard)
        din.clear(objboard)
        din.screen(objboard)
        os.system('clear')
        din.printscore()
        objboard.screen(0)
