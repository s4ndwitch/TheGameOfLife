import pygame
import sys


class Board:
    """
    Класс доски. Этот класс включает в себя как мир, так и интерфейс.
    """
    def __init__(self, x, y, cell_size):
        """
        Инициирование класса доски. Создаёт поле и запускает графику.
        :param x: ширина поля
        :param y: высота поля
        :param cell_size: ширина клетки
        """
        self.board = [[None for _ in range(x)] for _ in range(y)]
        self.run(x, y, cell_size)

    def board_render(self, screen, cell_size):
        """
        Отрисовка поля.
        :param screen: экран, на котором происходит отрисовка
        :param cell_size: ширина клетки
        :return: ничего
        """
        for line in range(len(self.board)):
            for cell in range(len(self.board[line])):
                pygame.draw.rect(screen, (255, 255, 255), (cell * cell_size, line * cell_size, cell_size, cell_size), 1)

    def run(self, x, y, cell_size):
        """
        Запуск отрисовки окна, мира.
        :param x: ширина поля
        :param y: высота поля
        :param cell_size: ширина клетки
        :return: ничего
        """
        pygame.init()
        screen = pygame.display.set_mode((x * cell_size, y * cell_size))  # TODO раширять по мере необходимости

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.board_render(screen, cell_size)
            pygame.display.flip()
