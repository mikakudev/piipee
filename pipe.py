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

    def is_connectable(self, other_pipe):
        """Проверка, могут ли две трубы соединяться."""
        print(f"Проверка соединения между {self.pipe_type} и {other_pipe.pipe_type}")

        # Прямые трубы соединяются с прямыми
        if self.pipe_type == "straight" and other_pipe.pipe_type == "straight":
            return True
        # Колена соединяются с коленами
        elif self.pipe_type == "corner" and other_pipe.pipe_type == "corner":
            return True
        # Двойные колена функционально как прямые трубы
        elif self.pipe_type == "double_corner" and other_pipe.pipe_type == "double_corner":
            return True
        # Прочие типы соединений (можно доработать)
        print(f"Не могут соединяться: {self.pipe_type} и {other_pipe.pipe_type}")
        return False