import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройка экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Арканоид')

# Загрузка фона
background = pygame.image.load('1.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Настройки цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)  # Красный цвет для второго шарика
DARK_PURPLE = (75, 0, 130)  # Темно-фиолетовый цвет для блоков

# Параметры платформы
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 15
paddle_speed = 10

# Параметры шарика
ball_radius = 20

# Блоки
block_width = (WIDTH - 5 * 10) // 4  # Четыре блока в ряд
block_height = 60


def create_blocks():
    return [pygame.Rect(5 + i * (block_width + 10), 5 + j * (block_height + 10), block_width, block_height)
            for i in range(4) for j in range(3)]


# Функция для перезапуска игры
def reset_game():
    global paddle, ball1, ball2, ball1_speed_x, ball1_speed_y, ball2_speed_x, ball2_speed_y, blocks
    paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Инициализация первого шарика
    ball1 = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_radius, ball_radius)
    ball1_speed_x = 8 * random.choice((1, -1))
    ball1_speed_y = -8

    # Инициализация второго шарика
    ball2 = pygame.Rect(WIDTH // 2 + 100, HEIGHT // 2, ball_radius, ball_radius)
    ball2_speed_x = 8 * random.choice((1, -1))
    ball2_speed_y = -8

    blocks = create_blocks()  # Глобальная переменная


# Функция отображения текста
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


# Основной игровой цикл
def main_game():
    global ball1_speed_x, ball1_speed_y, ball2_speed_x, ball2_speed_y, blocks  # Используем глобальные переменные
    running = True
    game_over = False

    while running:
        pygame.time.delay(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление платформой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.right += paddle_speed

        # Если игра не окончена, продолжаем обновлять шарики и блоки
        if not game_over:
            # Логика движения первого шарика
            ball1.x += ball1_speed_x
            ball1.y += ball1_speed_y

            # Логика движения второго шарика
            ball2.x += ball2_speed_x
            ball2.y += ball2_speed_y

            # Отскок от стен для первого шарика
            if ball1.left <= 0 or ball1.right >= WIDTH:
                ball1_speed_x = -ball1_speed_x
            if ball1.top <= 0:
                ball1_speed_y = -ball1_speed_y

            # Отскок от стен для второго шарика
            if ball2.left <= 0 or ball2.right >= WIDTH:
                ball2_speed_x = -ball2_speed_x
            if ball2.top <= 0:
                ball2_speed_y = -ball2_speed_y

            # Отскок от платформы для обоих шариков
            if ball1.colliderect(paddle):
                ball1_speed_y = -ball1_speed_y
            if ball2.colliderect(paddle):
                ball2_speed_y = -ball2_speed_y

            # Логика блоков для первого шарика
            new_blocks = []
            for block in blocks:
                if ball1.colliderect(block):
                    ball1_speed_y = -ball1_speed_y
                elif ball2.colliderect(block):  # Логика блоков для второго шарика
                    ball2_speed_y = -ball2_speed_y
                else:
                    new_blocks.append(block)
            blocks = new_blocks

            # Если один из шариков упал ниже экрана
            if ball1.bottom >= HEIGHT or ball2.bottom >= HEIGHT:
                game_over = True

        # Рисование объектов
        screen.blit(background, (0, 0))  # Рисуем фон
        pygame.draw.rect(screen, WHITE, paddle)  # Платформа
        pygame.draw.ellipse(screen, WHITE, ball1)  # Первый шарик — белый
        pygame.draw.ellipse(screen, RED, ball2)  # Второй шарик — красный
        for block in blocks:
            pygame.draw.rect(screen, DARK_PURPLE, block)  # Темно-фиолетовые блоки

        # Если игра окончена, выводим сообщение и ждем нажатия клавиши
        if game_over:
            draw_text("Вы проиграли", 64, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("Начните игру занова", 32, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
            pygame.display.flip()

            # Ждем нажатия пробела для перезапуска игры
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        reset_game()  # Перезапуск игры
                        game_over = False
                        waiting = False

        # Обновление экрана
        pygame.display.flip()


# Перезапуск игры
reset_game()
main_game()

# Завершение Pygame
pygame.quit()
