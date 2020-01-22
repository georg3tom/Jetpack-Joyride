import numpy as np
import sys
import os
import time
from colorama import Fore, Back, init, Style
init()


class Person:
    """contains basic prop"""

    def __init__(self, x, y):
        "x = row, y = col, not to be confused with coordinates"
        self._x = x
        self._y = y
        self._lenx = 3
        self._leny = 3
        self._lives = 5
        self._sheild = "OFF"
        self._score = 0
        self._board = np.array(
            [[" ", "^", " "], ["*", "*", "*"], ["*", " ", "*"]])

    def reposition(self, x, y, obj):
        if self._x + x > objdef.retmaxx() or self._x + x < objdef.retminx() or self._y + \
                y > objdef.retmaxy():
            return
        ret = self.col(x, y, obj)
        if ret == 1:
            return
        self._x = self._x + x
        self._y = self._y + y

    def col(self, x, y, obj):
        return 0

    def screen(self, obj):
        if self._x > 18:
            self._x = 18
        board = obj.retboard()
        for i in range(self._lenx):
            for j in range(self._leny):
                board[self._x + i, self._y + j] = self._board[i, j]

    def clear(self, obj):
        board = obj.retboard()
        for i in range(self._lenx):
            for j in range(self._leny):
                board[self._x + i, self._y + j] = " "
        obj.getboard(board)

    def gravity(self, obj):
        "reposition if out of screen and fake gravitational effect"
        if self._y < objdef.retminy():
            self._lives = self._lives - 1
            self._y = self._y + 20
            self._x = 18
        if self._x + 3 > objdef.retmaxx():
            return
        self.clear(obj)
        self.reposition(1, 0, obj)

    def retx(self):
        return self._x

    def rety(self):
        return self._y


class Din(Person):
    """class definition of the protagonist"""

    def __init__(self, x, y):
        Person.__init__(self, x, y)
        self._board = np.array(
            [[" ", "*", " "], ["*", "*", "*"], ["*", " ", "*"]])
        self.__coins = 0
        self.__time = 100
        self.__sheild_time = -1

    def col(self, x, y, obj):
        if self.issheild():
            return 0
        coltest = obj.retcoltest()
        if coltest[self._x + x, self._y + y] == 3 or\
                coltest[self._x + x, self._y + y + 1] == 3\
                or coltest[self._x + x, self._y + y + 2] == 3\
                or coltest[self._x + x + 1, self._y + y] == 3\
                or coltest[self._x + x + 1, self._y + y + 1] == \
                3 or coltest[self._x + x + 1, self._y + y + 2] \
                == 3 or coltest[self._x + x + 2, self._y + y]\
                == 3 or coltest[self._x + x + 2, self._y + y + 1]\
                == 3 or coltest[self._x + x + 2, self._y + y + 2] == 3:
            return 1

        if coltest[self._x + x, self._y + y] == 2 or\
                coltest[self._x + x, self._y + y + 1] == 2\
                or coltest[self._x + x, self._y + y + 2] == 2\
                or coltest[self._x + x + 1, self._y + y] == 2\
                or coltest[self._x + x + 1, self._y + y + 1] == \
                2 or coltest[self._x + x + 1, self._y + y + 2] \
                == 2 or coltest[self._x + x + 2, self._y + y]\
                == 2 or coltest[self._x + x + 2, self._y + y + 1]\
                == 2 or coltest[self._x + x + 2, self._y + y + 2] == 2:
            self._lives = self._lives - 1
            self.iskill(obj)
            if objdef.retstart() < 305:
                self.ssheild(2)
                self._x = 18
            return 1
        return 0

    def stay(self, k, obj):
        for i in range(k):
            self.reposition(0, 1, obj)

    def issheild(self):
        if self._sheild == "ON":
            return True
        return False

    def ssheild(self, x=0):
        if x == 2:
            self.__sheild_time = -1
            x = 1
        if x == 1:
            if self._sheild == "OFF":
                self._sheild = "ON"
                self.__sheild_time = time.time()
                return
        if self._sheild=="CHARGING" and time.time() - self.__sheild_time > 5:
            self.__sheild_time = time.time()
            self._sheild = "OFF"

        elif self._sheild!="OFF" and time.time()-self.__sheild_time >5:
            self.__sheild_time = time.time()
            self._sheild = "CHARGING"

    def printscore(self):
        tmp = int(self.__time / 60)
        prtime = str(tmp) + ":" + str(self.__time - (tmp * 60))
        print(Fore.CYAN, end='')
        print(
            "TIME:",
            prtime,
            "\tLIVES:",
            self._lives,
            "\t SCORE:",
            self._score,
            "\t COINS:",
            self.__coins,
            "\t SHEILD:",
            self._sheild, "      ")
        print(Style.RESET_ALL, end='')

    def iskill(self, obj, kill=1):
        "update score and check if player is kill"
        self._score = int((objdef.retstart() * 3 + self.__coins * 40))
        self.__time = 100 - int(time.time() - objdef.rettime())
        if self._lives == 0 or kill == 0 or self.__time < 1:
            os.system('clear')
            self.printscore()
            obj.gameover(self)

    def updatecoins(self, inc):
        self.__coins = self.__coins + inc

    def updatescore(self, val):
        self._score = self._score + val


