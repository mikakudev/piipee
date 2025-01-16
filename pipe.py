import pygame

PIPE_IMAGES = {
    "straight": pygame.image.load("assets/images/straight.png"),
    "corner": pygame.image.load("assets/images/corner.png"),
    "double_corner": pygame.image.load("assets/images/double_corner.png")
}

class Pipe:
    def __init__(self, pipe_type):
        self.pipe_type = pipe_type  # Тип трубы: straight, corner, double_corner
        self.orientation = 0  # Поворот трубы: 0, 90, 180, 270 градусов

    def rotate(self):
        """Поворачивает трубу на 90 градусов."""
        self.orientation = (self.orientation + 90) % 360

    def is_connectable(self, other_pipe, direction):
        """
        Проверяет, есть ли соединение между этой трубой и другой трубой в указанном направлении.

        Args:
            other_pipe (Pipe): Другая труба для проверки соединения.
            direction (str): Направление соединения ('up', 'down', 'left', 'right').

        Returns:
            bool: True, если трубы соединяются, иначе False.
        """
        # Определяем противоположное направление
        opposite_directions = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left',
        }

        # Проверяем, совпадают ли направления соединений
        return (direction in self.get_connections() and
                opposite_directions[direction] in other_pipe.get_connections())

    def get_connections(self):
        """
        Возвращает словарь направлений, в которых текущая труба может соединяться,
        в зависимости от её типа и ориентации.
        """
        if self.pipe_type == 'straight':
            if self.orientation in [0, 180]:
                return {'up', 'down'}
            elif self.orientation in [90, 270]:
                return {'left', 'right'}

        elif self.pipe_type == 'corner':
            if self.orientation == 0:
                return {'up', 'right'}
            elif self.orientation == 90:
                return {'right', 'down'}
            elif self.orientation == 180:
                return {'down', 'left'}
            elif self.orientation == 270:
                return {'left', 'up'}

        elif self.pipe_type == 'double_corner':
            # Двойное колено работает как прямая труба
            return {'up', 'down', 'left', 'right'}

        return set()

    def get_image(self):
        """Возвращает изображение трубы с учетом ориентации."""
        base_image = PIPE_IMAGES[self.pipe_type]
        return pygame.transform.rotate(base_image, self.orientation)