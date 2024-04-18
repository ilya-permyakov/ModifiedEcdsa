import random
from Point import Point
from CurveConfig import GenCurveConfig


class BasePoint:
    def __init__(self, curve):
        self.curve = curve

    def tonelli_shanks(self, n):
        p = self.curve['p']
        assert pow(n, (p - 1) // 2, p) == 1
        q = p - 1
        s = 0
        while q % 2 == 0:
            q //= 2
            s += 1
        if s == 1:
            return pow(n, (p + 1) // 4, p)
        for z in range(2, p):
            if p - 1 == pow(z, (p - 1) // 2, p):
                break
        c = pow(z, q, p)
        r = pow(n, (q + 1) // 2, p)
        t = pow(n, q, p)
        m = s
        while t != 1:
            i = 0
            tmp = t
            while tmp != 1:
                tmp = tmp * tmp % p
                i += 1
            b = pow(c, 1 << (m - i - 1), p)
            r = r * b % p
            c = b * b % p
            t = t * c % p
            m = i
        return r

    def find_random_point(self):
        while True:
            x = random.randint(1, self.curve['p'])
            y_squared = (x ** 3 + self.curve['a'] * x + self.curve['b']) % self.curve['p']
            y = self.tonelli_shanks(y_squared)
            if y is not None and ((y * y - y_squared) % self.curve['p'] == 0):
                return Point(x, y, self.curve)

    # def find_base_point(self):


params = GenCurveConfig().generate_params()
q = BasePoint(params).find_random_point()
print(q.curve, q.x, q.y)
