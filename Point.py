class Point:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def is_equality(self, point):
        return self.x == point.x and self.y == point.y

    def add(self, point):
        if self.x == 0 and self.y == 0:
            return point
        elif point.x == 0 and point.y == 0:
            return self

        p = self.curve['p']
        a = self.curve['a']

        if self.is_equality(point):
            if 2 * point.y % p == 0:
                return Point(float('inf'), float('inf'), self.curve)
            lambd = (3 * point.x ** 2 + a) * pow(2 * point.y, -1, p) % p
        else:
            if point.x - self.x % p == 0:
                return Point(float('inf'), float('inf'), self.curve)
            lambd = (point.y - self.y) * pow(point.x - self.x, -1, p) % p

        x = (lambd ** 2 - self.x - point.x) % p
        y = (lambd * (self.x - x) - self.y) % p

        return Point(x, y, self.curve)

    def mult(self, point, k):
        result = Point(0, 0, self.curve)

        binary_k = bin(k)[2:]

        for bit in binary_k:
            result = result.add(result)
            if bit == '1':
                result = result.add(point)

        return result

