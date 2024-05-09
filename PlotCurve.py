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

    plt.scatter(x_vals, y_vals)
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


plot_elliptic_curve_on_torus(-3, 3, 13)

# plot_torus()

# plot_elliptic_curve(-3, 3, 13)
