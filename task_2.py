import numpy as np
import matplotlib.pyplot as plt

# Параметры спирали
a = 1  # коэффициент масштаба
b = 0.1  # коэффициент роста
theta = np.linspace(0, 4 * np.pi, 1000)  # углы от 0 до 4π (для нескольких витков)

# Вычисляем координаты точки на спирали
r = a * np.exp(b * theta)  # радиус
x = r * np.cos(theta)  # декартова координата x
y = r * np.sin(theta)  # декартова координата y

# Визуализация спирали
plt.figure(figsize=(6, 6))
plt.plot(x, y, label="Логарифмическая спираль", color='b')
plt.title("Логарифмическая спираль")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.axis("equal")
plt.legend()
plt.show()
