import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

# Создаем массив значений x в диапазоне [-2, 2]
x = np.linspace(-5, 5, 400)

# Вычисляем значения y
y = np.sqrt(x**3 - 3*x + 3)

# Рисуем график
plt.plot(x, y, color='black', label='y^2 = x^3 - 3x + 3')
plt.plot(x, -y, color='black')

# Добавляем подписи к осям
plt.xlabel('Ось X')
plt.ylabel('Ось Y')

# Добавляем стрелки на осях
plt.annotate('', xy=(max(x), 0), xytext=(min(x), 0),
             arrowprops=dict(facecolor='black', arrowstyle='<|-|>'))
plt.annotate('', xy=(0, max(y)), xytext=(0, min(y)),
             arrowprops=dict(facecolor='black', arrowstyle='<|-|>'))

# Подписываем начало координат
plt.text(0, 0, '(0, 0)', ha='right')

# Добавляем легенду
plt.legend()

# Отображаем график
plt.grid(True)
plt.show()
