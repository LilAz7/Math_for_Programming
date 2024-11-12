import pygame
import random
import heapq
import time

# Константы
WINDOW_SIZE = 500  # Размер окна
GRID_SIZE = 20  # Размер одной клетки
ROWS = WINDOW_SIZE // GRID_SIZE  # Количество строк
COLS = WINDOW_SIZE // GRID_SIZE  # Количество столбцов

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("A* Pathfinding in Maze")
font = pygame.font.Font(None, 36)

# Лабиринт
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]  # 1 — стена, 0 — свободное пространство
start_pos = (1, 1)
end_pos = (COLS - 2, ROWS - 2)


# Функция генерации лабиринта
def generate_maze(x, y):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)
    maze[y][x] = 0  # Сделать текущую позицию проходом
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
            maze[ny][nx] = 0
            maze[y + dy // 2][x + dx // 2] = 0
            generate_maze(nx, ny)


# Генерация лабиринта
generate_maze(start_pos[0], start_pos[1])
maze[start_pos[1]][start_pos[0]] = 0
maze[end_pos[1]][end_pos[0]] = 0


# A* алгоритм для нахождения оптимального пути
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(maze, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for neighbor in neighbors:
            if 0 <= neighbor[0] < COLS and 0 <= neighbor[1] < ROWS and maze[neighbor[1]][neighbor[0]] == 0:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # Путь не найден


# Получаем оптимальный путь с использованием A*
optimal_path = a_star_search(maze, start_pos, end_pos)

# Переменные для анализа
real_path = []  # Запоминаем фактический путь игрока
player_pos = list(start_pos)  # Начальная позиция игрока
steps_taken = 0
game_won = False
game_start_time = None  # Время начала игры, будет установлено, когда игрок начнет движение


# Функция для рисования текста с обводкой
def draw_text_with_outline(text, font, color, x, y, outline_color, outline_width):
    # Рисуем обводку текста
    text_surface = font.render(text, True, outline_color)
    for dx in [-outline_width, 0, outline_width]:
        for dy in [-outline_width, 0, outline_width]:
            screen.blit(text_surface, (x + dx, y + dy))

    # Рисуем основной текст
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Функция для отрисовки сетки и пути
def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            if (x, y) == start_pos:
                pygame.draw.rect(screen, BLUE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            if (x, y) == end_pos:
                pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Отрисовка оптимального пути
    if optimal_path:
        for pos in optimal_path:
            pygame.draw.rect(screen, PURPLE, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Отрисовка фактического пути игрока
    for pos in real_path:
        pygame.draw.rect(screen, RED, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


# Функция для перемещения игрока
def move_player(dx, dy):
    global game_won, steps_taken
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy

    if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
        player_pos[0] = new_x
        player_pos[1] = new_y
        real_path.append(tuple(player_pos))
        steps_taken += 1

        if player_pos == list(end_pos):
            game_won = True


# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    draw_grid()

    if game_won:
        # Отображаем сообщение о завершении с обводкой
        draw_text_with_outline("Путь найден!", font, YELLOW, WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 - 18, BLACK, 2)

        # Подсчитаем и выведем шаги на оптимальном пути
        optimal_steps = len(optimal_path) - 1  # Минус 1, потому что старт не должен считаться как шаг
        draw_text_with_outline(f"Оптимальный путь: {optimal_steps} шагов", font, YELLOW, 10, 50, BLACK, 2)

        # Показать анализ пути
        draw_text_with_outline(f"Шагов: {steps_taken}", font, YELLOW, 10, 10, BLACK, 2)

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_start_time:
                    game_start_time = time.time()  # Засечь время начала игры, когда игрок двигается
                if event.key == pygame.K_UP:
                    move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_player(1, 0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
