import os
import sys
import signal
from colorama import init
from input import _Getch as getch
from classes import Board, Din, Coin, Rods
from random import randrange
import time
from defn import cls


if __name__ == "__main__":
    os.system('clear')
    objboard = Board(23, 400)
    din = Din(18, 5)
    din.screen(objboard)

    curpos = 0

    coins = []
    rods = []

    for i in range(35):
        if i % 2 == 0:
            pass
        coins.append(Coin(randrange(4, 18), randrange(i * 10, i * 10 + 10)))

    for i in range(15):
        if i % 2 == 1:
            pass
        rods.append(
            Rods(
                randrange(4), randrange(
                    4, 13), randrange(
                    i * 20, i * 20 + 10)))

    for coin in coins:
        coin.screen(objboard)

    for rod in rods:
        rod.screen(objboard)

    din.printscore()
    objboard.screen(0)
    print("\t\t\t\tPRESS ANY KEY TO START")
    getch().getget()
    start_time = time.time()
    while True:
        char = getch()()

        if char == 'q':
            din.iskill(objboard, 0)

        elif char == 'w':
            din.clear(objboard)
            din.reposition(-2, 0, objboard)

        elif char == 'a':
            din.clear(objboard)
            din.reposition(0, -1, objboard)

        elif char == 'd':
            din.clear(objboard)
            din.reposition(0, 1, objboard)
            for i in coins:
                i.coin_col(din)
            din.reposition(0, 1, objboard)
            for i in coins:
                i.coin_col(din)
            din.reposition(0, 1, objboard)
            for i in coins:
                i.coin_col(din)
            din.reposition(0, 1, objboard)

        din.gravity(objboard)

        for i in coins:
            i.coin_col(din)

        # os.system('clear')
        if curpos < 0.5:
            os.system('clear')

        cls()
        din.clear(objboard)
        din.screen(objboard)
        din.printscore()
        objboard.screen(int(curpos * 4))
        curpos = time.time() - start_time
        din.iskill(objboard)
