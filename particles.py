
class bullet():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def clear(self, board):
        board.board[self.x, self.y] = " "

    def screen(self, board):
        board.board[self.x, self.y] = ">"

    def forward(self, board):
        self.clear(board)
        self.y = self.y + 1
        self.screen(board)
