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
        self._lives = 3
        self._sheild = "NO"
        self._score = 0
        self._board = np.array(
            [[" ", "^", " "], ["*", "*", "*"], ["*", " ", "*"]])

    def reposition(self, x, y, obj):
        if self._x + x > objdef.maxx or self._x + x < objdef.minx or self._y + \
                y > objdef.maxy:
            return
        ret = self.col(x, y, obj)
        if ret == 1:
            return
        self._x = self._x + x
        self._y = self._y + y

    def col(self, x, y, obj):
        return 0

    def screen(self, obj):
        for i in range(self._lenx):
            for j in range(self._leny):
                obj.board[self._x + i, self._y + j] = self._board[i, j]

    def clear(self, obj):
        for i in range(self._lenx):
            for j in range(self._leny):
                obj.board[self._x + i, self._y + j] = " "

    def gravity(self, obj):
        "reposition if out of screen and fake gravitational effect"
        if self._y < objdef.miny:
            self._lives = self._lives - 1
            self._y = self._y + 20
            self._x = 18
        if self._x + 3 > objdef.maxx:
            return
        self.clear(obj)
        self.reposition(1,0,obj)

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
        self.__time = 60

    def col(self, x, y, obj):
        if obj.coltest[self._x + x, self._y + y] == 2 or\
                obj.coltest[self._x + x, self._y + y + 1] == 2\
                or obj.coltest[self._x + x, self._y + y + 2] == 2\
                or obj.coltest[self._x + x + 1, self._y + y] == 2\
                or obj.coltest[self._x + x + 1, self._y + y + 1] == \
                2 or obj.coltest[self._x + x + 1, self._y + y + 2] \
                == 2 or obj.coltest[self._x + x + 2, self._y + y]\
                == 2 or obj.coltest[self._x + x + 2, self._y + y + 1]\
                == 2 or obj.coltest[self._x + x + 2, self._y + y + 2] == 2:
            self._lives = self._lives - 1
            self.iskill(obj)
            self._x = 18
            return 1

    def printscore(self):
        print(Fore.CYAN, end='')
        print(
            "TIME:",
            self.__time,
            "\tLIVES:",
            self._lives,
            "\t SCORE:",
            self._score,
            "\t COINS:",
            self.__coins,
            "\t SHEILD:",
            self._sheild)
        print(Style.RESET_ALL, end='')

    def iskill(self, obj, kill=1):
        "update score and check if player is kill"
        self._score = int((objdef.start * 3 + self.__coins * 40))
        self._time = 60 - int(time.time()-objdef.time)
        if self._lives == 0 or kill == 0 or self.__time<0:
            os.system('clear')
            self.printscore()
            obj.gameover()

    def updatecoins(self,inc):
        self.__coins = self.__coins + inc

class Enemy(Person):
    """class definition of the dragon"""

    def __init__(self, x, y):
        Person.__init__(self, x, y)
        self._board = np.array([
            [".", ".", ".",".", ".", ".",".",".",".","."], 
            [".", ".", "."," ", ".", "."," ",".",".","."], 
            [".", ".", ".",".", ".", ".",".",".",".","."], 
            [".", ".", ".",".", " ", " ",".",".",".","."], 
            [".", ".", "."," ", ".", "."," ",".",".","."], 
            [" ", ".", ".",".", ".", ".",".",".","."," "], 
            [" ", ".", ".",".", ".", ".",".",".","."," "], 
            [" ", ".", ".",".", ".", ".",".",".","."," "], 
            [" ", ".", ".",".", ".", ".",".",".","."," "], 
            [".", ".", ".",".", ".", ".",".",".",".","."]
                ])
        self._lives = 10
        self._lenx = 10
        self._leny = 10 
    def screen(self, obj):
        Person.screen(self,obj)
        for i in range(self._lenx):
            for j in range(self._leny):
                obj.coltest[self._x + i,self._y + j] = 2

    def clear(self, obj):
        Person.clear(self,obj)
        for i in range(self._lenx):
            for j in range(self._leny):
                obj.board[self._x + i,self._y + j] = " "
                obj.coltest[self._x + i, self._y + j] = 0

    def reposition(self,din_x,obj):
        self.clear(obj)
        din_x = din_x - 7
        if din_x < 1:
            din_x = 1
        self._x = din_x
        self.screen(obj)



class Board:
    """description"""

    def __init__(self, row, col):
        self.board = np.full((row, col), " ")
        self.coltest = np.full((row, col), 0)
        self._row = row
        self._col = col
        for i in range(col):
            self.board[0, i] = "#"
            self.board[21, i] = "#"

    def screen(self, start):
        if start > 300:
            start = 305
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
                elif self.board[i, start + j] == "✖":
                    print(Fore.RED, end='')
                elif self.board[i, start + j] == ".":
                    print(Fore.GREEN, end='')
                    # print(Back.GREEN, end='')
                    # print(Back.RED, end='')
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

class Objects:
    def __init__(self, row, col):
        self._visibility = True
        self._row = row
        self._col = col

    def screen(self, obj):
        if not self._visibility:
            return
        obj.board[self._row, self._col] = ""

class Coin(Objects):
    def __init__(self, row, col):
        Objects.__init__(self,row,col)

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
    def __init__(self, ty, row, col):
        Objects.__init__(self,row,col)
        self.__ty = ty
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
                    obj.board[self._row + i, self._col + j] = self.board[i, j]
                    obj.coltest[self._row + i, self._col + j] = 2

    def clear(self, obj):
        self._visibility = False
        for i in range(5):
            for j in range(5):
                if self.board[i, j] != " ":
                    obj.board[self._row + i, self._col + j] = " "
                    obj.coltest[self._row + i, self._col + j] = 0


    def collision(self,obj,bullet):
        if self._visibility == False:
            return
        x,y=bullet.rowcol()
        for i in range(5):
            for j in range(5):
                if self.board[i, j] != " " and self._row +i == x and self._col + j ==y:
                    self.clear(obj)
                    return 1

        return 0
        
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
        self.time= time.time()

    def update(self, x):
        self.maxy = self.maxy1 + x
        self.miny = self.miny1 + x
        self.start = x


objdef = Defaults()


