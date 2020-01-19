import time


class Bullet():
    def __init__(self, din, board):
        self._x = din.retx() + 1
        self._y = din.rety() + 3
        self._visibility = True
        self._start = time.time()
        self.screen(board)

    def clear(self, board):
        self._visibility = False
        board.board[self._x, self._y] = " "

    def screen(self, board):
        board.board[self._x, self._y] = "✖"

    def forward(self, board):
        if time.time() - self._start > 5:
            self.clear(board)
        if not self._visibility:
            return
        self.clear(board)
        self._visibility = True
        if self._y > 390:
            self.clear(board)
            return
        self._y = self._y + 1
        self.screen(board)

    def rowcol(self):
        return self._x, self._y

    def isvisible(self):
        return self._visibility


class Snow(Bullet):
    def __init__(self, din, board):
        Bullet.__init__(self, din, board)
        self._x = din.retx() + 5
        self._y = din.rety() - 1
        self._visibility = True

    def collision(self,din):
        row = din.retx()
        col = din.rety()

    def forward(self, board):
        if time.time() - self._start > 5:
            self.clear(board)
        if not self._visibility:
            return
        self.clear(board)
        self._visibility = True
        if self._y > 390:
            self.clear(board)
            return
        self._y = self._y -1 
        self.screen(board)
