import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


def plot_elliptic_curve(a, b, p):
    x_vals = []
    y_vals = []

    for x in range(p):
        for y in range(p):
            if (y * y - x * x * x - a * x - b) % p == 0:
                x_vals.append(x)
                y_vals.append(y)

    plt.scatter(x_vals, y_vals, label=f"$y^2 = (x^3  {a}x + {b})$ mod {p}", s=100)
    # plt.title("Elliptic Curve")
    plt.legend(fontsize='x-large', loc='upper right')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


def plot_elliptic_curve_normal():
    # Диапазон значений x
    x = np.linspace(-3, 3, 3000)

    # Рассчитываем значения под корнем
    y_squared = x ** 3 - 3 * x + 3

    # Инициализируем y как массив комплексных чисел
    y = np.sqrt(y_squared + 0j)

    # Реальная и мнимая части
    y_real = y.real
    y_imag = y.imag

    # Только реальные значения y (где мнимая часть равна 0)
    real_mask = (y_imag == 0)

    x_real = x[real_mask]
    y_real = y_real[real_mask]

    # Построение графика
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_real, y_real, 'black', label=f"$y^2 = x^3 - 3x + 3$")
    ax.plot(x_real, -y_real, 'black')

    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)

        # Установка осей через (0, 0)
    ax.spines['bottom'].set_position('zero')
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_position('zero')
    ax.spines['left'].set_visible(True)

    # Убираем верхние и правые тики
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Добавляем стрелки на оси
    ax.plot((1), (0), ls="", marker=">", ms=10, color="black", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot((0), (1), ls="", marker="^", ms=10, color="black", transform=ax.get_xaxis_transform(), clip_on=False)

    # Убираем деления на осях
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])

    # Добавляем ноль в начале координат
    ax.text(-0.03, -0.1, '0', verticalalignment='top', horizontalalignment='right', fontsize=15)

    # Настройка меток на осях
    ax.set_xlabel('x', loc='right')  # Устанавливаем метку x у края оси
    ax.set_ylabel('y', loc='top', rotation=0)  # Устанавливаем метку y вертикально у верха оси
    # plt.title('Graph of $y^2 = x^3 - 3x + 3$')
    # plt.xlabel('x')
    # plt.ylabel('y')

    # plt.axhline(0, color='black', linewidth=1)
    # plt.axvline(0, color='black', linewidth=1)
    # plt.grid(True)
    plt.legend(fontsize='large', loc='upper right')
    plt.show()


def plot_torus(R=1, r=0.3):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, 2 * np.pi, 100)
    u, v = np.meshgrid(u, v)

    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)

    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_zlim(-3, 3)
    ax1.plot_surface(x, y, z, rstride=5, cstride=5, color='k', edgecolors='w')
    plt.show()


def plot_elliptic_curve_on_torus(a, b, p, R=1, r=0.2):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Generate torus
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, 2 * np.pi, 100)
    u, v = np.meshgrid(u, v)
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    ax.plot_surface(x, y, z, color='b', alpha=0.3)

    # Generate points on elliptic curve
    theta_vals = []
    phi_vals = []
    for x in range(p):
        for y in range(p):
            if (y * y - x * x * x - a * x - b) % p == 0:
                theta = 2 * np.pi * x / p
                phi = 2 * np.pi * y / p
                theta_vals.append(theta)
                phi_vals.append(phi)

    # Map points to torus
    x_vals = (R + r * np.cos(phi_vals)) * np.cos(theta_vals)
    y_vals = (R + r * np.cos(phi_vals)) * np.sin(theta_vals)
    z_vals = r * np.sin(phi_vals)
    ax.scatter(x_vals, y_vals, z_vals, color='r')

    plt.show()


# plot_elliptic_curve_on_torus(-3, 3, 13)

# plot_torus()

# plot_elliptic_curve(-3, 3, 13)

plot_elliptic_curve_normal()
