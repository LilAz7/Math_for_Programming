import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGraphicsScene, QGraphicsView, \
    QGraphicsRectItem, QMessageBox, QVBoxLayout, QWidget, QTextEdit
from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtGui import QColor, QBrush, QPen

# Параметры игры
GRID_SIZE = 7
CELL_SIZE = 50
FIELD_COLOR = QColor("#FEFDED")
LINE_COLOR = QColor("#C6EBC5")
SHIP_COLOR = QColor("#A1C398")
HIT_COLOR = QColor("#FA7070")
MISS_COLOR = QColor("#F0F0F0")


# Создание игрового окна
class BattleShipGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Морской бой")
        self.setGeometry(100, 100, GRID_SIZE * CELL_SIZE * 2 + 100, GRID_SIZE * CELL_SIZE + 250)

        # Основная настройка
        self.player_field = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.ai_field = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.ai_visible_field = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

        # Состояние игры
        self.player_turn = True
        self.game_over = False
        self.player_shots = 0
        self.ai_shots = 0
        self.history = []

        # Корабли
        self.ships = [3, 2, 1]
        self.player_remaining_ships = sum(self.ships)
        self.ai_remaining_ships = sum(self.ships)

        # Интерфейс
        self.initUI()

    def initUI(self):
        # Настройка виджета для вывода истории и статистики
        self.history_text = QTextEdit(self)
        self.history_text.setReadOnly(True)
        self.history_text.setGeometry(20, GRID_SIZE * CELL_SIZE + 50, GRID_SIZE * CELL_SIZE * 2, 100)

        # Кнопки для выбора режима игры
        self.random_button = QPushButton("Рандомная расстановка", self)
        self.random_button.setGeometry(20, 10, 200, 30)
        self.random_button.clicked.connect(self.setup_random)

        # Создание сцены и добавление на неё графических элементов
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(FIELD_COLOR)
        self.scene_view = QGraphicsView(self.scene, self)
        self.scene_view.setGeometry(20, 50, GRID_SIZE * CELL_SIZE * 2 + 60, GRID_SIZE * CELL_SIZE)

        self.draw_grid(0)
        self.draw_grid(GRID_SIZE * CELL_SIZE + 60)

        self.show()

    def log_shot(self, text):
        """Добавление записи в историю выстрелов."""
        self.history.append(text)
        self.history_text.append(text)

    def draw_grid(self, offset_x=0):
        """Рисование сетки для игрового поля."""
        for i in range(GRID_SIZE + 1):
            self.scene.addLine(offset_x + i * CELL_SIZE, 40, offset_x + i * CELL_SIZE, GRID_SIZE * CELL_SIZE + 40,
                               QPen(LINE_COLOR))
            self.scene.addLine(offset_x, i * CELL_SIZE + 40, offset_x + GRID_SIZE * CELL_SIZE, i * CELL_SIZE + 40,
                               QPen(LINE_COLOR))

    def draw_ships(self, field, offset_x=0, show_ships=False):
        """Отображение кораблей и выстрелов на поле."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1, y1 = offset_x + col * CELL_SIZE, 40 + row * CELL_SIZE
                rect = QRectF(x1, y1, CELL_SIZE, CELL_SIZE)
                if field[row][col] == 1 and show_ships:
                    ship_rect = QGraphicsRectItem(rect)
                    ship_rect.setBrush(QBrush(SHIP_COLOR))
                    ship_rect.setPen(QPen(LINE_COLOR))
                    self.scene.addItem(ship_rect)
                elif field[row][col] == 2:
                    hit_rect = QGraphicsRectItem(rect)
                    hit_rect.setBrush(QBrush(HIT_COLOR))
                    hit_rect.setPen(QPen(LINE_COLOR))
                    self.scene.addItem(hit_rect)
                elif field[row][col] == 3:
                    miss_rect = QGraphicsRectItem(rect)
                    miss_rect.setBrush(QBrush(MISS_COLOR))
                    miss_rect.setPen(QPen(LINE_COLOR))
                    self.scene.addItem(miss_rect)

    def setup_random(self):
        """Настройка рандомной игры."""
        self.clear_fields()
        self.place_random_ships(self.ai_field)
        self.place_random_ships(self.player_field)
        self.draw_ships(self.player_field, show_ships=True)
        self.draw_ships(self.ai_visible_field, offset_x=GRID_SIZE * CELL_SIZE + 60, show_ships=False)
        self.scene_view.mousePressEvent = self.player_shot

    def player_shot(self, event):
        """Выстрел игрока по полю ИИ."""
        if self.game_over or not self.player_turn:
            return
        x = int((event.x() - (GRID_SIZE * CELL_SIZE + 60)) / CELL_SIZE)
        y = int((event.y() - 40) / CELL_SIZE)
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and self.ai_visible_field[y][x] == 0:
            if self.ai_field[y][x] == 1:
                self.ai_visible_field[y][x] = 2
                self.ai_remaining_ships -= 1
                self.log_shot(f"Попадание по координатам ({x}, {y})!")
                self.check_winner()
            else:
                self.ai_visible_field[y][x] = 3
                self.player_turn = False
                self.log_shot(f"Промах по координатам ({x}, {y}).")
            self.player_shots += 1
            self.draw_ships(self.ai_visible_field, offset_x=GRID_SIZE * CELL_SIZE + 60, show_ships=False)
            if not self.player_turn:
                QTimer.singleShot(500, self.ai_turn)

    def ai_turn(self):
        """Ход ИИ. ИИ продолжает стрелять после попадания."""
        if self.game_over:
            return
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if self.player_field[y][x] in [0, 1]:
                break
        if self.player_field[y][x] == 1:
            self.player_field[y][x] = 2
            self.player_remaining_ships -= 1
            self.log_shot(f"ИИ попал по координатам ({x}, {y}).")
            self.check_winner()
            if not self.game_over:
                QTimer.singleShot(500, self.ai_turn)
        else:
            self.player_field[y][x] = 3
            self.player_turn = True
            self.log_shot(f"ИИ промахнулся по координатам ({x}, {y}).")
        self.ai_shots += 1
        self.draw_ships(self.player_field, offset_x=0, show_ships=True)

    def check_winner(self):
        """Проверка победителя и вывод финальной статистики."""
        if self.ai_remaining_ships <= 0:
            self.game_over = True
            QMessageBox.information(self, "Победа!", "Игрок победил!")
            self.log_shot("Победа игрока!")
        elif self.player_remaining_ships <= 0:
            self.game_over = True
            QMessageBox.information(self, "Поражение!", "ИИ победил!")
            self.log_shot("Победа ИИ!")

    def clear_fields(self):
        """Очистка полей и сброс состояния игры."""
        self.player_remaining_ships = sum(self.ships)
        self.ai_remaining_ships = sum(self.ships)
        self.player_shots = 0
        self.ai_shots = 0
        self.game_over = False
        self.history = []
        self.history_text.clear()
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.player_field[i][j] = 0
                self.ai_field[i][j] = 0
                self.ai_visible_field[i][j] = 0
        self.scene.clear()
        self.draw_grid(0)
        self.draw_grid(GRID_SIZE * CELL_SIZE + 60)

    def place_random_ships(self, field):
        """Рандомная расстановка кораблей для ИИ или игрока."""
        for ship_len in self.ships:
            placed = False
            while not placed:
                orientation = random.choice(['horizontal', 'vertical'])
                if orientation == 'horizontal':
                    row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - ship_len)
                    if self.can_place_ship(field, row, col, ship_len, orientation):
                        for i in range(ship_len):
                            field[row][col + i] = 1
                        placed = True
                else:
                    row, col = random.randint(0, GRID_SIZE - ship_len), random.randint(0, GRID_SIZE - 1)
                    if self.can_place_ship(field, row, col, ship_len, orientation):
                        for i in range(ship_len):
                            field[row + i][col] = 1
                        placed = True

    def can_place_ship(self, field, row, col, ship_len, orientation):
        """Проверка на возможность размещения корабля с учетом отступа."""
        for i in range(ship_len):
            if orientation == 'horizontal':
                if col + i >= GRID_SIZE or field[row][col + i] != 0:
                    return False
            else:
                if row + i >= GRID_SIZE or field[row + i][col] != 0:
                    return False
        for r in range(row - 1, row + (ship_len if orientation == 'vertical' else 1) + 1):
            for c in range(col - 1, col + (ship_len if orientation == 'horizontal' else 1) + 1):
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and field[r][c] == 1:
                    return False
        return True


# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = BattleShipGame()
    sys.exit(app.exec_())
