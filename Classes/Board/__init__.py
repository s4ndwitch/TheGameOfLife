import pygame
import sys
from ..Cell import *


class Board:
    """
    Класс доски. Этот класс включает в себя как мир, так и интерфейс.
    """

    def __init__(self, x, y, cell_size):
        """
        Инициирование класса доски. Создаёт поле, кооординаты х, у и ширины поля для доступа во всём классе и запускает графику.
        :param x: ширина поля
        :param y: высота поля
        :param cell_size: ширина клетки
        """
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.board = [[None for _ in range(x)] for _ in range(y)]
        self.run()

    def search_on_board(self, mouse_pos):
        """
        Ищет, какая клетка была нажата на поле.
        :param mouse_pos: координаты мыши в момент клика
        :return: координаты клетки в форматке list((x; y))
        """
        for line in range(len(self.board)):
            for cell in range(len(self.board[line])):
                if cell * self.cell_size <= mouse_pos[0] <= cell * self.cell_size + self.cell_size and \
                        line * self.cell_size <= mouse_pos[1] <= line * self.cell_size + self.cell_size:
                    return [cell, line]

    def search_in_gui(self, mouse_pos):
        """
        Ищет, какая кнопка была нажата.
        :param mouse_pos: координаты мыши в момент клика
        :return: номер кнопки в формате int
        """
        # TODO

    def get_click(self, mouse_pos):
        """
        Функция обработки нажатия.
        :param mouse_pos: координаты мыши в момент клика
        :return: номер кнопки или координаты клетки в формате list((x; y))
        """
        if mouse_pos[0] < len(self.board) * self.cell_size and mouse_pos[1] < len(self.board[0]) * self.cell_size:
            return self.search_on_board(mouse_pos)
        else:
            return self.search_in_gui(mouse_pos)

    def board_render(self, screen):
        """
        Отрисовка поля.
        :param screen: экран, на котором происходит отрисовка
        :return: ничего
        """
        for line in range(len(self.board)):
            for cell in range(len(self.board[line])):
                pygame.draw.rect(screen, (255, 255, 255),
                                 (cell * self.cell_size, line * self.cell_size, self.cell_size, self.cell_size), 1)

    def run(self):
        """
        Запуск отрисовки окна, мира.
        :return: ничего
        """
        pygame.init()
        screen = pygame.display.set_mode(
            (self.x * self.cell_size, self.y * self.cell_size))  # TODO раширять по мере необходимости

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        coords = self.get_click(event.pos)
                        if isinstance(coords, list):
                            self.board[coords[0]][coords[1]] = Cell(self)
            self.board_render(screen)
            pygame.display.flip()
