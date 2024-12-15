import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Размер экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гонка по кругу")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)

# Параметры круга
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2  # Центр круга
RADIUS = 200  # Радиус круга

# Загрузка иконок для персонажей
icon_size = 30
icons = {
    "Таракан": pygame.Surface((icon_size, icon_size)),
    "Собака": pygame.Surface((icon_size, icon_size)),
    "Дед Мороз": pygame.Surface((icon_size, icon_size)),
    "Человечек": pygame.Surface((icon_size, icon_size)),
}

# Рисуем простые иконки (например, цвета для простоты)
icons["Таракан"].fill(RED)
icons["Собака"].fill(GREEN)
icons["Дед Мороз"].fill(BLUE)
icons["Человечек"].fill(YELLOW)

# Персонажи
characters = [
    {"name": "Таракан", "color": RED, "angle": random.uniform(0, 2 * math.pi), "speed": random.uniform(1, 3), "laps": 0,
     "last_angle": 0},
    {"name": "Собака", "color": GREEN, "angle": random.uniform(0, 2 * math.pi), "speed": random.uniform(1, 3),
     "laps": 0, "last_angle": 0},
    {"name": "Дед Мороз", "color": BLUE, "angle": random.uniform(0, 2 * math.pi), "speed": random.uniform(1, 3),
     "laps": 0, "last_angle": 0},
    {"name": "Человечек", "color": YELLOW, "angle": random.uniform(0, 2 * math.pi), "speed": random.uniform(1, 3),
     "laps": 0, "last_angle": 0}
]

# Количество кругов для завершения гонки
target_laps = 5

# Шрифт для текста
font = pygame.font.SysFont(None, 36)


# Функция для отрисовки персонажа
def draw_character(character):
    x = CENTER_X + RADIUS * math.cos(character["angle"])
    y = CENTER_Y + RADIUS * math.sin(character["angle"])
    pygame.draw.circle(screen, character["color"], (int(x), int(y)), 15)

    # Отображаем иконку персонажа рядом с ним
    icon_x = CENTER_X + RADIUS * math.cos(character["angle"]) - icon_size // 2
    icon_y = CENTER_Y + RADIUS * math.sin(character["angle"]) - icon_size // 2
    screen.blit(icons[character["name"]], (icon_x, icon_y))


# Функция для отображения текста
def display_text(text, x, y, color):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


# Функция для отрисовки трассы и линии старта
def draw_track():
    # Рисуем круг трассы
    pygame.draw.circle(screen, LIGHT_GRAY, (CENTER_X, CENTER_Y), RADIUS, 10)

    # Рисуем шахматный стиль трассы (половинки чередуются)
    for i in range(0, 360, 15):  # Шахматные полоски на окружности
        angle_start = math.radians(i)
        angle_end = math.radians(i + 15)

        x1 = CENTER_X + RADIUS * math.cos(angle_start)
        y1 = CENTER_Y + RADIUS * math.sin(angle_start)
        x2 = CENTER_X + RADIUS * math.cos(angle_end)
        y2 = CENTER_Y + RADIUS * math.sin(angle_end)

        color = DARK_GRAY if (i // 15) % 2 == 0 else LIGHT_GRAY
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 10)

    # Линия старта
    pygame.draw.line(screen, BLACK, (CENTER_X - RADIUS, CENTER_Y), (CENTER_X + RADIUS, CENTER_Y), 5)


# Главный игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Рисуем трассу
    draw_track()

    # Проверяем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление состояния гонки
    for character in characters:
        # Замедляем скорость по мере прохождения кругов
        character["speed"] = max(1, character["speed"] - 0.05 * character["laps"])  # Уменьшаем скорость

        # Двигаем персонажа по кругу
        character["angle"] += character["speed"] * 0.01  # Увеличиваем угол на основе скорости
        if character["angle"] > 2 * math.pi:
            character["angle"] -= 2 * math.pi  # Если угол превышает 360 градусов, сбрасываем его

        # Проверка, пересек ли персонаж стартовую линию (первый угол)
        if character["angle"] < 0.1 and character["last_angle"] > 2 * math.pi - 0.1:  # Если прошло через 0 радиан
            character["laps"] += 1
            # Если количество кругов достигло заданного, останавливаем гонку для этого персонажа
            if character["laps"] >= target_laps:
                running = False  # Останавливаем игру, когда кто-то достигает 5 кругов

            # Каждые несколько шагов случайным образом изменяем скорость и направление
            if random.random() < 0.05:  # 5% шанс на изменение
                character["speed"] = random.uniform(1, 2)  # Изменяем скорость и направление

        # Обновляем последний угол для следующей итерации
        character["last_angle"] = character["angle"]

    # Отображаем персонажей
    for character in characters:
        draw_character(character)

    # Отображаем статус гонки
    leader = min(characters, key=lambda c: c["laps"])  # Лидер - игрок, который первым пересек стартовую линию
    display_text("Текущий лидер: " + leader["name"], 20, 20, BLACK)
    display_text("Кругов до победы: {}".format(target_laps), 20, 60, BLACK)

    # Отображаем текущие круги каждого персонажа
    for i, character in enumerate(characters):
        display_text(f"{character['name']}: {character['laps']} кругов", 20, 120 + i * 40, character["color"])

    pygame.display.update()
    clock.tick(60)  # Ограничиваем кадры 60 в секунду

# Выводим победителя после завершения гонки
winner = max(characters, key=lambda c: c["laps"])
display_text(f"Победитель: {winner['name']}", WIDTH // 2 - 100, HEIGHT // 2)
pygame.display.update()
pygame.time.wait(2000)  # Показываем победителя 2 секунды перед закрытием игры

pygame.quit()
