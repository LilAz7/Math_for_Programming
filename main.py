import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import Qt  # Добавьте этот импорт

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Научный калькулятор")
        self.setGeometry(100, 100, 300, 400)

        # Создаем строку для отображения ввода/вывода
        self.input_line = QLineEdit(self)
        self.input_line.setFixedHeight(40)
        self.input_line.setReadOnly(True)
        self.input_line.setAlignment(Qt.AlignRight)  # Теперь это работает
        self.input_line.setStyleSheet("font-size: 20px;")

        # Основной виджет и компоновка
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_line)

        # Добавление кнопок
        button_layout = QGridLayout()
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('C', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('sin', 4, 0), ('cos', 4, 1), ('tan', 4, 2), ('pi', 4, 3)
        ]

        # Создаем кнопки и добавляем их в сетку
        for (text, row, col) in buttons:
            button = QPushButton(text)
            button.setFixedSize(60, 60)
            button_layout.addWidget(button, row, col)
            button.clicked.connect(lambda ch, text=text: self.on_button_click(text))

        # Добавляем layout для кнопок в основной layout
        main_layout.addLayout(button_layout)

        # Настройка центрального виджета
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Переменная для хранения выражения
        self.expression = ""

    def on_button_click(self, char):
        if char == 'C':
            # Очистка экрана
            self.expression = ""
            self.input_line.setText("")
        elif char == '=':
            # Вычисление результата
            self.calculate_result()
        elif char == 'pi':
            # Вставка значения числа π
            self.expression += str(math.pi)
            self.input_line.setText(self.expression)
        elif char in ('sin', 'cos', 'tan'):
            # Обработка тригонометрических функций
            self.expression += f"math.{char}("
            self.input_line.setText(self.expression)
        else:
            # Добавляем нажатую кнопку к выражению
            self.expression += char
            self.input_line.setText(self.expression)

    def calculate_result(self):
        try:
            # Вычисление выражения с использованием eval
            result = eval(self.expression)
            self.input_line.setText(str(result))
            self.expression = str(result)  # сохраняем результат для дальнейших вычислений
        except Exception:
            self.input_line.setText("Ошибка")
            self.expression = ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
