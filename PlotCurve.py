import matplotlib.pyplot as plt


def plot_curve(curve_params):
    p = curve_params['p']
    a = curve_params['a']
    b = curve_params['b']

    for x in range(p):
        for y in range(p):
            if (y ** 2 - x ** 3 - a * x - b) % p == 0:
                plt.scatter(x, y, s=1)

    plt.show()
