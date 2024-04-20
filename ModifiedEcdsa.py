from BasePoint import BasePoint
from CurveConfig import GenCurveConfig
from Point import Point
import secrets
from hashlib import sha3_256
import timeit


class ModifiedECDSA:
    def __init__(self, curve, G):
        self.curve = curve
        self.base_point = G['base_point']
        self.subgroup_order = int(G['subgroup_order'])

    @staticmethod
    def hash_string_to_int(message):
        hash_obj = sha3_256(message.encode())
        hex_dig = hash_obj.hexdigest()
        num = int(hex_dig, 16)
        return num

    def gen_keys(self):
        d = secrets.randbelow(self.subgroup_order - 1) + 1
        Q = self.base_point.mult(self.base_point, pow(d, -1, self.subgroup_order))
        return {'d': d, 'Q': Q}

    def gen_sign(self, keys, message):
        start_time = timeit.default_timer()
        k = secrets.randbelow(self.subgroup_order - 1) + 1
        P = self.base_point.mult(self.base_point, k)
        r = P.x % self.subgroup_order
        s = (keys['d'] * (k - self.hash_string_to_int(message))) % self.subgroup_order
        end_time = timeit.default_timer()
        print(f"Время генерации подписи: {end_time - start_time} секунд.")
        return {'r': r, 's': s, 'Q': keys['Q']}

    def verification(self, params, message, sign, base_point):
        start_time = timeit.default_timer()
        if base_point['subgroup_order'] < sign['r'] < 1 and base_point['subgroup_order'] < sign['s'] < 1:
            print('Sign is a fake')
            return 1
        u1 = sign['s'] % base_point['subgroup_order']
        u2 = self.hash_string_to_int(message) % base_point['subgroup_order']
        A = Point.add(sign['Q'].mult(sign['Q'], u1), base_point['base_point'].mult(base_point['base_point'], u2))
        if sign['r'] == A.x % base_point['subgroup_order']:
            print('OK!')
            end_time = timeit.default_timer()
            print(f"Время проверки подписи: {end_time - start_time} секунд.")
            return 0
        else:
            print('Sign is a fake')
            end_time = timeit.default_timer()
            print(f"Время проверки подписи: {end_time - start_time} секунд.")
            return 1


'''
params = GenCurveConfig().generate_params()
print(params)
G = BasePoint(params).find_base_point()
ecdsa = ModifiedECDSA(params, G)
m = 'Hello, World!'
m2 = 'Hello World!'
keys = ecdsa.gen_keys()
sign = ecdsa.gen_sign(keys, m)
verif = ecdsa.verification(params, m, sign, G)
'''
