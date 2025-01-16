import pygame
from pipe import Pipe



class GameField:
    def __init__(self, size):
        self.size = size
        self.field = []
        self.start_position = (0, 0)  # Начальная позиция
        self.end_position = (self.size - 1, self.size - 1)  # Конечная позиция
        self.create_field()

    def create_field(self):
        """Создание игрового поля."""
        self.field = []
        for row in range(self.size):
            field_row = []
            for col in range(self.size):
                pipe_type = "straight"  # По умолчанию - прямая труба
                field_row.append(Pipe(pipe_type))
            self.field.append(field_row)

        # Устанавливаем начальный и конечный блоки
        self.field[0][0].start = True
        self.field[self.size - 1][self.size - 1].end = True

        print(f"Начальная позиция: {self.start_position}")
        print(f"Конечная позиция: {self.end_position}")

    def run_game(self):
        """Запуск игры."""
        # Инициализация Pygame
        pygame.init()
        window_size = 600
        screen = pygame.display.set_mode((window_size, window_size))
        pygame.display.set_caption("Трубопровод")

        # Главный игровой цикл
        running = True
        while running:
            screen.fill((255, 255, 255))  # Заполнение экрана белым цветом

            # Отображаем игровое поле
            self.display_field(screen)

            # Проверка завершения игры
            if self.is_game_solved():
                print("Игра завершена!")
                running = False  # Завершаем игру, если задача решена

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Закрыть игру
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Логика для обработки кликов по фишкам (поворот труб)
                    x, y = event.pos
                    row = y // (window_size // self.size)
                    col = x // (window_size // self.size)
                    if 0 <= row < self.size and 0 <= col < self.size:
                        self.field[row][col].rotate()  # Поворот фишки

            # Обновление экрана
            pygame.display.flip()

        pygame.quit()

    def display_field(self, screen):
        """Отображение игрового поля на экране."""
        window_size = 600
        cell_size = window_size // self.size
        for row in range(self.size):
            for col in range(self.size):
                pipe_image = self.field[row][col].get_image()
                screen.blit(pipe_image, (col * cell_size, row * cell_size))

    def is_game_solved(self):
        """Проверка, решена ли задача (по соединению труб)."""
        visited = set()
        return self.dfs(self.start_position[0], self.start_position[1], visited)

    def dfs(self, row, col, visited):
        """Поиск пути с использованием поиска в глубину (DFS)."""
        # Если мы достигли конечной точки
        if (row, col) == self.end_position:
            print(f"Конечная точка достигнута: ({row}, {col})")
            return True

        # Если клетка уже посещена, избегаем зацикливания
        if (row, col) in visited:
            return False

        visited.add((row, col))

        # Проверяем соседей (вверх, вниз, влево, вправо)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Направления (верх, низ, влево, вправо)
        for d in directions:
            new_row, new_col = row + d[0], col + d[1]

            # Проверка, что клетка находится в пределах поля
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                print(f"Проверка соединения: ({row}, {col}) с ({new_row}, {new_col})")
                # Проверяем, соединяются ли текущая фишка и соседняя
                if self.field[row][col].is_connectable(self.field[new_row][new_col], direction):
                    # Рекурсивно ищем путь
                    if self.dfs(new_row, new_col, visited):
                        return True

        # Если путь не найден, возвращаем False
        return False