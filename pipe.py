import pygame

PIPE_IMAGES = {
    "straight": pygame.image.load("assets/images/straight.png"),
    "corner": pygame.image.load("assets/images/corner.png"),
    "double_corner": pygame.image.load("assets/images/double_corner.png")
}

class Pipe:
    def __init__(self, pipe_type, start=False, end=False):
        """Инициализация фишки."""
        self.pipe_type = pipe_type  # Тип трубы (straight, corner, double_corner)
        self.rotation = 0  # Угол поворота (0, 90, 180, 270)
        self.start = start  # Является ли это начальной фишкой
        self.end = end  # Является ли это конечной фишкой

    def rotate(self):
        """Поворот фишки на 90 градусов."""
        self.rotation = (self.rotation + 90) % 360

    def get_image(self):
        """Возвращает изображение фишки с учётом её поворота."""
        image = PIPE_IMAGES[self.pipe_type]
        return pygame.transform.rotate(image, self.rotation)

    def is_connectable(self, other_pipe, row, col, new_row, new_col):
        """Проверка, могут ли две трубы соединяться по типу и направлению."""
        print(
            f"Проверка соединения между {self.pipe_type} ({self.rotation}) и {other_pipe.pipe_type} ({other_pipe.rotation})")

        # Карта направлений: row_delta, col_delta → направление
        direction_map = {
            (-1, 0): "north",  # вверх
            (1, 0): "south",  # вниз
            (0, -1): "west",  # влево
            (0, 1): "east"  # вправо
        }

        # Определяем текущее направление движения
        direction = direction_map[(new_row - row, new_col - col)]

        # Карта допустимых направлений для каждого типа трубы
        pipe_directions = {
            "straight": {
                0: {"north", "south"},  # вертикальная труба
                90: {"west", "east"}  # горизонтальная труба
            },
            "corner": {
                0: {"north", "east"},  # поворот "вверх-вправо"
                90: {"east", "south"},  # поворот "вправо-вниз"
                180: {"south", "west"},  # поворот "вниз-влево"
                270: {"west", "north"}  # поворот "влево-вверх"
            },
            "double_corner": {
                0: {"north", "south"},  # как прямая вертикальная
                90: {"west", "east"}  # как прямая горизонтальная
            }
        }

        # Получаем допустимые направления для текущей и соседней трубы
        self_allowed = pipe_directions.get(self.pipe_type, {}).get(self.rotation, set())
        other_allowed = pipe_directions.get(other_pipe.pipe_type, {}).get(other_pipe.rotation, set())

        # Проверяем, совпадают ли направления
        if direction in self_allowed and direction in other_allowed:
            print(
                f"Трубы соединяются: {self.pipe_type} ({self.rotation}) -> {other_pipe.pipe_type} ({other_pipe.rotation})")
            return True

        print(
            f"Трубы не соединяются: {self.pipe_type} ({self.rotation}) -> {other_pipe.pipe_type} ({other_pipe.rotation})")
        return False