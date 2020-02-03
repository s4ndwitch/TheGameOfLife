import pygame
import sys
from ..Cell import *
from ..Wall import *


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
        self.check = False
        self.run()

    def update(self):
        for line in self.board:
            for cell in line:
                if isinstance(cell, Cell):
                    if cell.count != self.check:
                        continue
                    cell.update()
                    if cell.count:
                        cell.count = False
                    else:
                        cell.count = True
        if self.check:
            self.check = False
        else:
            self.check = True

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
        if mouse_pos[0] < len(self.board[0]) * self.cell_size and mouse_pos[1] < len(self.board) * self.cell_size:
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
                if self.board[line][cell] is None:
                    pygame.draw.rect(screen, (113, 113, 113),
                                     (cell * self.cell_size, line * self.cell_size, self.cell_size, self.cell_size), 1)
                if isinstance(self.board[line][cell], Cell):
                    if self.board[line][cell].dead_inside:
                        pygame.draw.rect(screen, (162, 168, 172),
                                         (cell * self.cell_size, line * self.cell_size, self.cell_size, self.cell_size))
                        continue
                    if self.board[line][cell].code.count(7) and not self.board[line][cell].code.count(8):
                        pygame.draw.rect(screen, (0, 255, 0),
                                         (cell * self.cell_size, line * self.cell_size, self.cell_size, self.cell_size))
                        continue
                    if self.board[line][cell].code.count(8):
                        pygame.draw.rect(screen, (255, 0, 0),
                                         (cell * self.cell_size, line * self.cell_size, self.cell_size, self.cell_size))
                        continue
                if isinstance(self.board[line][cell], Wall):
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (cell * self.cell_size, line * self.cell_size, self.cell_size, self.cell_size))

    def run(self):
        """
        Запуск отрисовки окна, мира.
        :return: ничего
        """
        pygame.init()
        tick_time = 1000
        started = True
        clock = pygame.time.Clock()
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
                            self.board[coords[1]][coords[0]] = Cell(self, coords[0], coords[1], self.check)
                    if event.button == 3:
                        coords = self.get_click(event.pos)
                        if isinstance(coords, list):
                            # self.board[coords[1]][coords[0]] = Wall()
                            coords = self.get_click(event.pos)
                            if isinstance(self.board[coords[1]][coords[0]], Cell):
                                print("Gen-code:\n" + ", ".join([str(i) for i in self.board[coords[1]][coords[0]].code]))
                                print("Energy:\n" + str(self.board[coords[1]][coords[0]].energy))
                    if event.button == 4:
                        tick_time += 1
                    if event.button == 5:
                        if tick_time > 1:
                            tick_time -= 1
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        if started:
                            started = False
                        else:
                            started = True
            if started:
                # clock.tick(tick_time)
                self.update()
            screen.fill((0, 0, 0))
            self.board_render(screen)
            pygame.display.flip()
