import secrets
from sage.all import is_prime
import timeit


class GenCurveConfig:

    """
    @staticmethod
    def is_prime(n, k=15):
        if n % 2 == 0:
            return False

        d = n - 1
        s = 0

        while d % 2 == 0:
            d //= 2
            s += 1

        for _ in range(k):
            a = secrets.randbelow(n - 2) + 2
            b = pow(a, d, n)
            if b == 1 or b == n - 1:
                continue
            for _ in range(s - 1):
                b = (b * b) % n
                if b == n - 1:
                    break
            else:
                return False
        return True
    """
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
