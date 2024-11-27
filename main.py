import pygame
import random
import heapq

WINDOW_SIZE = 500
GRID_SIZE = 20
ROWS = WINDOW_SIZE // GRID_SIZE
COLS = WINDOW_SIZE // GRID_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 191, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

WALL = 1
OPEN = 0
DANGER = 2
TELEPORT = 3
FREEZE = 4

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Pathfinding with Obstacles")
font = pygame.font.Font(None, 36)

maze = [[WALL for _ in range(COLS)] for _ in range(ROWS)]
start_pos = (1, 1)
end_pos = (COLS - 2, ROWS - 2)

def generate_maze(x, y):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)
    maze[y][x] = OPEN
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == WALL:
            maze[ny][nx] = OPEN
            maze[y + dy // 2][x + dx // 2] = OPEN
            generate_maze(nx, ny)

generate_maze(start_pos[0], start_pos[1])
maze[start_pos[1]][start_pos[0]] = OPEN
maze[end_pos[1]][end_pos[0]] = OPEN

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
            if 0 <= neighbor[0] < COLS and 0 <= neighbor[1] < ROWS and maze[neighbor[1]][neighbor[0]] != WALL:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

optimal_path = a_star_search(maze, start_pos, end_pos)

player_pos = list(start_pos)
real_path = []
steps_taken = 0
game_won = False
freeze_steps = 0

def add_obstacles():
    for _ in range(5):  # Опасные
        x, y = random.randint(1, COLS - 2), random.randint(1, ROWS - 2)
        if maze[y][x] == OPEN and (x, y) not in [start_pos, end_pos]:
            maze[y][x] = DANGER

    for _ in range(2):  # Телепорты
        x, y = random.randint(1, COLS - 2), random.randint(1, ROWS - 2)
        if maze[y][x] == OPEN and (x, y) not in [start_pos, end_pos]:
            maze[y][x] = TELEPORT

    for _ in range(2):  # Замораживающие
        x, y = random.randint(1, COLS - 2), random.randint(1, ROWS - 2)
        if maze[y][x] == OPEN and (x, y) not in [start_pos, end_pos]:
            maze[y][x] = FREEZE

add_obstacles()

def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            color = WHITE if maze[y][x] == OPEN else BLACK
            if maze[y][x] == DANGER:
                color = RED
            elif maze[y][x] == TELEPORT:
                color = ORANGE
            elif maze[y][x] == FREEZE:
                color = CYAN

            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            if (x, y) == start_pos:
                pygame.draw.rect(screen, BLUE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            if (x, y) == end_pos:
                pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def move_player(dx, dy):
    global freeze_steps, player_pos, steps_taken
    if freeze_steps > 0:
        freeze_steps -= 1
        return

    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy

    if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] != WALL:
        player_pos[0] = new_x
        player_pos[1] = new_y
        real_path.append((new_x, new_y))
        steps_taken += 1

        handle_obstacle()

def handle_obstacle():
    global player_pos, freeze_steps
    x, y = player_pos
    if maze[y][x] == DANGER:
        print("Опасное препятствие! Возврат на старт.")
        player_pos = list(start_pos)
    elif maze[y][x] == TELEPORT:
        print("Телепорт!")
        while True:
            tx, ty = random.randint(1, COLS - 2), random.randint(1, ROWS - 2)
            if maze[ty][tx] == OPEN:
                player_pos = [tx, ty]
                break
    elif maze[y][x] == FREEZE:
        print("Замораживающее препятствие! Заморозка на 3 хода.")
        freeze_steps = 3

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    draw_grid()

    if tuple(player_pos) == end_pos:
        game_won = True

    pygame.draw.rect(screen, BLUE, (player_pos[0] * GRID_SIZE, player_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    if game_won:
        text = font.render("Путь найден!", True, YELLOW)
        screen.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, WINDOW_SIZE // 2 - text.get_height() // 2))
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
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
