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
        self.code = [7 for _ in range(9)]
        self.age = 0
        self.count = count
        self.energy = 50
        self.itera = 1

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
            self.find()

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
        self.code[randint(0, len(self.code) - 1)] = randint(1, 8)
        if 8 in self.code:
            for _ in range(2):
                try:
                    self.code[self.code.index(7)] = 8
                except Exception as error:
                    print(error, "\r")

    def double(self):
        direction = randint(1, 4)
        if direction == 1:
            if self.y > 0:
                if self.board.board[self.y - 1][self.x] is None:
                    self.board.board[self.y - 1][self.x] = Cell(self.board, self.x, self.y - 1,
                                                                self.count)
                    self.board.board[self.y - 1][self.x].itera = (self.board.board[self.y][
                                                                      self.x].itera + 1) % 4
                    if self.board.board[self.y - 1][self.x].itera == 0:
                        self.board.board[self.y - 1][self.x].mutize()
                    self.board.board[self.y - 1][self.x].energy = 50
                    self.board.board[self.y][self.x].energy = 50
        if direction == 2:
            if self.x < len(self.board.board[0]) - 1:
                if self.board.board[self.y][self.x + 1] is None:
                    self.board.board[self.y][self.x + 1] = Cell(self.board, self.x + 1, self.y,
                                                                self.count)
                    self.board.board[self.y][self.x + 1].itera = (self.board.board[self.y][
                                                                      self.x].itera + 1) % 4
                    if self.board.board[self.y][self.x + 1].itera == 0:
                        self.board.board[self.y][self.x + 1].mutize()
                    self.board.board[self.y][self.x + 1].energy = 50
                    self.board.board[self.y][self.x].energy = 50
        if direction == 3:
            if self.y < len(self.board.board) - 1:
                if self.board.board[self.y + 1][self.x] is None:
                    self.board.board[self.y + 1][self.x] = Cell(self.board, self.x, self.y + 1,
                                                                self.count)
                    self.board.board[self.y + 1][self.x].itera = (self.board.board[self.y][
                                                                      self.x].itera + 1) % 4
                    if self.board.board[self.y + 1][self.x].itera == 0:
                        self.board.board[self.y + 1][self.x].mutize()
                    self.board.board[self.y + 1][self.x].energy = 50
                    self.board.board[self.y][self.x].energy = 50
        if direction == 4:
            if self.x > 0:
                if self.board.board[self.y][self.x - 1] is None:
                    self.board.board[self.y][self.x - 1] = Cell(self.board, self.x - 1, self.y,
                                                                self.count)
                    self.board.board[self.y][self.x - 1].itera = (self.board.board[self.y][
                                                                      self.x].itera + 1) % 4
                    if self.board.board[self.y][self.x - 1].itera == 0:
                        self.board.board[self.y][self.x - 1].mutize()
                    self.board.board[self.y][self.x - 1].energy = 50
                    self.board.board[self.y][self.x].energy = 50

    def find(self):
        cells = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    continue
                if self.y + i >= len(self.board.board) or self.y + i < 0 or self.x + j < 0 or self.x + j >= len(self.board.board[0]):
                    continue
                if isinstance(self.board.board[self.y + i][self.x + j], Cell):
                    cells += [[i, j]]
        for pair in cells:
            if pair[0] == 0 or pair[1] == 0:
                self.eat()
            if abs(pair[0]) == 1 and abs(pair[1]) == 1:
                if pair[0] == -1:
                    if pair[1] == -1:
                        self.move("LEFT")
                        self.eat()
                    if pair[1] == 1:
                        self.move("RIGHT")
                        self.eat()
                if pair[0] == 1:
                    self.move("DOWN")
                    self.eat()
            if pair[0] == -2:
                if pair[1] < 0:
                    self.move("UP")
                    self.move("LEFT")
                    cells_in = []
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            if k == 0 and l == 0:
                                continue
                            if self.y + k >= len(
                                    self.board.board) or self.y + k < 0 or self.x + l < 0 or self.x + k >= len(
                                    self.board.board[0]):
                                continue
                            if isinstance(self.board.board[self.y + k][self.x + l], Cell):
                                cells_in += [[k, l]]
                    for pair in cells_in:
                        if pair[0] == 0 or pair[1] == 0:
                            self.eat()
                        if abs(pair[0]) == 1 and abs(pair[1]) == 1:
                            if pair[0] == -1:
                                if pair[1] == -1:
                                    self.move("LEFT")
                                    self.eat()
                                if pair[1] == 1:
                                    self.move("RIGHT")
                                    self.eat()
                            if pair[0] == 1:
                                self.move("DOWN")
                                self.eat()
                if pair[1] > 0:
                    self.move("UP")
                    self.move("RIGHT")
                    cells_in = []
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            if k == 0 and l == 0:
                                continue
                            if self.y + k >= len(
                                    self.board.board) or self.y + k < 0 or self.x + l < 0 or self.x + k >= len(
                                self.board.board[0]):
                                continue
                            if isinstance(self.board.board[self.y + k][self.x + l], Cell):
                                cells_in += [[k, l]]
                    for pair in cells_in:
                        if pair[0] == 0 or pair[1] == 0:
                            self.eat()
                        if abs(pair[0]) == 1 and abs(pair[1]) == 1:
                            if pair[0] == -1:
                                if pair[1] == -1:
                                    self.move("LEFT")
                                    self.eat()
                                if pair[1] == 1:
                                    self.move("RIGHT")
                                    self.eat()
                            if pair[0] == 1:
                                self.move("DOWN")
                                self.eat()
            if pair[0] == 2:
                if pair[1] < 0:
                    self.move("DOWN")
                    self.move("LEFT")
                    cells_in = []
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            if k == 0 and l == 0:
                                continue
                            if self.y + k >= len(
                                    self.board.board) or self.y + k < 0 or self.x + l < 0 or self.x + k >= len(
                                self.board.board[0]):
                                continue
                            if isinstance(self.board.board[self.y + k][self.x + l], Cell):
                                cells_in += [[k, l]]
                    for pair in cells_in:
                        if pair[0] == 0 or pair[1] == 0:
                            self.eat()
                        if abs(pair[0]) == 1 and abs(pair[1]) == 1:
                            if pair[0] == -1:
                                if pair[1] == -1:
                                    self.move("LEFT")
                                    self.eat()
                                if pair[1] == 1:
                                    self.move("RIGHT")
                                    self.eat()
                            if pair[0] == 1:
                                self.move("DOWN")
                                self.eat()
                if pair[1] > 0:
                    self.move("DOWN")
                    self.move("RIGHT")
                    cells_in = []
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            if k == 0 and l == 0:
                                continue
                            if self.y + k >= len(
                                    self.board.board) or self.y + k < 0 or self.x + l < 0 or self.x + k >= len(
                                self.board.board[0]):
                                continue
                            if isinstance(self.board.board[self.y + k][self.x + l], Cell):
                                cells_in += [[k, l]]
                    for pair in cells_in:
                        if pair[0] == 0 or pair[1] == 0:
                            self.eat()
                        if abs(pair[0]) == 1 and abs(pair[1]) == 1:
                            if pair[0] == -1:
                                if pair[1] == -1:
                                    self.move("LEFT")
                                    self.eat()
                                if pair[1] == 1:
                                    self.move("RIGHT")
                                    self.eat()
                            if pair[0] == 1:
                                self.move("DOWN")
                                self.eat()

    def photosynthesis(self):
        if self.y < len(self.board.board) // 2:
            self.energy += 10
        else:
            self.energy += 6

    def DIE(self):
        self.dead_inside = True

    def is_similar(self, another):
        count = sum([1 for i in range(len(self.code)) if sorted(self.code)[i] == sorted(another.code)[i]])
        return True if count >= len(self.code) / 5 * 4 else False

    def eat(self):
        directions = ["UP", "RIGHT", "DOWN", "LEFT"]
        for _ in range(4):
            direction = choice(directions)
            if direction == "UP":
                if self.y > 0:
                    if isinstance(self.board.board[self.y - 1][self.x], Cell):
                        if self.board.board[self.y - 1][self.x].dead_inside:
                            self.energy += 25
                            self.board.board[self.y - 1][self.x] = None
                            break
                        else:
                            if not self.is_similar(self.board.board[self.y - 1][self.x]):
                                self.energy += 45
                                self.board.board[self.y - 1][self.x] = None
                                break
            if direction == "RIGHT":
                if self.x < len(self.board.board[0]) - 1:
                    if isinstance(self.board.board[self.y][self.x + 1], Cell):
                        if self.board.board[self.y][self.x + 1].dead_inside:
                            self.energy += 25
                            self.board.board[self.y][self.x + 1] = None
                            break
                        else:
                            if not self.is_similar(self.board.board[self.y][self.x + 1]):
                                self.energy += 45
                                self.board.board[self.y][self.x + 1] = None
                                break
            if direction == "DOWN":
                if self.y < len(self.board.board) - 1:
                    if isinstance(self.board.board[self.y + 1][self.x], Cell):
                        if self.board.board[self.y + 1][self.x].dead_inside:
                            self.energy += 25
                            self.board.board[self.y + 1][self.x] = None
                            break
                        else:
                            if not self.is_similar(self.board.board[self.y + 1][self.x]):
                                self.energy += 45
                                self.board.board[self.y + 1][self.x] = None
                                break
            if direction == "LEFT":
                if self.x > 0:
                    if isinstance(self.board.board[self.y][self.x - 1], Cell):
                        if self.board.board[self.y][self.x - 1].dead_inside:
                            self.energy += 25
                            self.board.board[self.y][self.x - 1] = None
                            break
                        else:
                            if not self.is_similar(self.board.board[self.y][self.x - 1]):
                                self.energy += 45
                                self.board.board[self.y][self.x - 1] = None
                                break
            del directions[directions.index(direction)]

    def update(self):
        if self.code.count(7) > len(self.code) // 2:
            if self.age == 500:
                self.DIE()
            if self.age == 600:
                self.board.board[self.y][self.x] = None
        if self.code.count(7) < len(self.code) // 2:
            if self.age == 60:
                self.DIE()
            if self.age == 150:
                self.board.board[self.y][self.x] = None
        if not self.dead_inside:
            if self.energy >= 200:
                self.double()
            self.energy -= 5
            self.do(self.get(self.code[self.step]))
            self.step = (self.step + 1) % len(self.code)
            if self.energy <= 0:
                self.DIE()
        else:
            if self.y < len(self.board.board) - 1:
                if self.board.board[self.y + 1][self.x] is None:
                    self.move("DOWN")
        self.age += 1
