import numpy as np
from colorama import Fore, init
init()


class Defaults:
    """has all the default values"""

    def __init__(self):
        self.miny = 0
        self.minx = 1
        self.maxy = 87
        self.maxx = 20
        self.maxtime = "3:00"


objdef = Defaults()


class Person:
    """contains basic prop"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lenx = 3
        self.leny = 3
        self.board = np.array(
            [[" ", "^", " "], ["*", "*", "*"], ["*", " ", "*"]])

    def reposition(self, x, y):
        if self.x + x > objdef.maxx or self.x + x < objdef.minx or self.y + \
                y > objdef.maxy or self.y + y < objdef.miny:
            return
        self.x = self.x + x
        self.y = self.y + y

    def screen(self, obj):
        for i in range(self.lenx):
            for j in range(self.leny):
                obj.board[self.x + i, self.y + j] = self.board[i, j]

    def clear(self, obj):
        for i in range(self.lenx):
            for j in range(self.leny):
                obj.board[self.x + i, self.y + j] = " "

    def gravity(self, obj):
        if self.x + 3 > objdef.maxx:
            return
        self.clear(obj)
        self.x = self.x + 1


class Din(Person):

    def __init__(self, x, y):
        Person.__init__(self, x, y)
        self.board = np.array(
            [[" ", "^", " "], ["*", "*", "*"], ["*", " ", "*"]])
        self.coins = 0
        self.lives = 3
        self.sheild = "NO"

    def printscore(self):
        print(
            "LIVES:",
            self.lives,
            "\t COINS:",
            self.coins,
            "\t SHEILD:",
            self.sheild)


class Board:
    """description"""

    def __init__(self, row, col):
        self.board = np.full((row, col), " ")
        self.coltest = np.full((row, col), " ")
        self.row = row
        self.col = col
        for i in range(col):
            self.board[0, i] = "#"
            self.board[21, i] = "#"

    def screen(self, start):
        for i in range(22):
            for j in range(90):
                if i == 0 or i == 21:
                    print(Fore.RED, end='')
                print(self.board[i, start + j], end='')
            print(Fore.WHITE)


class coins:
    def __init__(self, row, col):
        self.visibility = True
        self.row = row
        self.col = col
