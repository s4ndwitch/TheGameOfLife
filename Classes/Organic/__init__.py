class Organic:
    """
    Класс органики.
    """
    def __init__(self, x: int, y: int, world):
        """
        Инициализация органики.
        :param x: положение органики по ширине.
        :param y: положение органики оп высоте.
        :param world: родительский мир.
        """
        self.x = x  # Положение органики по ширине.
        self.y = y  # Положение органики по высоте.
        self.world = world  # Родительский мир.
        self.check = True  # Переключатель для проверки совршения хода.

    def update(self) -> None:
        """
        Обновление положения. Летит вниз.
        :return: None
        """
        if self.y < len(self.world) - 1 and self.world[self.y + 1][self.x] is None:  # Если пусто.
            self.y += 1  # Изменение координаты своего положение на 1 вниз.
            self.world[self.y][self.x] = self  # Копирование себя.
            self.world[self.y - 1][self.x] = None  # Уничтожение своей прошлой версии.
