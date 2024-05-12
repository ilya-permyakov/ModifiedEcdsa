from Point import Point
from BasePoint import BasePoint
import time


def measure_time(operation, *args, repetitions=1000):
    start_time = time.perf_counter_ns()
    for _ in range(repetitions):
        operation(*args)
    end_time = time.perf_counter_ns()
    elapsed_time_ns = end_time - start_time
    average_time_us = (elapsed_time_ns / repetitions) / 1000
    return f"{average_time_us:.3f}"


# Базовые арифметические операции
def add(x, y, p):
    return (x + y) % p


def subtract(x, y, p):
    return (x - y) % p


def multiply(x, y, p):
    return (x * y) % p


def multiplicative_inverse(x, p):
    return pow(x, -1, p)


params = {'a': -3, 'b': 41058363725152142129326129780047268409114441015993725554835256314039467401291,
          'p': 115792089210356248762697446949407573530086143415290314195533631308867097853951}

x = 4383487845893
y = 8943223903485

print("Сложение:", measure_time(add, x, y, params['p']), "мкс")
print("Вычитание:", measure_time(subtract, x, y, params['p']), "мкс")
print("Умножение:", measure_time(multiply, x, y, params['p']), "мкс")
print("Мультипликативный обратный:", measure_time(multiplicative_inverse, x, params['p']), "мкс")

points = BasePoint(params)
point1 = points.find_random_point()
point2 = points.find_random_point()

print("Сложение точек:", measure_time(point1.add, point2), "мкс")
print("Скалярное умножение точек:", measure_time(point1.mult, point1, 4), "мкс")
