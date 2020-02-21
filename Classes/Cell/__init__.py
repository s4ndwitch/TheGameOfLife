from ..Wall import *
from ..Organic import *
from random import randint


class Cell:
    """
    Класс клетки -- живого существа, живущего по собственному генному коду.
    """

    def __init__(self, board, x, y, count, world):
        """
        Принимает на вход изначальную доску, чтобы взаимодейсвтует с миром.
        :param board: изначальная доска
        """
        self.step = 0
        self.dead_inside = False
        self.x = x
        self.y = y
        self.board = board
        self.code = [25 for _ in range(64)]
        print(self.code)
        self.count = count
        self.energy = 50
        self.world = world

    def photo(self):
        # TODO Времена года и положение по оси y
        self.energy += 5
        self.step += 1

    def double(self):
        direction = 5
        if direction == 1:
            if self.y > 0:
                if self.board[self.y - 1][self.x] is None:
                    self.board[self.y - 1][self.x] = Cell(self.board, self.x, self.y - 1, self.count, self)
                    self.board[self.y - 1][self.x].code = self.code.copy()
                    self.board[self.y - 1][self.x].energy = 50
                    self.board[self.y][self.x].energy = 50
        if direction == 2:
            if self.x < len(self.board[0]) - 1:
                if self.board[self.y][self.x + 1] is None:
                    self.board[self.y][self.x + 1] = Cell(self.board, self.x + 1, self.y, self.count, self)
                    self.board[self.y][self.x + 1].code = self.code.copy()
                    self.board[self.y][self.x + 1].energy = 50
                    self.board[self.y][self.x].energy = 50
        if direction == 3:
            if self.y < len(self.board) - 1:
                if self.board[self.y + 1][self.x] is None:
                    self.board[self.y + 1][self.x] = Cell(self.board, self.x, self.y + 1, self.count, self)
                    self.board[self.y + 1][self.x].code = self.code.copy()
                    self.board[self.y + 1][self.x].energy = 50
                    self.board[self.y][self.x].energy = 50
        if direction == 4:
            if self.x > 0:
                if self.board[self.y][self.x - 1] is None:
                    self.board[self.y][self.x - 1] = Cell(self.board, self.x - 1, self.y, self.count, self)
                    self.board[self.y][self.x - 1].code = self.code.copy()
                    self.board[self.y][self.x - 1].energy = 50
                    self.board[self.y][self.x].energy = 50
        if direction == 5:
            if self.x - 1 > 0 and self.y - 1 < len(self.board) - 1:
                if self.board[self.y - 1][self.x - 1] is None:
                    self.board[self.y - 1][self.x - 1] = Cell(self.board, self.x - 1, self.y - 1, self.count, self)
                    self.board[self.y - 1][self.x - 1].code = self.code.copy()
                    self.board[self.y - 1][self.x - 1].energy = 50
                    self.board[self.y - 1][self.x - 1] = 50

    def check_direction(self, num):
        if num == 0:
            return self.y > 0 and self.x < len(self.board[0]) - 1
        if num == 1:
            return self.x < len(self.board[0]) - 1
        if num == 2:
            return self.y < len(self.board) - 1 and self.x < len(self.board[0]) - 1
        if num == 3:
            return self.y < len(self.board) - 1
        if num == 4:
            return self.y < len(self.board) - 1 and self.x > 0
        if num == 5:
            return self.x > 0
        if num == 6:
            return self.y > 0 and self. x > 0
        if num == 7:
            return self.y > 0

    def return_direction(self, num):
        if num == 0:
            return self.board[self.y - 1][self.x + 1]
        if num == 1:
            return self.board[self.y][self.x + 1]
        if num == 2:
            return self.board[self.y + 1][self.x + 1]
        if num == 3:
            return self.board[self.y + 1][self.x]
        if num == 4:
            return self.board[self.y + 1][self.x - 1]
        if num == 5:
            return self.board[self.y][self.x - 1]
        if num == 6:
            return self.board[self.y - 1][self.x - 1]
        if num == 7:
            return self.board[self.y - 1][self.x]

    def move(self, num):
        if num == 0:
            if self.check_direction(num) and self.board[self.y - 1][self.x + 1] is None:
                self.board[self.y - 1][self.x + 1] = self
                self.board[self.y][self.x] = None
                self.x += 1
                self.y -= 1
        if num == 1:
            if self.check_direction(num) and self.board[self.y][self.x + 1] is None:
                self.board[self.y][self.x + 1] = self
                self.board[self.y][self.x] = None
                self.x += 1
        if num == 2:
            if self.check_direction(num) and self.board[self.y + 1][self.x + 1] is None:
                self.board[self.y + 1][self.x + 1] = self
                self.board[self.y][self.x] = None
                self.y += 1
                self.x += 1
        if num == 3:
            if self.check_direction(num) and self.board[self.y + 1][self.x] is None:
                self.board[self.y + 1][self.x] = self
                self.board[self.y][self.x] = None
                self.y += 1
        if num == 4:
            if self.check_direction(num) and self.board[self.y + 1][self.x - 1] is None:
                self.board[self.y + 1][self.x - 1] = self
                self.board[self.y][self.x] = None
                self.y += 1
                self.x -= 1
        if num == 5:
            if self.check_direction(num) and self.board[self.y][self.x - 1] is None:
                self.board[self.y][self.x - 1] = self
                self.board[self.y][self.x] = None
                self.x -= 1
        if num == 6:
            if self.check_direction(num) and self.board[self.y - 1][self.x - 1] is None:
                self.board[self.y - 1][self.x - 1] = self
                self.board[self.y][self.x] = None
                self.x -= 1
                self.y -= 1
        if num == 7:
            if self.check_direction(num) and self.board[self.y - 1][self.x] is None:
                self.board[self.y - 1][self.x] = self
                self.board[self.y][self.x] = None
                self.y -= 1
        if self.check_direction(num):
            if self.return_direction(num) is None:
                self.step = (self.step + self.code[(self.step + 2) % len(self.code)]) % len(self.code)
            if isinstance(type(Wall), type(self.return_direction(num))):
                self.step = (self.step + self.code[(self.step + 3) % len(self.code)]) % len(self.code)
            if isinstance(type(Organic), type(self.return_direction(num))):
                self.step = (self.step + self.code[(self.step + 4) % len(self.code)]) % len(self.code)
            if isinstance(type(Cell), type(self.return_direction(num))):
                if self.is_similar(self.return_direction(num)):
                    self.step = (self.step + self.code[(self.step + 6) % len(self.code)]) % len(self.code)
                else:
                    self.step = (self.step + self.code[(self.step + 5) % len(self.code)]) % len(self.code)

    def is_similar(self, cell):
        return self.code == cell.code

    def do(self, step):
        if self.code[step] == 25:
            self.photo()
        elif self.code[step] == 26:
            self.move(self.code[(step + 1) % len(self.code)] % 8)
            self.step += 1
        elif self.code[step] == 38:
            self.step += self.code[step + 2] if self.code[step + 1] * 15 <= self.energy else self.code[step + 3]
            self.step += 1
        else:
            self.step += self.code[step]

    def update(self):
        self.energy -= 1
        if self.energy == 0:
            self.dead_inside = True
        if self.energy >= 100:
            self.double()
        self.step %= 63
        self.do(self.step)
