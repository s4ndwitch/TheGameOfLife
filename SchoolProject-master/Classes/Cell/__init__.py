from random import randint, choice


class Cell:
    """
    Класс клетки -- живого существа, живущего по собственному генному коду.
    """

    def __init__(self, board, x, y, count):
        """
        Принимает на вход изначальную доску, чтобы взаимодейсвтует с миром.
        :param board: изначальная доска
        """
        self.step = 0
        self.dead_inside = False
        self.x = x
        self.y = y
        self.board = board
        self.code = [7] * 15
        self.age = 0
        self.count = count
        self.energy = 255

    def move(self, direction):
        if direction == "UP":
            if self.y > 0:
                if self.board.board[self.y - 1][self.x] is None:
                    self.board.board[self.y - 1][self.x] = self
                    self.board.board[self.y][self.x] = None
                    self.y -= 1
        if direction == "RIGHT":
            if self.x < len(self.board.board[0]) - 1:
                if self.board.board[self.y][self.x + 1] is None:
                    self.board.board[self.y][self.x + 1] = self
                    self.board.board[self.y][self.x] = None
                    self.x += 1
        if direction == "DOWN":
            if self.y < len(self.board.board) - 1:
                if self.board.board[self.y + 1][self.x] is None:
                    self.board.board[self.y + 1][self.x] = self
                    self.board.board[self.y][self.x] = None
                    self.y += 1
        if direction == "LEFT":
            if self.x > 0:
                if self.board.board[self.y][self.x - 1] is None:
                    self.board.board[self.y][self.x - 1] = self
                    self.board.board[self.y][self.x] = None
                    self.x -= 1
        if direction == "TLEFT":
            for i in range(len(self.code)):
                if self.code[i] in {1, 2, 3, 4}:
                    if self.code[i] != 1:
                        self.code[i] -= 1
                    else:
                        self.code[i] = 4
        if direction == "TRIGHT":
            for i in range(len(self.code)):
                if self.code[i] in {1, 2, 3, 4}:
                    if self.code[i] != 4:
                        self.code[i] += 1
                    else:
                        self.code[i] = 1

    def do(self, command):
        if command == "MOVE UP":
            self.move("UP")
        if command == "MOVE LEFT":
            self.move("LEFT")
        if command == "MOVE DOWN":
            self.move("DOWN")
        if command == "MOVE RIGHT":
            self.move("RIGHT")
        if command == "TURN TO LEFT":
            self.move("TLEFT")
        if command == "TURN TO RIGHT":
            self.move("TRIGHT")
        if command == "PHOTOSYNTHESIS":
            self.photosynthesis()
        if command == "EAT":
            self.eat()

    def get(self, num):
        if num == 1:
            return "MOVE UP"
        if num == 2:
            return "MOVE RIGHT"
        if num == 3:
            return "MOVE DOWN"
        if num == 4:
            return "MOVE LEFT"
        if num == 5:
            return "TURN TO LEFT"
        if num == 6:
            return "TURN TO RIGHT"
        if num == 7:
            return "PHOTOSYNTHESIS"
        if num == 8:
            return "EAT"

    def mutize(self):
        for _ in range(4):
            self.code[randint(0, len(self.code) - 1)] = randint(1, 8)

    def double(self):
        direction = randint(1, 4)
        if direction == 1:
            if self.y > 0:
                if self.board.board[self.y - 1][self.x] is None:
                    self.board.board[self.y - 1][self.x] = Cell(self.board, self.x, self.y - 1, self.count)
                    self.board.board[self.y - 1][self.x].mutize()
                    self.board.board[self.y - 1][self.x].energy = 50
                    self.board.board[self.y][self.x].energy = 50
        if direction == 2:
            if self.x < len(self.board.board[0]) - 1:
                if self.board.board[self.y][self.x + 1] is None:
                    self.board.board[self.y][self.x + 1] = Cell(self.board, self.x + 1, self.y, self.count)
                    self.board.board[self.y][self.x + 1].mutize()
                    self.board.board[self.y][self.x + 1].energy = 50
                    self.board.board[self.y][self.x].energy = 50
        if direction == 3:
            if self.y < len(self.board.board) - 1:
                if self.board.board[self.y + 1][self.x] is None:
                    self.board.board[self.y + 1][self.x] = Cell(self.board, self.x, self.y + 1, self.count)
                    self.board.board[self.y + 1][self.x].mutize()
                    self.board.board[self.y + 1][self.x].energy = 50
                    self.board.board[self.y][self.x].energy = 50
        if direction == 4:
            if self.x > 0:
                if self.board.board[self.y][self.x - 1] is None:
                    self.board.board[self.y][self.x - 1] = Cell(self.board, self.x - 1, self.y, self.count)
                    self.board.board[self.y][self.x - 1].mutize()
                    self.board.board[self.y][self.x - 1].energy = 50
                    self.board.board[self.y][self.x].energy = 50

    def photosynthesis(self):
        self.energy += 15

    def DIE(self):
        self.dead_inside = True

    def eat(self):
        directions = ["UP", "RIGHT", "DOWN", "LEFT"]
        for _ in range(4):
            direction = choice(directions)
            ate = False
            if direction == "UP":
                if self.y > 0:
                    if isinstance(self.board.board[self.y - 1][self.x], Cell):
                        if not self.board.board[self.y - 1][self.x].dead_inside:
                            self.energy += self.board.board[self.y - 1][self.x].energy
                        else:
                            self.energy += 25
                        self.board.board[self.y - 1][self.x] = None
                        ate = True
            if direction == "RIGHT":
                if self.x < len(self.board.board[0]) - 1:
                    if isinstance(self.board.board[self.y][self.x + 1], Cell):
                        if not self.board.board[self.y][self.x + 1].dead_inside:
                            self.energy += self.board.board[self.y][self.x + 1].energy
                        else:
                            self.energy += 25
                        self.board.board[self.y][self.x + 1] = None
                        ate = True
            if direction == "DOWN":
                if self.y < len(self.board.board) - 1:
                    if isinstance(self.board.board[self.y + 1][self.x], Cell):
                        if not self.board.board[self.y + 1][self.x].dead_inside:
                            self.energy += self.board.board[self.y + 1][self.x].energy
                        else:
                            self.energy += 25
                        self.board.board[self.y + 1][self.x] = None
                        ate = True
            if direction == "LEFT":
                if self.x > 0:
                    if isinstance(self.board.board[self.y][self.x - 1], Cell):
                        if not self.board.board[self.y][self.x - 1].dead_inside:
                            self.energy += self.board.board[self.y][self.x - 1].energy
                        else:
                            self.energy += 25
                        self.board.board[self.y][self.x - 1] = None
                        ate = True
            if not ate:
                del directions[directions.index(direction)]

    def update(self):
        if self.age == 1500 or (self.age == 300 and 8 in self.code):
            self.DIE()
        if not self.dead_inside:
            if self.energy >= 500 and 8 not in self.code:
                self.double()
            elif self.energy >= 2000 and 8 in self.code:
                self.double()
            self.energy -= 10
            self.do(self.get(self.code[self.step]))
            self.step = (self.step + 1) % len(self.code)
            if self.energy <= 0:
                self.DIE()
        self.age += 1
