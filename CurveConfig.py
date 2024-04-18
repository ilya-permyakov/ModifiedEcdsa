import random


class GenCurveConfig:
    def __init__(self, max_value=2000):
        self.max_value = max_value

    @staticmethod
    def is_prime(n, k=15):
        if n <= 3:
            raise Exception('n should be greater than 3.')
        if n % 2 == 0:
            return False
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        for _ in range(k):
            a = random.randint(2, n - 2)
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

    def generate_prime(self):
        while True:
            p = random.randint(2, self.max_value)
            if self.is_prime(p):
                return p

    def generate_params(self):
        p = self.generate_prime()
        while True:
            a = random.randint(1, self.max_value)
            b = random.randint(1, self.max_value)
            if (4 * a ** 3 + 27 * b ** 2) % p != 0:
                return {'a': a, 'b': b, 'p': p}

