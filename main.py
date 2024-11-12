import tkinter as tk
import math


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Научный калькулятор")
        self.expression = ""
        self.input_var = tk.StringVar()

        # Настройки цвета
        self.root.configure(bg="#EAEAE5")  

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.root, bg="#EAEAE5")
        input_frame.pack(pady=10)

        input_field = tk.Entry(input_frame, textvariable=self.input_var, font=('Arial', 16), width=30, bd=5,
                               insertwidth=2, borderwidth=4)
        input_field.grid(row=0, column=0, padx=5)
        input_field.configure(bg="#FFFFFF")  # Белый фон для поля ввода

        button_frame = tk.Frame(self.root, bg="#EAEAE5")
        button_frame.pack()

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2),
            ('(', 5, 3), (')', 6, 0), ('pi', 6, 1)
        ]

        for (text, row, column) in buttons:
            button = tk.Button(button_frame, text=text, padx=15, pady=15, font=('Arial', 14),
                               command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=column, padx=5, pady=5)
            button.configure(bg="#C6A57A", fg="#FFFFFF", relief='groove', bd=2)
            button.bind("<Enter>", lambda e: e.widget.configure(bg="#D8B69B"))  # Цвет при наведении
            button.bind("<Leave>", lambda e: e.widget.configure(bg="#C6A57A"))  # Цвет при уходе

        # Угол кнопок
        for btn in button_frame.winfo_children():
            btn.config(width=4, height=2)
            btn.config(borderwidth=0, highlightthickness=0)
            btn.config(activebackground="#D8B69B")  # Цвет при нажатии

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.input_var.set("")
        elif char == '=':
            self.calculate_result()
        else:
            self.expression += char
            self.input_var.set(self.expression)

    def calculate_result(self):
        try:
            # Заменяем 'pi' на значение числа
            expression = self.expression.replace('pi', str(math.pi))

            # Обработка тригонометрических функций
            if 'sin' in expression:
                expression = expression.replace('sin', 'math.sin')
            if 'cos' in expression:
                expression = expression.replace('cos', 'math.cos')
            if 'tan' in expression:
                expression = expression.replace('tan', 'math.tan')

            # Вычисление результата
            result = eval(expression)
            self.input_var.set(result)
            self.expression = str(result)  # сохраняем результат для дальнейших вычислений
        except Exception as e:
            self.input_var.set("Ошибка")
            self.expression = ""


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
