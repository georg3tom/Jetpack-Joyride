import os
import sys
import signal
from colorama import init
from input import _Getch as getch
from classes import Board, Din, Coin, Rods ,Enemy
from random import randrange
import time
from defn import cls, bullet_maintainance, coin_maintainance
from particles import Bullet


if __name__ == "__main__":
    os.system('clear')
    objboard = Board(23, 400)
    din = Din(18, 5)
    din.screen(objboard)
    boss = Enemy(11,378)
    boss.screen(objboard)

    curpos = 0

    coins = []
    rods = []
    bullets = []

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

    coin_maintainance(coins,objboard,din)
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
            coin_maintainance(coins,objboard,din)
            din.reposition(0, 1, objboard)

        elif char == 'f':
            bullets.append(Bullet(din,objboard))

        din.gravity(objboard)

        coin_maintainance(coins,objboard,din)

        if curpos < 0.5:
            os.system('clear')

        cls()
        bullets = bullet_maintainance(bullets,objboard,rods)
        din.clear(objboard)
        din.screen(objboard)
        din.printscore()
        # print(curpos)
        objboard.screen(int(curpos * 4))
        curpos = time.time() - start_time
        din.iskill(objboard)
