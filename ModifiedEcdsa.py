from Point import Point
import secrets
from hashlib import sha3_256


class ModifiedECDSA:
    def __init__(self, curve, G):
        self.curve = curve
        self.base_point = Point(G['base_point'].x, G['base_point'].y, curve)
        self.subgroup_order = int(G['subgroup_order'])

    @staticmethod
    def hash_string_to_int(message):
        hash_obj = sha3_256(message.encode())
        hex_dig = hash_obj.hexdigest()
        num = int(hex_dig, 16)
        return num

    @staticmethod
    def hash_file_to_int(filename):
        with open(filename, 'rb') as f:
            file_content = f.read()
        hash_obj = sha3_256(file_content)
        hex_dig = hash_obj.hexdigest()
        num = int(hex_dig, 16)
        return num

    def gen_keys(self):
        d = secrets.randbelow(self.subgroup_order - 1) + 1
        d_1 = pow(d, -1, self.subgroup_order)
        Q = self.base_point.mult(self.base_point, d_1)
        return {'d': d, 'Q': Q}

    def gen_sign(self, keys, file):
        k = secrets.randbelow(self.subgroup_order - 1) + 1
        P = self.base_point.mult(self.base_point, k)
        r = P.x % self.subgroup_order
        s = (keys['d'] * (k - self.hash_file_to_int(file))) % self.subgroup_order
        return {'r': r, 's': s}

    def verification(self, file, sign, public_key):
        if self.subgroup_order < sign['r'] < 1 and self.subgroup_order < sign['s'] < 1:
            result = 'Подпись неверна'
            return result
        u1 = sign['s'] % self.subgroup_order
        u2 = self.hash_file_to_int(file) % self.subgroup_order
        A = Point.add(public_key.mult(public_key, u1), self.base_point.mult(self.base_point, u2))
        if sign['r'] == A.x % self.subgroup_order:
            result = 'Подпись верна'
            return result
        else:
            result = 'Подпись неверна'
            return result
