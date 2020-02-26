import pygame
from ..Cell import *
from configparser import ConfigParser
from time import time


class Board:
    """
    Класс доски.
    """

    def __init__(self, config: ConfigParser):
        """
        Инициализация класса доски.
        :param config: файл конфигурации.
        """
        self.config = config  # Передача файла конфигурации для последующих обращений.
        self.y = int(config["BOARD"]["Y"])  # Количество линий клеток.
        self.x = int(config["BOARD"]["X"])  # Количество клеток в линии.
        self.cell_size = int(self.config["BOARD"]["CELL_SIZE"])  # Сторона квадрата.
        self.board = [[None for x in range(self.x)] for y in range(self.y)]  # Сама доска.
        self.season = "Summer"  # Время года на доске.
        self.check = True  # Переключатель для проверки совершённого клеткой хода.
        self.zone = [len(self.board) // 16 * i for i in range(17)]  # Зонирование доски.
        self.start = time()
        self.mutation_full_zone = True
        self.run()  # Переход на запуск окна.

    def give_energy(self, y: int) -> int:
        """
        Возвращает количество энергии клетке.
        :param y: положение клетки по высоте.
        :return: количество энергии
        """
        if self.season == "Summer":  # Случай с летом.
            for border in range(1, len(self.zone)):  # Перебор границ.
                if self.zone[border - 1] <= y <= self.zone[border] \
                        and 1 <= border <= 11:  # Если подходит.
                    return 11 - (border - 1)  # Возрващение велечины.
            return 0  # Если ничто не подошло.
        elif self.season == "Autumn":  # Осень.
            for border in range(1, len(self.zone)):  # Перебор границ.
                if self.zone[border - 1] <= y <= self.zone[border] \
                        and 1 <= border <= 10:  # Если подходит.
                    return 10 - (border - 1)  # Возрващение велечины.
            return 0  # Если ничто не подошло.
        elif self.season == "Winter":  # Зима.
            for border in range(1, len(self.zone)):  # Перебор границ.
                if self.zone[border - 1] <= y <= self.zone[border] \
                        and 1 <= border <= 9:  # Если подходит.
                    return 9 - (border - 1)  # Возрващение велечины.
            return 0  # Если ничто не подошло.
        elif self.season == "Spring":  # Весна.
            for border in range(1, len(self.zone)):  # Перебор границ.
                if self.zone[border - 1] <= y <= self.zone[border] \
                        and 1 <= border <= 10:  # Если подходит.
                    return 10 - (border - 1)  # Возрващение велечины.
            return 0  # Если ничто не подошло.

    def give_mineral(self, y: int) -> int:
        """
        Выдаёт клетке минералы, если она находится в нижних слоях.
        Кстати, эта функция не зависит от времени года
        По крайней мере пока что. (Не думаю, что буду доробатывать)
        :param y: положение клетки по высоте.
        :return: количество минералов
        """
        for border in range(len(self.zone) // 2, len(self.zone)):  # Перебор границ.
            if self.zone[border - 1] <= y <= self.zone[border] and self.zone[len(self.zone) // 2] <=\
                    self.zone[border] <= self.zone[-1]:  # Если подходит.
                return 1 if self.zone[border] in range(self.y // 2, self.y // 2 + self.y // 8)\
                    else 2 if self.zone[border] in range(
                    self.y // 2 + self.y // 8, self.y // 2 + self.y // 4)\
                    else 3  # Возрващение велечины.

    def render(self, screen: pygame.Surface) -> None:
        """
        Отрисовка изображения в окне.
        :param screen: окно приложения.
        :return: None
        """
        screen.fill((0, 0, 0))  # Заливка окна чёрным.
        for y in range(len(self.board)):  # Отсчёт по-вертикали.
            for x in range(len(self.board[y])):  # Отсчёт по-горизонтали.
                if self.board[y][x] is None:  # Пустая клетка.
                    pygame.draw.rect(screen, (113, 113, 113),
                                     (x * self.cell_size, y * self.cell_size,
                                      self.cell_size, self.cell_size), 1)  # Отрисовка квадрата.
                if isinstance(self.board[y][x], Cell):  # Если в клетке есть бот.
                    color = [0, 0, 0]  # Создание списка цветов.
                    color[0] = 205 if 28 in self.board[y][x].code or 29 in self.board[y][x].code or 49 in self.board[y][x].code else 0  # Наличие гена поедания.
                    color[1] = 205 if 25 in self.board[y][x].code else 0  # Наличие гена фотосинтеза.
                    color[2] = 255 if 33 in self.board[y][x].code else 0  # Наличие гена переработки.
                    pygame.draw.rect(screen, color,
                                     (x * self.cell_size, y * self.cell_size,
                                      self.cell_size, self.cell_size))  # Отрисовка бота.
                if isinstance(self.board[y][x], Organic):  # Если в клетке есть органика.
                    pygame.draw.rect(screen, (205, 205, 205),
                                     (x * self.cell_size, y * self.cell_size,
                                      self.cell_size, self.cell_size))  # Отрисовка органики.
        pygame.display.flip()  # Обновление кадра.

    def run(self) -> None:
        """
        Запуск отрисовки и обработки.
        :return: None
        """
        screen = pygame.display.set_mode((self.x * self.cell_size,
                                          self.y * self.cell_size))  # Окно приложения.
        run = True  # Переменная для плавного завершения программы.
        step = 0  # Переменная хода.
        while run:  # Запуск основного цикла игры.
            for event in pygame.event.get():  # Получение всех событий, которые будут происходить.
                if event.type == pygame.QUIT:  # Событие завершения.
                    run = False  # Объявление завершения циклов.
                if event.type == pygame.MOUSEBUTTONDOWN:  # Обработка нажатия клавиши мыши.
                    x = event.pos[0] // self.cell_size  # Определение X координаты щелчка.
                    y = event.pos[1] // self.cell_size  # Определение Y координаты щелчка.
                    if event.button == 1:  # Нажатие ЛКМ.
                        self.board[y][x] = Cell(self, x, y)  # Добавление клетки на доску.
                    if event.button == 3:  # Нажатие ПКМ.
                        print("\n".join([str(self.board[y][x].energy), " ".join(
                            [str(i) for i in self.board[y][x].code])]) if isinstance(
                            self.board[y][x], Cell) else "")
                        if isinstance(self.board[y][x], Cell):
                            print(f"Минеравлов: {self.board[y][x].mineral}")
                            print("Умеет:")
                            able, was = {
                                10: "Переробатывать органику",
                                16: "Отпочковывать потомков",
                                23: "Поворачиваться (Менять направление)",
                                24: "Поворачиваться (Абссолютно, независимо от ген кода)",
                                25: "Фотосинтезировать",
                                26: "Передвигаться",
                                27: "Передвигаться (Абссолютно, независимо от ген кода)",
                                28: "Есть другие клетки",
                                29: "Есть другие клетки (Абссолютно, независимо от ген кода)",
                                30: "Команда \"Посмотреть\"",
                                31: "Команда \"Посмотреть по абссолютному направлению\"",
                                33: "Хемосинтез",
                                36: "Команда \"Сколько у меня минералов?\"",
                                38: "Команда \"Сколько у меня энергии?\"",
                                49: "Есть другие клетки (Абссолютно, независимо от ген кода)",
                            }, []
                            for i in self.board[y][x].code:
                                if i in able and i not in was:
                                    print(able[i])
                                    was += [i]
                    if event.button == 2:
                        if isinstance(self.board[y][x], Cell):
                            for i in range(len(self.board[y][x].code)):
                                if self.board[y][x].code[i] == 25:
                                    self.board[y][x].code[i] = 26
            self.update()  # Обновление доски.
            self.render(screen)  # Отрисовка изображения и смена кадра.
            step += 1  # Добавление хода.
            if step % 183 == 0:  # Когда проходит 183 хода.
                self.season = {  # Начало словаря с записанными случаями смены.
                    "Summer": "Autumn",  # Лето сменяется осенью.
                    "Autumn": "Winter",  # Осень сменяется зиомй.
                    "Winter": "Spring",  # Зима сменяется весной.
                    "Spring": "Summer"  # Весна сменяется летом.
                }.get(self.season)  # Смена времени года.
        pygame.quit()  # Выход из приложения.

    def update(self) -> None:
        """
        Парсинг ботов.
        :return: None
        """
        for line in self.board:  # Перебор строк.
            for cell in line:  # Перебор клеток в строке.
                if isinstance(cell, Cell) or isinstance(cell, Organic):  # Если клетка или органика.
                    if self.check != cell.check:  # Проверка на совершённость хода.
                        cell.update()  # Обновление клетки.
                        cell.check = False if cell.check else True  # Переключение состояния хода.
        self.check = False if self.check else True  # Обновление состояния хода.
