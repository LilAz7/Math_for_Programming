import pygame
import random

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

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Maze Game")
font = pygame.font.Font(None, 36)  # Шрифт для уведомления о прохождении

# Создание лабиринта с начальной и конечной точками
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]  # 1 — стена, 0 — свободное пространство
start_pos = (1, 1)
end_pos = (COLS - 2, ROWS - 2)
game_won = False  # Флаг, указывающий на прохождение лабиринта


# Функция генерации лабиринта с помощью DFS
def generate_maze(x, y):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)
    maze[y][x] = 0  # Сделать текущую позицию проходом
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
            # Прорубаем путь между ячейками
            maze[ny][nx] = 0
            maze[y + dy // 2][x + dx // 2] = 0
            generate_maze(nx, ny)


# Генерация лабиринта с использованием DFS
generate_maze(start_pos[0], start_pos[1])

# Убедимся, что начальная и конечная позиции свободны
maze[start_pos[1]][start_pos[0]] = 0
maze[end_pos[1]][end_pos[0]] = 0

player_pos = list(start_pos)  # Начальная позиция игрока


# Функция для отрисовки сетки
def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Отметим начальную точку
            if (x, y) == start_pos:
                pygame.draw.rect(screen, BLUE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Отметим конечную точку
            if (x, y) == end_pos:
                pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Отметим объект игрока
            if [x, y] == player_pos:
                pygame.draw.rect(screen, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


# Функция для перемещения игрока
def move_player(dx, dy):
    global game_won
    # Новая позиция игрока
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy

    # Проверка на выход за пределы и на столкновение со стенами
    if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
        player_pos[0] = new_x
        player_pos[1] = new_y

        # Проверка на достижение конечной точки
        if player_pos == list(end_pos):
            game_won = True  # Устанавливаем флаг, что игра пройдена


# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    draw_grid()

    # Если игра пройдена, отображаем сообщение
    if game_won:
        message = font.render("Поздравляем! Вы прошли лабиринт!", True, (255, 0, 0))
        screen.blit(message,
                    (WINDOW_SIZE // 2 - message.get_width() // 2, WINDOW_SIZE // 2 - message.get_height() // 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_won:  # Блокируем движение, если игра пройдена
            # Движение с помощью стрелок
            if event.key == pygame.K_UP:
                move_player(0, -1)  # Вверх
            elif event.key == pygame.K_DOWN:
                move_player(0, 1)  # Вниз
            elif event.key == pygame.K_LEFT:
                move_player(-1, 0)  # Влево
            elif event.key == pygame.K_RIGHT:
                move_player(1, 0)  # Вправо

    # Отрисовка экрана
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
