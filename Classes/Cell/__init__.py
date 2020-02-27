from ..Organic import *
from random import choice, randint
from ..Wall import *
from time import time


class Cell:
    """
    Класс клетки.
    """

    def __init__(self, world, x: int, y: int):
        """
        Инициализация клетки.
        :param world: парамент родительского мира.
        :param x: положение клетки по ширине.
        :param y: положение клетки по высоте.
        """
        self.code = [25] * 64  # Генетический код бота.
        self.step = 0  # Курсор команды, которая должна выполниться при следующем обновлении.
        self.energy = 300  # Количесвто энергии бота.
        self.world = world  # Родительская доска.
        self.x = x  # Положение клетки по ширине.
        self.y = y  # Положение клетки по высоте.
        self.check = True  # Переключатель для проверки совершения хода.
        self.board = world.board  # Выгрузка доски для упрощённого обращения к ней.
        self.mineral = 0  # Количество минералов у клетки.
        self.directions = {  # Список направлений, изменяющийся при повороте.
            0: "DOWN",  # Снизу.
            1: "DOWN-LEFT",  # Снизу, слева.
            2: "LEFT",  # Слева.
            3: "LEFT-UP",  # Сверху, слева.
            4: "UP",  # Верх.
            5: "UP-RIGHT",  # Верх, справа.
            6: "RIGHT",  # Справа.
            7: "RIGHT-DOWN",  # Снизу, справа.
        }

    def change_direction(self, num: int) -> None:
        """
        Поворот на определённое количество единиц.
        :param num: количество поворотов
        :return: None
        """
        directions = [i for i in self.directions.values()]  # Получение списка направлений.
        for _ in range(num):  # Перебор количества поворотов.
            directions.insert(0, directions[-1])  # Перезапись последнего значения в первое.
            del directions[-1]  # Удаление старого значения.
        self.directions = {i: directions[i] for i in range(8)}  # Создание новых направлений.

    def change_direction_abs(self, direction: int) -> None:
        """
        поворот клекти в абсолютном направлении.
        :param direction: направление
        :return: None
        """
        directions = [i for i in self.directions.values()]  # Получение списка направлений.
        while directions.index("UP") != direction:  # Пока не будет достигнут результат.
            directions.insert(0, directions[-1])  # Поворот.
            del directions[-1]  # Удаление старого значения.
        self.directions = {i: directions[i] for i in range(8)}  # Создание новых направлений.

    def check_direction(self, direction: int) -> object:
        """
        Возвращает то, что было в определённой стороне от клетки.
        :param direction: направление
        :return: объект со стороны
        """
        direction = self.directions[direction]  # Возвращение направления из числа.
        if self.check_list(direction) is not False:  # Проверка возможности обратиться к списку.
            if direction == "UP":  # Направление вверх.
                return self.board[self.y - 1][self.x]
            if direction == "UP-RIGHT":  # Направление вправо и вверх.
                return self.board[self.y - 1][self.x + 1]
            if direction == "RIGHT":  # Направление вправо.
                return self.board[self.y][self.x + 1]
            if direction == "RIGHT-DOWN":  # Направление вниз и вправо.
                return self.board[self.y + 1][self.x + 1]
            if direction == "DOWN":  # Направление вниз.
                return self.board[self.y + 1][self.x]
            if direction == "DOWN-LEFT":  # Направление вниз и влево.
                return self.board[self.y + 1][self.x - 1]
            if direction == "LEFT":  # Направление влево.
                return self.board[self.y][self.x - 1]
            if direction == "LEFT-UP":  # Направление вверх и влево.
                return self.board[self.y - 1][self.x - 1]
        return False  # Невозможно получить доступ к списку.

    def check_list(self, direction: str) -> bool:
        """
        Проверка, если есть возможность работать со списком в определённом направлении.
        :param direction: направление
        :return: True или False
        """
        if direction == "UP":  # Направление вверх.
            return True if self.y > 0 else False  # Не начало списка строк.
        if direction == "UP-RIGHT":  # Направление вверх и врпаво.
            return True if self.y > 0 and self.x < len(
                self.board[self.y]) - 1 else False  # Не начало списка строк и не конец в ширину.
        if direction == "RIGHT":  # Направление вправо.
            return True if self.x < len(self.board[self.y]) - 1 else False  # Если не конец строки.
        if direction == "RIGHT-DOWN":  # Направление вправо и вниз.
            return True if self.x < len(self.board[self.y]) - 1 and self.y < len(
                self.board) - 1 else False  # Если не конец списка строк и самих строк.
        if direction == "DOWN":  # Направление вниз.
            return True if self.y < len(self.board) - 1 else False  # Если не конец списка строк.
        if direction == "DOWN-LEFT":  # Направление вниз и влево.
            return True if self.y < len(
                self.board) - 1 and self.x > 0 else False  # Не конец списка строк и не начало онных.
        if direction == "LEFT":  # Направление влево.
            return True if self.x > 0 else False
        if direction == "LEFT-UP":  # Направление влево и вверх.
            return True if self.x > 0 and self.y > 0 else False  # Не начало списка строк и их самих.

    def do(self, step: int) -> None:
        """
        Функция исполнения команды генетического алгоритма.
        :return: None
        """
        if self.code[step] == 10:  # Ген переработки органики.
            self.eat_organic()  # Инициализация выполнения.
            self.step = (self.step + 1) % len(self.code)  # Смещение на 1 ген.
        elif self.code[step] == 16:  # Ген принудительного размножения.
            self.double()  # Размножение.
            self.step = (self.step + 1) % len(self.code)  # Шаг на один.
        elif self.code[step] == 23:  # Ген смены направления.
            self.change_direction(self.code[(self.step + 1) % len(self.code)] % 8)  # Выполнение.
            self.step = (self.step + 2) % len(self.code)  # Смещение курсора на 2.
            self.do(self.step)  # Выполнение последующего дейсвтия.
        elif self.code[step] == 24:  # Поворот по абсолютному направлению.
            self.change_direction_abs(self.code[(self.step + 1) % len(self.code)] % 8)  # Выполнение.
            self.step = (self.step + 2) % len(self.code)  # Смещение курсора на 2.
            self.do(self.step)  # Выполнение последующего дейсвтия.
        elif self.code[step] == 25:  # Ген фотосинтеза.
            result = self.world.give_energy(self.y)  # Обращение к доске за энергией.
            if result == 0:  # Проверка, если энергии не получено.
                self.energy -= 1  # Простаивание.
            else:  # Если есть результат.
                self.energy += int(result * (1 + self.mineral // 100))  # Присваивание энергии.
            self.step = (self.step + 1) % len(self.code)  # Переход на один.
        elif self.code[step] == 26:  # Ген передвижения.
            self.move(self.code[(self.step + 1) % len(self.code)] % 8)  # Перемещение.
        elif self.code[step] == 27:  # Абсолютное перемещение.
            self.move_abs(self.code[(self.step + 1) % len(self.code)] % 8)  # Исполнение.
        elif self.code[step] == 28:  # Ген поедания.
            self.eat(self.code[(self.step + 1) % len(self.code)] % 8)  # Вызов функции поедания.
        elif self.code[step] in {29, 49}:  # Абсолютное поедание.
            self.eat_abs(self.code[(self.step + 1) % len(self.code)] % 8)  # Поедание.
        elif self.code[step] == 30:  # Ген просмотра со стороны.
            self.watch(self.code[(self.step + 1) % len(self.code)] % 8)  # Реализация.
        elif self.code[step] == 31:  # Осмотр по абсолютному направлению.
            self.watch_abs(self.code[(self.step + 1) % len(self.code)] % 8)  # Выполнение.
        # elif self.code[step] == 32 or self.code[step] == 42:  # Ген распределения энергии.
        #     self.share(self.code[(self.step + 1) % len(self.code)] % 8)  # Вызов.
        #     self.step = (self.step + 1) % len(self.code)  # Продвижение курсора.
        elif self.code[step] == 33:  # Ген хемосинтеза (Переработка минералов в энергию)
            self.mine()  # Переработка
        elif self.code[step] == 36:  # Сколько у меня минералов?
            if self.mineral < self.code[(self.step + 1) % len(self.code)] \
                    * int(self.world.config["CELL"]["CONST_MINERAL"]):  # Если минералов меньше.
                self.step = (self.step + 1) % len(self.code)  # Пройти на один.
                self.do(self.step)  # Выполнить команду.
            else:  # В ином случае.
                self.step = (self.step + 2) % len(self.code)  # Переместиться сразу на два гена.
                self.do(self.step)  # Выполнить команду.
        elif self.code[step] == 38:  # Сколько у меня энергии?
            if self.energy < self.code[(self.step + 1) % len(self.code)] \
                    * int(self.world.config["CELL"]["CONST_ENERGY"]):  # Если энергии меньше.
                self.step = (self.step + 1) % len(self.code)  # Пройти на один.
                self.do(self.step)  # Выполнить команду.
            else:  # В ином случае.
                self.step = (self.step + 2) % len(self.code)  # Переместиться сразу на два гена.
                self.do(self.step)  # Выполнить команду.
        else:  # Если ген не является исполняемым.
            self.step = (self.step + self.code[step]) % len(self.code)  # Безусловный переход.
            self.energy -= 1  # Трата времени.

    def double(self) -> None:
        """
        Отпочкование потомка.
        :return: None
        """
        directions = self.directions.copy()  # Копирование списка направлений для работы с ним.
        if self.energy < 152:  # Если недостаточно энергии для деления и минимального разделения энергии.
            self.board[self.y][self.x] = Organic(self.x, self.y, self.board)  # Смерть.
        else:  # Если всего достаточно.
            self.energy -= 150  # Штраф за размножение.
            for _ in range(8):  # Перебор всех возможных направлений.
                direction = choice([i for i in directions.keys()])  # Выбор случайного направления.
                result = self.check_direction(direction)
                if result is None and result is not False:  # Если в этом направлении пусто.
                    if directions[direction] == "UP":  # Направление вверх.
                        self.board[self.y - 1][self.x] = Cell(self.world, self.x,
                                                              self.y - 1)  # Создание клетки.
                        self.board[self.y - 1][self.x].energy = self.energy // 2  # Отдача энергии.
                        self.board[self.y - 1][self.x].mineral = self.mineral // 2  # Минералов.
                        self.board[self.y - 1][self.x].code = self.code.copy()  # Передача генов.
                        self.energy //= 2  # Остаток в половину энергии.
                        self.mineral //= 2  # Остатов половину минералов.
                        if randint(1, 4) == 4:  # Шанс мутации равняется 25%.
                            self.board[self.y - 1][self.x].mutate()  # Мутация потомка.
                        if self.world.mutation_full_zone:
                            if int(self.world.start) - int(time()) >= 200:
                                self.world.mutation_full_zone = False
                            if self.board[self.y - 1][self.x].y <= len(self.board) // 16:  # Радиация.
                                self.board[self.y - 1][self.x].mutate(True)  # Мутировать.
                        break  # Окончание размножения.
                    if directions[direction] == "UP-RIGHT":  # Направление ввеох и вправо.
                        self.board[self.y - 1][self.x + 1] = Cell(self.world, self.x + 1,
                                                                  self.y - 1)  # Создание клетки.
                        self.board[self.y - 1][
                            self.x + 1].energy = self.energy // 2  # Отдача трети энергии.
                        self.board[self.y - 1][self.x + 1].code = self.code.copy()  # Передача генов.
                        self.board[self.y - 1][self.x + 1].mineral = self.mineral // 2  # Минералов.
                        self.mineral //= 2  # Остатов половину минералов.
                        self.energy //= 2  # Остаток в половину энергии.
                        if randint(1, 4) == 4:  # Шанс мутации равняется 25%.
                            self.board[self.y - 1][self.x + 1].mutate()  # Мутация потомка.
                        if self.world.mutation_full_zone:
                            if int(self.world.start) - int(time()) >= 200:
                                self.world.mutation_full_zone = False
                            if self.board[self.y - 1][self.x + 1].y <= len(self.board) // 16:  # Радиация
                                self.board[self.y - 1][self.x + 1].mutate(True)  # Мутировать.
                        break  # Окончание размножения.
                    if directions[direction] == "RIGHT":  # Направление вправо.
                        self.board[self.y][self.x + 1] = Cell(self.world, self.x + 1,
                                                              self.y)  # Создание клетки.
                        self.board[self.y][
                            self.x + 1].energy = self.energy // 2  # Отдача трети энергии.
                        self.board[self.y][self.x + 1].mineral = self.mineral // 2  # Минералов.
                        self.mineral //= 2  # Остатов половину минералов.
                        self.board[self.y][self.x + 1].code = self.code.copy()  # Передача генов.
                        self.energy //= 2  # Остаток в половину энергии.
                        if randint(1, 4) == 4:  # Шанс мутации равняется 25%.
                            self.board[self.y][self.x + 1].mutate()  # Мутация потомка.
                        if self.world.mutation_full_zone:
                            if int(self.world.start) - int(time()) >= 200:
                                self.world.mutation_full_zone = False
                            if self.board[self.y][self.x + 1].y <= len(self.board) // 16:  # Радиация.
                                self.board[self.y][self.x + 1].mutate(True)  # Мутировать.
                        break  # Окончание размножения.
                    if directions[direction] == "RIGHT-DOWN":  # Направление вниз и вправо.
                        self.board[self.y + 1][self.x + 1] = Cell(self.world, self.x + 1,
                                                                  self.y + 1)  # Создание клетки.
                        self.board[self.y + 1][
                            self.x + 1].energy = self.energy // 2  # Отдача трети энергии.
                        self.board[self.y + 1][self.x + 1].mineral = self.mineral // 2  # Минералов.
                        self.mineral //= 2  # Остатов половину минералов.
                        self.board[self.y + 1][self.x + 1].code = self.code.copy()  # Передача генов.
                        self.energy //= 2  # Остаток в половину энергии.
                        if randint(1, 4) == 4:  # Шанс мутации равняется 25%.
                            self.board[self.y + 1][self.x + 1].mutate()  # Мутация потомка.
                        if self.world.mutation_full_zone:
                            if int(self.world.start) - int(time()) >= 200:
                                self.world.mutation_full_zone = False
                            if self.board[self.y + 1][self.x + 1].y <= len(self.board) // 16:  # Радиация
                                self.board[self.y + 1][self.x + 1].mutate(True)  # Мутировать.
                        break  # Окончание размножения.
                    if directions[direction] == "DOWN":  # Направление вниз.
                        self.board[self.y + 1][self.x] = Cell(self.world, self.x,
                                                              self.y + 1)  # Создание клетки.
                        self.board[self.y + 1][self.x].energy = self.energy // 2  # Отдача энергии.
                        self.board[self.y + 1][self.x].mineral = self.mineral // 2  # Минералов.
                        self.mineral //= 2  # Остатов половину минералов.
                        self.board[self.y + 1][self.x].code = self.code.copy()  # Передача генов.
                        self.energy //= 2  # Остаток в половину энергии.
                        if randint(1, 4) == 4:  # Шанс мутации равняется 25%.
                            self.board[self.y + 1][self.x].mutate()  # Мутация потомка.
                        if self.world.mutation_full_zone:
                            if int(self.world.start) - int(time()) >= 200:
                                self.world.mutation_full_zone = False
                            if self.board[self.y + 1][self.x].y <= len(self.board) // 16:  # Радиация.
                                self.board[self.y + 1][self.x].mutate(True)  # Мутировать.
                        break  # Окончание размножения.
                    if directions[direction] == "DOWN-LEFT":  # Направление вниз и влево.
                        self.board[self.y + 1][self.x - 1] = Cell(self.world, self.x - 1,
                                                                  self.y + 1)  # Создание клетки.
                        self.board[self.y + 1][
                            self.x - 1].energy = self.energy // 2  # Отдача трети энергии.
                        self.board[self.y + 1][self.x - 1].mineral = self.mineral // 2  # Минералов.
                        self.mineral //= 2  # Остатов половину минералов.
                        self.board[self.y + 1][self.x - 1].code = self.code.copy()  # Передача генов.
                        self.energy //= 2  # Остаток в половину энергии.
                        if randint(1, 4) == 4:  # Шанс мутации равняется 25%.
                            self.board[self.y + 1][self.x - 1].mutate()  # Мутация потомка.
                        if self.board[self.y + 1][self.x - 1].y <= len(self.board) // 16:  # Радиация
                            self.board[self.y + 1][self.x - 1].mutate(True)  # Мутировать.
                        break  # Окончание размножения.
                    if directions[direction] == "LEFT":  # Направление влево.
                        self.board[self.y][self.x - 1] = Cell(self.world, self.x - 1,
                                                              self.y)  # Создание клетки.
                        self.board[self.y][self.x - 1].energy = self.energy // 2  # Отдача энергии.
                        self.board[self.y][self.x - 1].mineral = self.mineral // 2  # Минералов.
                        self.mineral //= 2  # Остатов половину минералов.
                        self.board[self.y][self.x - 1].code = self.code.copy()  # Передача генов.
                        self.energy //= 2  # Остаток в половину энергии.
                        if randint(1, 4) == 4:  # Шанс мутации равняется 25%.
                            self.board[self.y][self.x - 1].mutate()  # Мутация потомка.
                        if self.world.mutation_full_zone:
                            if int(self.world.start) - int(time()) >= 200:
                                self.world.mutation_full_zone = False
                            if self.board[self.y][self.x - 1].y <= len(self.board) // 16:  # Радиация.
                                self.board[self.y][self.x - 1].mutate()  # Мутировать.
                        break  # Окончание размножения.
                    if directions[direction] == "LEFT-UP":  # Направление вверх и влево.
                        self.board[self.y - 1][self.x - 1] = Cell(self.world, self.x - 1,
                                                                  self.y - 1)  # Создание клетки.
                        self.board[self.y - 1][
                            self.x - 1].energy = self.energy // 2  # Отдача трети энергии.
                        self.board[self.y - 1][self.x - 1].code = self.code.copy()  # Передача генов.
                        self.board[self.y - 1][self.x - 1].mineral = self.mineral // 2  # Минералов.
                        self.mineral //= 2  # Остатов половину минералов.
                        self.energy //= 2  # Остаток в половину энергии.
                        if randint(1, 4) == 4:  # Шанс мутации равняется 25%.
                            self.board[self.y - 1][self.x - 1].mutate()  # Мутация потомка.
                        if self.world.mutation_full_zone:
                            if int(self.world.start) - int(time()) >= 200:
                                self.world.mutation_full_zone = False
                            if self.board[self.y - 1][self.x - 1].y <= len(self.board) // 16:  # Радиация
                                self.board[self.y - 1][self.x - 1].mutate()  # Мутировать.
                        break  # Окончание размножения.
                else:  # Если не пусто.
                    del directions[direction]  # Удаление проверенного направления.
            if len(directions) == 0:  # Окончание всех проверок.
                self.board[self.y][self.x] = Organic(self.x, self.y, self.board)  # Смерть.

    def eat(self, direction: int) -> None:
        """
        Поедание.
        :param direction: сторона
        :return: None
        """
        result = self.check_direction(direction)  # Получение объекта со стороны.
        try:
            if result is not False:  # Проверка, если результат не отрицательный.
                if result is None:  # Если нечего есть.
                    self.energy -= 1  # Простаивание.
                    self.do((self.step + 1) % len(self.code))  # Выполнение команды.
                if isinstance(result, Organic):  # Если с этой стороны находится органика.
                    self.energy += 150  # Получение энергии с мёртвой клекти.
                if isinstance(result, Wall):  # Если с этой стороны находтся стена.
                    self.energy -= 100  # Отравление.
                    self.do((self.step + 1) % len(self.code))  # Выполнение команды.
                if self.directions[direction] == "UP":  # Направление вверх.
                    if isinstance(self.board[self.y - 1][self.x], Cell):  # Если на пути клетка.
                        self.energy += self.board[self.y - 1][self.x].energy // 3  # Приём энергии.
                        if self.is_relative(self.board[self.y - 1][self.x]):  # Проверка на родство.
                            step = (self.step + 2) % len(self.code)  # Обозначение безусловного перехода.
                        else:  # Если не родственный.
                            step = (self.step + 3) % len(self.code)  # Создание безусловного перехода.
                    self.board[self.y - 1][self.x] = None  # Уничтожение объекта.
                    if isinstance(self.board[self.y - 1][self.x], Cell):  # Перепроверка на то, что событие с клеткой было.
                        self.do(step)  # Выполнение команды.
                if self.directions[direction] == "UP-RIGHT":  # Направление ввеох и вправо.
                    if isinstance(self.board[self.y - 1][self.x + 1], Cell):  # Если на пути клетка.
                        self.energy += self.board[self.y - 1][self.x + 1].energy // 3  # Приём энергии.
                        if self.is_relative(self.board[self.y - 1][self.x + 1]):  # Проверка на родство.
                            step = (self.step + 2) % len(self.code)  # Обозначение безусловного перехода.
                        else:  # Если не родственный.
                            step = (self.step + 3) % len(self.code)  # Создание безусловного перехода.
                    self.board[self.y - 1][self.x + 1] = None  # Уничтожение объекта.
                    if isinstance(self.board[self.y - 1][self.x + 1], Cell):  # Перепроверка на то, что событие с клеткой было.
                        self.do(step)  # Выполнение команды.
                if self.directions[direction] == "RIGHT":  # Направление вправо.
                    if isinstance(self.board[self.y][self.x + 1], Cell):  # Если на пути клетка.
                        self.energy += self.board[self.y][self.x + 1].energy // 3  # Приём энергии.
                        if self.is_relative(self.board[self.y][self.x + 1]):  # Проверка на родство.
                            step = (self.step + 2) % len(self.code)  # Обозначение безусловного перехода.
                        else:  # Если не родственный.
                            step = (self.step + 3) % len(self.code)  # Создание безусловного перехода.
                    self.board[self.y][self.x + 1] = None  # Уничтожение объекта.
                    if isinstance(self.board[self.y][self.x + 1], Cell):  # Перепроверка на то, что событие с клеткой было.
                        self.do(step)  # Выполнение команды.
                if self.directions[direction] == "RIGHT-DOWN":  # Направление вниз и вправо.
                    if isinstance(self.board[self.y + 1][self.x + 1], Cell):  # Если на пути клетка.
                        self.energy += self.board[self.y + 1][self.x + 1].energy // 3  # Приём энергии.
                        if self.is_relative(self.board[self.y + 1][self.x + 1]):  # Проверка на родство.
                            step = (self.step + 2) % len(self.code)  # Обозначение безусловного перехода.
                        else:  # Если не родственный.
                            step = (self.step + 3) % len(self.code)  # Создание безусловного перехода.
                    self.board[self.y + 1][self.x + 1] = None  # Уничтожение объекта.
                    if isinstance(self.board[self.y + 1][self.x + 1], Cell):  # Перепроверка на то, что событие с клеткой было.
                        self.do(step)  # Выполнение команды.
                if self.directions[direction] == "DOWN":  # Направление вниз.
                    if isinstance(self.board[self.y + 1][self.x], Cell):  # Если на пути клетка.
                        self.energy += self.board[self.y + 1][self.x].energy // 3  # Приём энергии.
                        if self.is_relative(self.board[self.y + 1][self.x]):  # Проверка на родство.
                            step = (self.step + 2) % len(self.code)  # Обозначение безусловного перехода.
                        else:  # Если не родственный.
                            step = (self.step + 3) % len(self.code)  # Создание безусловного перехода.
                    self.board[self.y + 1][self.x] = None  # Уничтожение объекта.
                    if isinstance(self.board[self.y + 1][self.x], Cell):  # Перепроверка на то, что событие с клеткой было.
                        self.do(step)  # Выполнение команды.
                if self.directions[direction] == "DOWN-LEFT":  # Направление вниз и влево.
                    if isinstance(self.board[self.y + 1][self.x - 1], Cell):  # Если на пути клетка.
                        self.energy += self.board[self.y + 1][self.x - 1].energy // 3  # Приём энергии.
                        if self.is_relative(self.board[self.y + 1][self.x - 1]):  # Проверка на родство.
                            step = (self.step + 2) % len(self.code)  # Обозначение безусловного перехода.
                        else:  # Если не родственный.
                            step = (self.step + 3) % len(self.code)  # Создание безусловного перехода.
                    self.board[self.y + 1][self.x - 1] = None  # Уничтожение объекта.
                    if isinstance(self.board[self.y + 1][self.x - 1], Cell):  # Перепроверка на то, что событие с клеткой было.
                        self.do(step)  # Выполнение команды.
                if self.directions[direction] == "LEFT":  # Направление влево.
                    if isinstance(self.board[self.y][self.x - 1], Cell):  # Если на пути клетка.
                        self.energy += self.board[self.y][self.x - 1].energy // 3  # Приём энергии.
                        if self.is_relative(self.board[self.y][self.x - 1]):  # Проверка на родство.
                            step = (self.step + 2) % len(self.code)  # Обозначение безусловного перехода.
                        else:  # Если не родственный.
                            step = (self.step + 3) % len(self.code)  # Создание безусловного перехода.
                    self.board[self.y][self.x - 1] = None  # Уничтожение объекта.
                    if isinstance(self.board[self.y][self.x - 1], Cell):  # Перепроверка на то, что событие с клеткой было.
                        self.do(step)  # Выполнение команды.
                if self.directions[direction] == "LEFT-UP":  # Направление вверх и влево.
                    if isinstance(self.board[self.y - 1][self.x - 1], Cell):  # Если на пути клетка.
                        self.energy += self.board[self.y - 1][self.x - 1].energy // 3  # Приём энергии.
                        if self.is_relative(self.board[self.y - 1][self.x - 1]):  # Проверка на родство.
                            step = (self.step + 2) % len(self.code)  # Обозначение безусловного перехода.
                        else:  # Если не родственный.
                            step = (self.step + 3) % len(self.code)  # Создание безусловного перехода.
                    self.board[self.y - 1][self.x - 1] = None  # Уничтожение объекта.
                    if isinstance(self.board[self.y - 1][self.x - 1], Cell):  # Перепроверка на то, что событие с клеткой было.
                        self.do(step)  # Выполнение команды.
            else:  # Если нулевой.
                self.energy -= 1  # Бездействие.
        except:
            pass

    def eat_abs(self, direction):
        directions = {  # Список направлений, изменяющийся при повороте.
            0: "DOWN",  # Снизу.
            1: "DOWN-LEFT",  # Снизу, слева.
            2: "LEFT",  # Слева.
            3: "LEFT-UP",  # Сверху, слева.
            4: "UP",  # Верх.
            5: "UP-RIGHT",  # Верх, справа.
            6: "RIGHT",  # Справа.
            7: "RIGHT-DOWN",  # Снизу, справа.
        }
        direction = [i for i in self.directions.values()].index(directions[direction])
        self.eat(direction)

    def eat_organic(self):
        variants = [i for i in range(8)]
        while variants:
            direction_num = choice(variants)
            if self.check_direction(direction_num) is not False:
                direction = self.directions[direction_num]
                if direction == "UP-RIGHT":
                    if isinstance(self.board[self.y - 1][self.x + 1], Organic):
                        self.board[self.y - 1][self.x + 1] = None
                        self.energy += 100
                        break
                if direction == "RIGHT":
                    if isinstance(self.board[self.y][self.x + 1], Organic):
                        self.board[self.y][self.x + 1] = None
                        self.energy += 100
                        break
                if direction == "RIGHT-DOWN":
                    if isinstance(self.board[self.y + 1][self.x + 1], Organic):
                        self.board[self.y + 1][self.x + 1] = None
                        self.energy += 100
                        break
                if direction == "DOWN":
                    if isinstance(self.board[self.y + 1][self.x], Organic):
                        self.board[self.y + 1][self.x] = None
                        self.energy += 100
                        break
                if direction == "DOWN-LEFT":
                    if isinstance(self.board[self.y + 1][self.x - 1], Organic):
                        self.board[self.y + 1][self.x - 1] = None
                        self.energy += 100
                        break
                if direction == "LEFT":
                    if isinstance(self.board[self.y][self.x - 1], Organic):
                        self.board[self.y][self.x - 1] = None
                        self.energy += 100
                        break
                if direction == "LEFT-UP":
                    if isinstance(self.board[self.y - 1][self.x - 1], Organic):
                        self.board[self.y - 1][self.x - 1] = None
                        self.energy += 100
                        break
                if direction == "UP":
                    if isinstance(self.board[self.y - 1][self.x], Organic):
                        self.board[self.y - 1][self.x] = None
                        self.energy += 100
                        break
            variants.remove(direction_num)

    def is_relative(self, cell) -> bool:
        """
        Возвращает True, если клетка родственна данной, иначе -- False.
        :param cell: иная клетка.
        :return: True или False
        """
        get_code = cell.code.copy()  # Копирование кода иной клетки.
        for gen in get_code:  # Перебор генов в своём коде.
            if gen in get_code:  # Проверка на наличие данного гена в чужом коде.
                del get_code[get_code.index(gen)]  # Удаление в копии.
        return len(get_code) < 2  # Разница меньше 2 -- возвращает True, в ином случае -- False.

    def mine(self) -> None:
        """
        Переработка минералов
        :return: None
        """
        if self.mineral > 1000:  # За раз можно переработать только 1000 минералов
            self.mineral -= 1000
            self.energy += 4000  # 1 минерал = 4 энергии (Привет гуманитариям)
        else:  # Если меньше или равно.
            self.energy += 4 * self.mineral
            self.mineral = 0  # Обнуление минералов.
        self.step = (self.step + 1) % len(self.code)  # Переход на 1

    def move(self, direction: int) -> None:
        """
        Функция перемещения клетки.
        :param direction: направление перемещения.
        :return: None
        """
        object_on_way = self.check_direction(direction)
        if object_on_way is None:  # Если пусто.
            if self.directions[direction] == "UP":  # Направление вверх.
                self.board[self.y - 1][self.x] = self  # Создание себя.
                self.board[self.y][self.x] = None  # Уничтожение старой своей копии.
                self.y -= 1  # Изменение по высоте.
            if self.directions[direction] == "UP-RIGHT":  # Направление ввеох и вправо.
                self.board[self.y - 1][self.x + 1] = self  # Создание себя.
                self.board[self.y][self.x] = None  # Уничтожение старой своей копии.
                self.y -= 1  # Изменение по высоте.
                self.x += 1  # Изменение по ширине.
            if self.directions[direction] == "RIGHT":  # Направление вправо.
                self.board[self.y][self.x + 1] = self  # Создание себя.
                self.board[self.y][self.x] = None  # Уничтожение старой своей копии.
                self.x += 1  # Изменение по ширине.
            if self.directions[direction] == "RIGHT-DOWN":  # Направление вниз и вправо.
                self.board[self.y + 1][self.x + 1] = self  # Создание себя.
                self.board[self.y][self.x] = None  # Уничтожение старой своей копии.
                self.y += 1  # Изменение по высоте.
                self.x += 1  # Изменение по ширине.
            if self.directions[direction] == "DOWN":  # Направление вниз.
                self.board[self.y + 1][self.x] = self  # Создание себя.
                self.board[self.y][self.x] = None  # Уничтожение старой своей копии.
                self.y += 1  # Изменение по высоте.
            if self.directions[direction] == "DOWN-LEFT":  # Направление вниз и влево.
                self.board[self.y + 1][self.x - 1] = self  # Создание себя.
                self.board[self.y][self.x] = None  # Уничтожение старой своей копии.
                self.y += 1  # Изменение по высоте.
                self.x -= 1  # Изменение по ширине.
            if self.directions[direction] == "LEFT":  # Направление влево.
                self.board[self.y][self.x - 1] = self  # Создание себя.
                self.board[self.y][self.x] = None
                self.x -= 1  # Изменение по ширине.
            if self.directions[direction] == "LEFT-UP":  # Направление вверх и влево.
                self.board[self.y - 1][self.x - 1] = self  # Создание себя.
                self.board[self.y][self.x] = None  # Уничтожение старой своей копии.
                self.y -= 1  # Изменение по высоте.
                self.x -= 1  # Изменение по ширине.
            self.do((self.step + 2) % len(self.code))  # Выполнение команды.
        elif isinstance(object_on_way, Wall):  # Если на пути стена.
            self.do((self.step + 3) % len(self.code))  # Выполнение команды.
        elif isinstance(object_on_way, Organic):  # Если на пути органика.
            self.do((self.step + 4) % len(self.code))  # Выполнение команды.
        elif isinstance(object_on_way, Cell):  # Если на пути какая-либо клетка.
            if not self.is_relative(object_on_way):  # Проверка на родство.
                self.do((self.step + 5) % len(self.code))  # Выполнение команды.
            else:  # Иной бот.
                self.do((self.step + 6) % len(self.code))  # Выполнение команды.
        elif object_on_way is False:  # Упор в границу.
            self.step = (self.step + 1) % len(self.code)  # Переход.
            self.do(self.step)  # Выполнение команды.

    def move_abs(self, direction):
        directions = {  # Список направлений, изменяющийся при повороте.
            0: "UP",  # Верх.
            1: "UP-RIGHT",  # Верх, справа.
            2: "RIGHT",  # Справа.
            3: "RIGHT-DOWN",  # Снизу, справа.
            4: "DOWN",  # Снизу.
            5: "DOWN-LEFT",  # Снизу, слева.
            6: "LEFT",  # Слева.
            7: "LEFT-UP"  # Сверху, слева.
        }
        direction = [i for i in self.directions.values()].index(directions[direction])
        self.move(direction)

    def mutate(self, extra=False) -> None:
        """
        Мутация.
        :return: None
        """
        if not extra:
            self.code[randint(0, 63)] = randint(0, 63)  # Замена случайного гена случайным числом.
        else:
            self.code[randint(0, 63)] = 24  # Добавим ген поворота
            self.code[randint(0, 63)] = 26  # Добавим ген ходьбы
            for i in range(2):
                self.code[randint(0, 63)] = randint(0, 63)  # Замена случайного гена случайным числом.

    def share(self, direction: int) -> None:
        """
        Уравнять энергию с соседом.
        :param direction: относительное направление
        :return: None
        """
        if isinstance(self.check_direction(direction), Cell):
            if self.directions[direction] == "UP":  # Направление вверх.
                self.board[self.y - 1][self.x].energy, self.energy = self.energy + self.board[
                    self.y - 1][self.x].energy // 2, self.energy + self.board[
                    self.y - 1][self.x].energy // 2  # Распределить энергию.
            if self.directions[direction] == "UP-RIGHT":  # Направление ввеох и вправо.
                self.board[self.y - 1][self.x + 1].energy, self.energy = self.energy + self.board[
                    self.y - 1][self.x + 1].energy // 2, self.energy + self.board[
                    self.y - 1][self.x + 1].energy // 2  # Распределить энергию.
            if self.directions[direction] == "RIGHT":  # Направление вправо.
                self.board[self.y][self.x + 1].energy, self.energy = self.energy + self.board[
                    self.y][self.x + 1].energy // 2, self.energy + self.board[
                    self.y][self.x + 1].energy // 2  # Распределить энергию.
            if self.directions[direction] == "RIGHT-DOWN":  # Направление вниз и вправо.
                self.board[self.y + 1][self.x + 1].energy, self.energy = self.energy + self.board[
                    self.y + 1][self.x + 1].energy // 2, self.energy + self.board[
                    self.y + 1][self.x + 1].energy // 2  # Распределить энергию.
            if self.directions[direction] == "DOWN":  # Направление вниз.
                self.board[self.y + 1][self.x].energy, self.energy = self.energy + self.board[
                    self.y + 1][self.x].energy // 2, self.energy + self.board[
                    self.y + 1][self.x].energy // 2  # Распределить энергию.
            if self.directions[direction] == "DOWN-LEFT":  # Направление вниз и влево.
                self.board[self.y + 1][self.x - 1].energy, self.energy = self.energy + self.board[
                    self.y + 1][self.x - 1].energy // 2, self.energy + self.board[
                    self.y + 1][self.x - 1].energy // 2  # Распределить энергию.
            if self.directions[direction] == "LEFT":  # Направление влево.
                self.board[self.y][self.x - 1].energy, self.energy = self.energy + self.board[
                    self.y][self.x - 1].energy // 2, self.energy + self.board[
                    self.y][self.x - 1].energy // 2  # Распределить энергию.
            if self.directions[direction] == "LEFT-UP":  # Направление вверх и влево.
                self.board[self.y - 1][self.x - 1].energy, self.energy = self.energy + self.board[
                    self.y - 1][self.x - 1].energy // 2, self.energy + self.board[
                    self.y - 1][self.x - 1].energy // 2  # Распределить энергию.

    def update(self) -> None:
        """
        Обновление состояния бота.
        :return: None
        """
        if self.energy <= 0:  # Если энергия заканчивается.
            self.board[self.y][self.x] = Organic(self.x, self.y, self.board)  # Смерть.
        else:
            try:  # Проверка на наличие ошибок.
                self.do(self.step)  # Совершение дейсвтия, прописанного в генном коде.
            except RecursionError:  # Бесконечное углубление.
                pass  # Остановка выполнения кода.
            if self.y >= self.world.y // 2:  # Если находится в нижней части мира.
                self.mineral += self.world.give_mineral(self.y)  # Обращение за минералами.
                if self.mineral > 2000:  # Если граница максимума пересечена.
                    self.mineral = 2000  # Обрезание.
            if self.energy >= int(self.world.config["CELL"]["BORN_ENERGY"]):  # Достижение порога размножения.
                self.double()  # Размножение.
            # if self.y == 0:
            #     self.mutate()
            self.energy -= int(self.world.config["CELL"]["MINUS_ENERGY"])

    def watch(self, direction: int) -> None:
        """
        Проверка стороны.
        :param direction: направление
        :return: None
        """
        result = self.check_direction(direction)  # Объект со стороны.
        if result is None:  # Если пусто.
            self.do((self.step + 2) % len(self.code))  # Выполнение команды.
        if isinstance(result, Wall):  # Если стена.
            self.do((self.step + 3) % len(self.code))  # Выполнение команды.
        if isinstance(result, Organic):  # Если труп.
            self.do((self.step + 4) % len(self.code))  # Выполнение команды.
        if isinstance(result, Cell):  # Если клетка.
            if self.is_relative(result):  # Если родственник.
                self.do((self.step + 5) % len(self.code))  # Выполнение команды.
            else:  # В ином случае.
                self.do((self.step + 6) % len(self.code))  # Выполнение команды.

    def watch_abs(self, direction):
        directions = {  # Список направлений, изменяющийся при повороте.
            0: "UP",  # Верх.
            1: "UP-RIGHT",  # Верх, справа.
            2: "RIGHT",  # Справа.
            3: "RIGHT-DOWN",  # Снизу, справа.
            4: "DOWN",  # Снизу.
            5: "DOWN-LEFT",  # Снизу, слева.
            6: "LEFT",  # Слева.
            7: "LEFT-UP"  # Сверху, слева.
        }
        direction = [i for i in self.directions.values()].index(directions[direction])
        self.watch(direction)
