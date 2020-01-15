import numpy as np
import sys
import os
from colorama import Fore, Back, init, Style
init()


class Defaults:
    """has all the default values"""

    def __init__(self):
        self.miny = 0
        self.miny1 = 0
        self.minx = 1
        self.maxy = 87
        self.maxy1 = 87
        self.maxx = 20
        self.maxtime = "3:00"
        self.start = 0

    def update(self, x):
        self.maxy = self.maxy1 + x
        self.miny = self.miny1 + x
        self.start = x


objdef = Defaults()


class Person:
    """contains basic prop"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lenx = 3
        self.leny = 3
        self.lives = 3
        self.sheild = "NO"
        self.score = 0
        self.board = np.array(
            [[" ", "^", " "], ["*", "*", "*"], ["*", " ", "*"]])

    def reposition(self, x, y, obj):
        if self.x + x > objdef.maxx or self.x + x < objdef.minx or self.y + \
                y > objdef.maxy:
            return
        ret = self.col(x, y, obj)
        if ret == 1:
            return
        self.x = self.x + x
        self.y = self.y + y

    def col(self, x, y, obj):
        return 0

    def screen(self, obj):
        for i in range(self.lenx):
            for j in range(self.leny):
                obj.board[self.x + i, self.y + j] = self.board[i, j]

    def clear(self, obj):
        for i in range(self.lenx):
            for j in range(self.leny):
                obj.board[self.x + i, self.y + j] = " "

    def gravity(self, obj):
        "reposition if out of screen and fake gravitational effect"
        if self.y < objdef.miny:
            self.lives = self.lives - 1
            self.y = self.y + 20
            self.x = 18
        if self.x + 3 > objdef.maxx:
            return
        self.clear(obj)
        self.reposition(1,0,obj)


class Din(Person):
    """class definition of the protagonist"""

    def __init__(self, x, y):
        Person.__init__(self, x, y)
        self.board = np.array(
            [[" ", "*", " "], ["*", "*", "*"], ["*", " ", "*"]])
        self.coins = 0

    def col(self, x, y, obj):
        if obj.coltest[self.x + x, self.y + y] == 2 or\
                obj.coltest[self.x + x, self.y + y + 1] == 2\
                or obj.coltest[self.x + x, self.y + y + 2] == 2\
                or obj.coltest[self.x + x + 1, self.y + y] == 2\
                or obj.coltest[self.x + x + 1, self.y + y + 1] == \
                2 or obj.coltest[self.x + x + 1, self.y + y + 2] \
                == 2 or obj.coltest[self.x + x + 2, self.y + y]\
                == 2 or obj.coltest[self.x + x + 2, self.y + y + 1]\
                == 2 or obj.coltest[self.x + x + 2, self.y + y + 2] == 2:
            self.lives = self.lives - 1
            self.iskill(obj)
            self.x = 18
            return 1

    def printscore(self):
        print(Fore.CYAN, end='')
        print(
            "LIVES:",
            self.lives,
            "\t SCORE:",
            self.score,
            "\t COINS:",
            self.coins,
            "\t SHEILD:",
            self.sheild)
        print(Style.RESET_ALL, end='')

    def iskill(self, obj, kill=1):
        "update score and check if player is kill"
        self.score = int((objdef.start * 3 + self.coins * 40))
        if self.lives == 0 or kill == 0:
            os.system('clear')
            self.printscore()
            obj.gameover()


class Board:
    """description"""

    def __init__(self, row, col):
        self.board = np.full((row, col), " ")
        self.coltest = np.full((row, col), 0)
        self.row = row
        self.col = col
        for i in range(col):
            self.board[0, i] = "#"
            self.board[21, i] = "#"

    def screen(self, start):
        objdef.update(start)
        for i in range(22):
            for j in range(90):
                if i == 0 or i == 21:
                    print(Fore.RED, end='')
                    print(Back.RED, end='')
                elif self.board[i, start + j] == "":
                    print(Fore.YELLOW, end='')
                    print(Style.BRIGHT, end='')
                elif self.board[i, start + j] == "*":
                    print(Fore.BLUE, end='')
                    print(Back.BLUE, end='')
                elif self.board[i, start + j] == "/" or self.board[i, start + j] == "-" or self.board[i, start + j] == "|" or self.board[i, start + j] == "\\":
                    print(Fore.RED, end='')
                    # print(Back.BLUE, end='')
                print(self.board[i, start + j], end='')
                print(Style.RESET_ALL, end='')
            print()

    def gameover(self):
        txt = "GAME OVER"
        for i in range(len(txt)):
            self.board[11, 40 + objdef.start + i] = txt[i]
        self.screen(objdef.start)
        sys.exit()


class Coin:
    def __init__(self, row, col):
        self.visibility = True
        self.row = row
        self.col = col

    def screen(self, obj):
        if not self.visibility:
            return
        obj.board[self.row, self.col] = ""

    def coin_col(self, obj):
        if not self.visibility:
            return
        if obj.x == self.row and obj.y == self.col or obj.x == self.row \
                and obj.y + 1 == self.col or obj.x == self.row and \
                obj.y + 2 == self.col or obj.x + 1 == self.row and \
                obj.y == self.col or obj.x + 1 == self.row and obj.y\
                + 1 == self.col or obj.x + 1 == self.row and obj.y +\
                2 == self.col or obj.x + 2 == self.row and obj.y ==\
                self.col or obj.x + 2 == self.row and obj.y + 1 == \
                self.col or obj.x + 2 == self.row and obj.y + 2 ==\
                self.col:
            self.visibility = False
            obj.coins = obj.coins + 1


class Rods:
    def __init__(self, ty, row, col):
        self.visibility = True
        self.x = row
        self.y = col
        self.ty = ty
        self.board = np.array([[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [
                              " ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "]])
        if ty == 0:
            self.board = np.array([[" ", " ", "|", " ", " "], [" ", " ", "|", " ", " "], [
                " ", " ", "|", " ", " "], [" ", " ", "|", " ", " "], [" ", " ", "|", " ", " "]])
        if ty == 1:
            self.board = np.array([[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [
                "-", "-", "-", "-", "-"], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "]])
        if ty == 2:
            self.board = np.array([[" ", " ", " ", " ", "/"], [" ", " ", " ", "/", " "], [
                " ", " ", "/", " ", " "], [" ", "/", " ", " ", " "], ["/", " ", " ", " ", " "]])
        if ty == 3:
            self.board = np.array([["\\ ", " ", " ", " ", " "], [" ", "\\", " ", " ", " "], [
                " ", " ", "\\", " ", " "], [" ", " ", " ", "\\", " "], [" ", " ", " ", " ", "\\"]])

    def screen(self, obj):
        for i in range(5):
            for j in range(5):
                if self.board[i, j] != " ":
                    obj.board[self.x + i, self.y + j] = self.board[i, j]
                    obj.coltest[self.x + i, self.y + j] = 2

    def clear(self, obj):
        for i in range(5):
            for j in range(5):
                if self.board[i, j] != " ":
                    obj.board[self.x + i, self.y + j] = " "
