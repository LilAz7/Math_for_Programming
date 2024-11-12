import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Размер сетки
grid_size = 100
# Параметры волны
speed_of_wave = 1  # скорость распространения волны
frequency = 1  # частота волны
amplitude = 1  # амплитуда волны
time_steps = 100  # количество кадров анимации

# Создаем двумерную сетку
x = np.linspace(-50, 50, grid_size)
y = np.linspace(-50, 50, grid_size)
X, Y = np.meshgrid(x, y)

# Функция для вычисления амплитуды волны в каждой точке пространства на текущем шаге времени
def wave_amplitude(t):
    # Рассчитываем радиус от центра
    R = np.sqrt(X**2 + Y**2)
    # Амплитуда волны на каждом шаге времени (синусоидальная волна)
    return amplitude * np.sin(2 * np.pi * frequency * (t - R / speed_of_wave))

# Инициализация графика
fig, ax = plt.subplots()
# Начальный кадр
im = ax.imshow(wave_amplitude(0), extent=(-50, 50, -50, 50), animated=True, cmap='viridis')
ax.set_title("Распространение волны")

# Функция обновления кадра анимации
def update(t):
    im.set_array(wave_amplitude(t))
    return [im]

# Создание анимации
ani = FuncAnimation(fig, update, frames=np.linspace(0, 10, time_steps), interval=100, blit=True)

# Показ анимации
plt.show()
