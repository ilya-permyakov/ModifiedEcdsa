import secrets
from sage.all import is_prime
import timeit


class GenCurveConfig:
    @staticmethod
    def generate_prime():
        start_time = timeit.default_timer()
        while True:
            p = secrets.randbits(256)
            if is_prime(p):
                end_time = timeit.default_timer()
                print(f"Время генерации простого числа: {end_time - start_time} секунд.")
                return p

    def generate_params(self):
        start_time = timeit.default_timer()
        p = self.generate_prime()

        while True:
            a = secrets.randbelow(150) + 1
            b = secrets.randbelow(150) + 1
            if (4 * a ** 3 + 27 * b ** 2) % p != 0:
                end_time = timeit.default_timer()
                print(f"Время генерации параметров: {end_time - start_time} секунд.")
                return {'a': a, 'b': b, 'p': p}
