import os
import sys
import signal
from colorama import init
from input import _Getch as getch
from classes import Board, Din, Coin, Rods ,Enemy, Magnet ,Speedb
from random import randrange
import time
from defn import cls, bullet_maintainance, coin_maintainance, enemy_maintainance, speedboost, enemy_kill, snowball_maintainance,speedb_maintainance
from particles import Bullet, Snow


if __name__ == "__main__":
    os.system('clear')
    objboard = Board(23, 400)
    din = Din(18, 10)
    din.screen(objboard)
    boss = Enemy(11,378)
    boss.screen(objboard)
    speedfactor = 0
    speedtime = 0
    prev_speed = -1
    tmp=0
    gravity_time = time.time()
    snow_time =gravity_time
    bosscol = 305

    coins = []
    rods = []
    bullets = []
    snowballs = []
    magnets = []
    speedbs = []

    #generate coins,rods and speedboost
    for i in range(35):
        if i % 2 == 0:
            continue
        coins.append(Coin(randrange(4, 19), randrange(i * 10, i * 10 + 10)))
        coins.append(Coin(randrange(4, 19), randrange(i * 10, i * 10 + 10)))

    magnets.append(Magnet(randrange(4, 18), randrange(130,140)))
    magnets.append(Magnet(randrange(4, 18), randrange(230,240)))
    magnets.append(Magnet(randrange(4, 18), randrange(330,340)))

    speedbs.append(Speedb(randrange(4, 18), randrange(110,120)))
    speedbs.append(Speedb(randrange(4, 18), randrange(250,260)))

    for i in range(33):
        if i % 2 == 1 :
            continue
        rods.append( Rods( randrange(4), randrange( 4, 15), randrange( i * 10, i * 10 + 5)))

    # render rods and speedboost
    coin_maintainance(coins,objboard,din)
    for rod in rods:
        rod.screen(objboard)

    for i in speedbs:
        i.screen(objboard)

    #wait for keypress to start
    print()
    din.printscore()
    objboard.screen(tmp,din)
    print("\t\t\t\tPRESS ANY KEY TO START")
    getch().getget()
    start_time = time.time()

    while True:
        #check for input
        char = getch()()

        if char == 'q':
            din.iskill(objboard, 0)

        elif char == 'w':
            gravity_time = time.time()
            din.clear(objboard)
            din.reposition(-1, 0, objboard)
            coin_maintainance(coins,objboard,din)
            din.reposition(-1, 0, objboard)
            coin_maintainance(coins,objboard,din)
            din.reposition(-1, 0, objboard)

        elif char == 'a':
            din.clear(objboard)
            din.reposition(0, -1, objboard)
            coin_maintainance(coins,objboard,din)
            din.reposition(0, -1, objboard)

        elif char == 'd':
            din.clear(objboard)
            din.reposition(0, 1, objboard)
            coin_maintainance(coins,objboard,din)
            din.reposition(0, 1, objboard)

        elif char == 'f':
            bullets.append(Bullet(din,objboard))

        elif char == ' ':
            din.ssheild(1)


        if time.time()-gravity_time > 0.3:
            din.gravity(objboard)
            coin_maintainance(coins,objboard,din)
            if time.time()-gravity_time > 0.5:
                din.gravity(objboard)
                coin_maintainance(coins,objboard,din)
                if time.time()-gravity_time > 0.8:
                    din.gravity(objboard)

        coin_maintainance(coins,objboard,din)

        if tmp ==0:
            os.system('clear')

        cls()
        for rod in rods:
            rod.screen(objboard)
        speedfactor,prev_speed = speedb_maintainance(speedbs,objboard,din,prev_speed)
        for magnet in magnets:
            magnet.attract(din,objboard)
        din.ssheild()
        bullets = bullet_maintainance(bullets,objboard,rods,snowballs)
        snowball_maintainance(snowballs,din,objboard)
        din.clear(objboard)
        din.printscore()
        if time.time()-speedtime > 0.2:
            speedtime = time.time()
            tmp = tmp +1
            if tmp < bosscol:
                din.stay(1,objboard)
            if speedfactor == 1:
                tmp = tmp + 2
                if tmp < bosscol:
                    din.stay(2,objboard)
        din.screen(objboard)
        if tmp > bosscol:
            enemy_kill(boss,din,objboard,bullets)
            if time.time() - snow_time > 1.4 :
                snowballs.append(Snow(boss,objboard,din))
                snow_time = time.time()
        objboard.screen(tmp,din)
        enemy_maintainance(boss,din,objboard)
        din.iskill(objboard)
