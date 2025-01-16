import pygame
import sys

import GameManager
from game_field import GameField  # Импорт класса GameField

# Размеры окна
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GRAY = (200, 200, 200)


# Инициализация Pygame
def init_game():
    if not pygame.get_init():  # Проверяем, был ли Pygame инициализирован
        print("Инициализация Pygame...")
        pygame.init()  # Инициализация Pygame
    else:
        print("Pygame уже инициализирован!")

    global FONT, screen
    FONT = pygame.font.Font(pygame.font.get_default_font(), 24)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Экран создается здесь
    print("Экран создан.")


# Функция для отрисовки кнопки
def draw_button(text, x, y, width, height, color, action=None):
    """Рисует кнопку и возвращает True, если она нажата."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Если мышь над кнопкой
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, GRAY, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    # Текст на кнопке
    text_surface = FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)


# Главное меню
def show_menu():
    try:
        init_game()  # Инициализация Pygame перед началом работы

        selected_size = 9  # Размер сетки по умолчанию

        def change_size(new_size):
            """Меняет размер сетки."""
            nonlocal selected_size
            selected_size = new_size
            print(f"Выбран размер сетки: {selected_size}x{selected_size}")

        def start_game():
            print(f"Начинаем игру с размером {selected_size}x{selected_size}")

            # Логируем переход в игру
            try:
                game_field = GameField(selected_size, screen=screen)  # Инициализируем игровое поле
                GameManager.SCREEN = 'game'
                game_field.run_game()  # Запускаем игру
            except Exception as e:
                print(f"Ошибка при запуске игры: {e}")

        def show_records():
            print(f"Открываем рекорды для размера {selected_size}x{selected_size}")
            # Здесь откроется экран рекордов

        running = True
        while running:
            screen.fill(WHITE)
            if GameManager.SCREEN == 'menu':
                # Заголовок
                title_surface = FONT.render("Выберите размер сетки", True, BLACK)
                title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
                screen.blit(title_surface, title_rect)

                # Кнопки выбора размера сетки
                draw_button("9x9", 100, 150, 100, 50, BLUE, lambda: change_size(9))
                draw_button("12x12", 250, 150, 100, 50, BLUE, lambda: change_size(12))
                draw_button("15x15", 400, 150, 100, 50, BLUE, lambda: change_size(15))

                # Кнопки действия
                draw_button("Начать игру", 150, 300, 150, 50, BLUE, start_game)
                draw_button("Рекорды", 350, 300, 150, 50, BLUE, show_records)

                # Обновление экрана
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()

        # Делаем таймаут перед завершением, чтобы избежать быстрого закрытия
        pygame.time.wait(500)  # 500 миллисекунд перед выходом
        pygame.quit()

    except pygame.error as e:
        print(f"Ошибка Pygame: {e}")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"Общая ошибка: {e}")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    try:
        show_menu()
    except pygame.error as e:
        print(f"Ошибка Pygame: {e}")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"Общая ошибка: {e}")
        pygame.quit()
        sys.exit()
