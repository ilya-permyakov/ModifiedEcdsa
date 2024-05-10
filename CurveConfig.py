import secrets
from sage.all import is_prime


class GenCurveConfig:
    @staticmethod
    def generate_prime():
        while True:
            p = secrets.randbits(256)
            if is_prime(p):
                return p

    def generate_params(self):
        p = self.generate_prime()

        while True:
            a = secrets.randbelow(150) + 1
            b = secrets.randbelow(150) + 1
            if (4 * a ** 3 + 27 * b ** 2) % p != 0:
                return {'a': a, 'b': b, 'p': p}