class Enemy(Person):
    """class definition of the creeper"""

    def __init__(self, x, y):
        Person.__init__(self, x, y)
        self._board = np.array([
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", " ", ".", ".", " ", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", " ", " ", ".", ".", ".", "."],
            [".", ".", ".", " ", ".", ".", " ", ".", ".", "."],
            [" ", ".", ".", ".", ".", ".", ".", ".", ".", " "],
            [" ", ".", ".", ".", ".", ".", ".", ".", ".", " "],
            [" ", ".", ".", ".", ".", ".", ".", ".", ".", " "],
            [" ", ".", ".", ".", ".", ".", ".", ".", ".", " "],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
        ])
        self._lives = 10
        self._lenx = 10
        self._leny = 10

    def screen(self, obj):
        Person.screen(self, obj)
        coltest = obj.retcoltest()
        for i in range(self._lenx):
            for j in range(self._leny):
                coltest[self._x + i, self._y + j] = 2
        obj.getcoltest(coltest)

    def clear(self, obj):
        Person.clear(self, obj)
        coltest = obj.retcoltest()
        for i in range(self._lenx):
            for j in range(self._leny):
                # obj.board[self._x + i,self._y + j] = " "
                coltest[self._x + i, self._y + j] = 0
        obj.getcoltest(coltest)

    def collision(self, bullet):
        x, y = bullet.rowcol()
        for i in range(self._lenx):
            for j in range(self._leny):
                if self._x + i == x and self._y + j == y:
                    self._lives = self._lives - 1
                    return 1
        return 0

    def gameover(self, obj, din):
        if self._lives < 1:
            din.updatescore(1000)
            for i in range(self._lenx):
                for j in range(self._leny):
                    if self._board[i][j] == ".":
                        self._board[i][j] = "#"
            self.clear(obj)
            self.screen(obj)
            obj.gameover(din, " YOU WIN")

    def reposition(self, din_x, obj):
        self.clear(obj)
        din_x = din_x - 7
        if din_x < 1:
            din_x = 1
        self._x = din_x
        self.screen(obj)


