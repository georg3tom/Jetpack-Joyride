import time

class Bullet():
    def __init__(self, din, board):
        self._x = din.retx() + 1
        self._y = din.rety() + 3
        self._visibility = True
        self._start = time.time()
        self.screen(board)

    def clear(self, obj):
        board = obj.retboard()
        self._visibility = False
        board[self._x, self._y] = " "
        obj.getboard(board)
        coltest = obj.retcoltest()
        coltest[self._x,self._y] = 0
        obj.getcoltest(coltest)

    def screen(self, obj):
        board = obj.retboard()
        board[self._x, self._y] = "✖"
        obj.getboard(board)

    def forward(self, obj):
        if time.time() - self._start > 5:
            self.clear(obj)
        if not self._visibility:
            return
        self.clear(obj)
        self._visibility = True
        if self._y > 390:
            self.clear(obj)
            return
        self._y = self._y + 1
        self.screen(obj)

    def rowcol(self):
        return self._x, self._y

    def isvisible(self):
        return self._visibility


class Snow(Bullet):
    def __init__(self, boss, board,din):
        Bullet.__init__(self, boss, board)
        self._x = din.retx()
        self._y = boss.rety() - 1
        self._visibility = True
        coltest = board.retcoltest()
        coltest[self._x,self._y] = 2
        board.getcoltest(coltest)

    def screen(self, obj):
        board = obj.retboard()
        board[self._x, self._y] = "۞"
        obj.getboard(board)


    def collision(self,din):
        row = din.retx()
        col = din.rety()

    def forward(self, board):
        if time.time() - self._start > 11:
            self.clear(board)
        if not self._visibility:
            return
        self.clear(board)
        self._visibility = True
        if self._y > 390:
            self.clear(board)
            return
        coltest = board.retcoltest()
        coltest[self._x,self._y] = 0
        self._y = self._y -1 
        coltest[self._x,self._y] = 2
        self.screen(board)
        board.getcoltest(coltest)
