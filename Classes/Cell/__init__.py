class Cell:
    """
    Класс клетки -- живого существа, живущего по собственному генному коду.
    """
    def __init__(self, board):
        """
        Принимает на вход изначальную доску, чтобы взаимодейсвтует с миром.
        :param board: изначальная доска
        """
        self.board = board
        self.code = []  # TODO написать
        self.step = 0

    def move(self, direction):
        if direction == "UP":
            pass  # TODO
        if direction == "RIGHT":
            pass  # TODO
        if direction == "DOWN":
            pass  # TODO
        if direction == "LEFT":
            pass  # TODO

    def do(self, command):
        if command == "MOVE UP":
            self.move("UP")
        if command == "MOVE LEFT":
            self.move("LEFT")
        if command == "MOVE DOWN":
            self.move("DOWN")
        if command == "MOVE RIGHT":
            self.move("RIGHT")

    def get(self, num):
        if num == 1:
            return "MOVE UP"
        if num == 2:
            return "MOVE RIGHT"
        if num == 3:
            return "MOVE DOWN"
        if num == 4:
            return "MOVE LEFT"

    def update(self):
        self.do(self.get(self.code[self.step]))
        self.step = (self.step + 1) % len(self.code)