class Board:
    """screen on which drawing is done"""

    def __init__(self, row, col):
        self.__board = np.full((row, col), " ")
        self.__coltest = np.full((row, col), 0)
        self._row = row
        self._col = col
        for i in range(col):
            self.__board[0, i] = "#"
            self.__board[21, i] = "#"

    def screen(self, start, din):
        if start > 305:
            start = 305
        objdef.update(start)
        for i in range(22):
            for j in range(90):
                if i == 0 or i == 21:
                    print(Fore.RED, end='')
                    print(Back.RED, end='')
                elif self.__board[i, start + j] == "#":
                    print(Fore.RED, end='')
                    print(Back.RED, end='')
                elif self.__board[i, start + j] == "":
                    print(Fore.YELLOW, end='')
                    print(Style.BRIGHT, end='')
                elif self.__board[i, start + j] == "*" and din.issheild():
                    print(Fore.MAGENTA, end='')
                    print(Back.MAGENTA, end='')
                elif self.__board[i, start + j] == "*":
                    print(Fore.BLUE, end='')
                    print(Back.BLUE, end='')
                elif self.__board[i, start + j] == "@":
                    print(Fore.RED, end='')
                    print(Back.RED, end='')
                elif self.__board[i, start + j] == "✖":
                    print(Fore.RED, end='')
                elif self.__board[i, start + j] == ".":
                    print(Fore.GREEN, end='')
                    print(Back.GREEN, end='')
                elif self.__board[i, start + j] == "/" or self.__board[i, start + j] == "-" or self.__board[i, start + j] == "|" or self.__board[i, start + j] == "\\":
                    print(Fore.RED, end='')
                    # print(Back.BLUE, end='')
                print(self.__board[i, start + j], end='')
                print(Style.RESET_ALL, end='')
            print()

    def gameover(self, din, txt2=" YOU LOSE"):
        txt = "GAME OVER"
        for i in range(len(txt)):
            self.__board[11, 40 + objdef.retstart() + i] = txt[i]
        for i in range(len(txt2)):
            self.__board[12, 40 + objdef.retstart() + i] = txt2[i]
        self.screen(objdef.retstart(), din)
        sys.exit()

    def retboard(self):
        return self.__board

    def getboard(self, board):
        self.__board = board

    def retcoltest(self):
        return self.__coltest

    def getcoltest(self, board):
        self.__coltest = board


class Objects:
    """parent class for rods and coins"""

    def __init__(self, row, col):
        self._visibility = True
        self._row = row
        self._col = col

    def screen(self, obj):
        if not self._visibility:
            return
        board = obj.retboard()
        board[self._row, self._col] = ""
        obj.getboard(board)


class Coin(Objects):
    """coin class"""

    def __init__(self, row, col):
        Objects.__init__(self, row, col)

    def coin_col(self, obj):
        if not self._visibility:
            return
        if obj.retx() == self._row and obj.rety() == self._col or obj.retx() == self._row \
                and obj.rety() + 1 == self._col or obj.retx() == self._row and \
                obj.rety() + 2 == self._col or obj.retx() + 1 == self._row and \
                obj.rety() == self._col or obj.retx() + 1 == self._row and obj.rety()\
                + 1 == self._col or obj.retx() + 1 == self._row and obj.rety() +\
                2 == self._col or obj.retx() + 2 == self._row and obj.rety() ==\
                self._col or obj.retx() + 2 == self._row and obj.rety() + 1 == \
                self._col or obj.retx() + 2 == self._row and obj.rety() + 2 ==\
                self._col:
            self._visibility = False
            obj.updatecoins(1)


class Rods(Objects):
    """rod class"""

    def __init__(self, ty, row, col):
        Objects.__init__(self, row, col)
        self.__ty = ty
        self.__board = np.array([[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [
            " ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "]])
        if ty == 0:
            self.__board = np.array([[" ", " ", "*", " ", " "], [" ", " ", "|", " ", " "], [
                " ", " ", "|", " ", " "], [" ", " ", "|", " ", " "], [" ", " ", "*", " ", " "]])
        if ty == 1:
            self.__board = np.array([[" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "], [
                "*", "-", "-", "-", "*"], [" ", " ", " ", " ", " "], [" ", " ", " ", " ", " "]])
        if ty == 2:
            self.__board = np.array([[" ", " ", " ", " ", "*"], [" ", " ", " ", "/", " "], [
                " ", " ", "/", " ", " "], [" ", "/", " ", " ", " "], ["*", " ", " ", " ", " "]])
        if ty == 3:
            self.__board = np.array([["*", " ", " ", " ", " "], [" ", "\\", " ", " ", " "], [
                " ", " ", "\\", " ", " "], [" ", " ", " ", "\\", " "], [" ", " ", " ", " ", "*"]])

    def screen(self, obj):
        """render rods on board"""
        if not self._visibility:
            return
        board = obj.retboard()
        coltest = obj.retcoltest()
        for i in range(5):
            for j in range(5):
                if self.__board[i, j] != " ":
                    board[self._row + i, self._col + j] = self.__board[i, j]
                    coltest[self._row + i, self._col + j] = 2
        obj.getboard(board)
        obj.getcoltest(coltest)

    def clear(self, obj):
        """remove rods form board"""
        self._visibility = False
        board = obj.retboard()
        coltest = obj.retcoltest()
        for i in range(5):
            for j in range(5):
                if self.__board[i, j] != " ":
                    board[self._row + i, self._col + j] = " "
                    coltest[self._row + i, self._col + j] = 0
        obj.getboard(board)
        obj.getcoltest(coltest)

    def collision(self, obj, bullet):
        """detect bullet collision"""
        if not self._visibility:
            return
        x, y = bullet.rowcol()
        for i in range(5):
            for j in range(5):
                if self.__board[i, j] != " " and self._row + \
                        i == x and self._col + j == y:
                    self.clear(obj)
                    return 1

        return 0


class Magnet(Objects):
    """speedboost class"""

    def __init__(self, row, col):
        Objects.__init__(self, row, col)
        self.__board = np.array([["*", " ", "*"], ["@", "@", "@"]])

    def screen(self, obj):
        board = obj.retboard()
        coltest = obj.retcoltest()
        for i in range(2):
            for j in range(3):
                if self.__board[i, j] != " ":
                    board[self._row + i, self._col + j] = self.__board[i, j]
                    coltest[self._row + i, self._col + j] = 3
        obj.getboard(board)
        obj.getcoltest(coltest)

    def attract(self, din, objboard):
        self.screen(objboard)
        if din.issheild():
            return
        y = din.rety()
        x = din.retx()
        if abs(y - self._col) < 15 and x -2 <= self._row  and x + 4 >= self._row:
            din.clear(objboard)
            if y - self._col < 0:
                din.reposition(0, 1, objboard)
                din.reposition(0, 1, objboard)
                din.reposition(0, 1, objboard)

            else:
                din.reposition(0, -1, objboard)
                din.reposition(0, -1, objboard)
                din.reposition(0, -1, objboard)

            # if x < self._row:
            #     din.reposition(1, 0, objboard)

            # elif x > self._row:
            #     din.reposition(-1, 0, objboard)


class Speedb(Objects):
    def __init__(self, row, col):
        Objects.__init__(self, row, col)

    def screen(self, obj):
        """render speedboost to board"""
        if not self._visibility:
            return
        board = obj.retboard()
        board[self._row, self._col] = "⧖"
        obj.getboard(board)

    def speed_col(self, obj):
        """check is speedboost is activated"""
        if not self._visibility:
            return 0
        if obj.retx() == self._row and obj.rety() == self._col or obj.retx() == self._row \
                and obj.rety() + 1 == self._col or obj.retx() == self._row and \
                obj.rety() + 2 == self._col or obj.retx() + 1 == self._row and \
                obj.rety() == self._col or obj.retx() + 1 == self._row and obj.rety()\
                + 1 == self._col or obj.retx() + 1 == self._row and obj.rety() +\
                2 == self._col or obj.retx() + 2 == self._row and obj.rety() ==\
                self._col or obj.retx() + 2 == self._row and obj.rety() + 1 == \
                self._col or obj.retx() + 2 == self._row and obj.rety() + 2 ==\
                self._col:
            self._visibility = False
            return 1
        return 0


class Defaults:
    """has all the default values"""

    def __init__(self):
        self.__miny = 0
        self.__miny1 = 0
        self.__minx = 1
        self.__maxy = 87
        self.__maxy1 = 87
        self.__maxx = 20
        self.__start = 0
        self.__time = time.time()

    def update(self, x):
        self.__maxy = self.__maxy1 + x
        self.__miny = self.__miny1 + x
        self.__start = x

    def retstart(self):
        return self.__start

    def retmaxx(self):
        return self.__maxx

    def retmaxy(self):
        return self.__maxy

    def retminx(self):
        return self.__minx

    def retminy(self):
        return self.__miny

    def rettime(self):
        return self.__time


objdef = Defaults()
