from Point import Point
from ModifiedEcdsa import ModifiedECDSA
from CurveConfig import GenCurveConfig
from BasePoint import BasePoint
import secrets
from hashlib import sha3_256
import statistics
import time


class OriginalECDSA:
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
        Q = self.base_point.mult(self.base_point, d)
        return {'d': d, 'Q': Q}

    def gen_sign(self, keys, file):
        k = secrets.randbelow(self.subgroup_order - 1) + 1
        P = self.base_point.mult(self.base_point, k)
        r = P.x % self.subgroup_order
        s = (pow(k, -1, self.subgroup_order) * (self.hash_file_to_int(file) + keys['d'] * r)) % self.subgroup_order
        return {'r': r, 's': s}

    def verification(self, file, sign, public_key):
        if self.subgroup_order < sign['r'] < 1 and self.subgroup_order < sign['s'] < 1:
            result = 'Подпись неверна'
            return result
        u1 = pow(sign['s'], -1, self.subgroup_order) * self.hash_file_to_int(file) % self.subgroup_order
        u2 = sign['r'] * pow(sign['s'], -1, self.subgroup_order) % self.subgroup_order
        A = Point.add(public_key.mult(public_key, u2), self.base_point.mult(self.base_point, u1))
        if sign['r'] == A.x % self.subgroup_order:
            result = 'Подпись верна'
            return result
        else:
            result = 'Подпись неверна'
            return result


def test_original_ecdsa(curve, base_point, iterations):
    orig_ecdsa = OriginalECDSA(curve, base_point)
    keys = orig_ecdsa.gen_keys()

    data = "/mnt/d/vkr/ModifiedEcdsa/test.txt"

    sign_times = []
    verify_times = []
    for _ in range(iterations):
        start_sign = time.perf_counter()
        signature = orig_ecdsa.gen_sign(keys, data)
        end_sign = time.perf_counter()
        sign_times.append(end_sign - start_sign)

        start_verify = time.perf_counter()
        verify = orig_ecdsa.verification(data, signature, keys['Q'])
        end_verify = time.perf_counter()
        verify_times.append(end_verify - start_verify)

    return statistics.mean(sign_times), statistics.mean(verify_times)


def test_my_ecdsa(curve, base_point, iterations):
    my_ecdsa = ModifiedECDSA(curve, base_point)
    keys = my_ecdsa.gen_keys()

    data = "/mnt/d/vkr/ModifiedEcdsa/test.txt"

    sign_times = []
    verify_times = []
    for _ in range(iterations):
        start_sign = time.perf_counter()
        signature = my_ecdsa.gen_sign(keys, data)
        end_sign = time.perf_counter()
        sign_times.append(end_sign - start_sign)

        start_verify = time.perf_counter()
        verify = my_ecdsa.verification(data, signature, keys['Q'])
        end_verify = time.perf_counter()
        verify_times.append(end_verify - start_verify)

    return statistics.mean(sign_times), statistics.mean(verify_times)


iter = 100
params = GenCurveConfig().generate_params()
G = BasePoint(params).find_base_point()
original_ecdsa_sign_avg, original_ecdsa_verify_avg = test_original_ecdsa(params, G, iter)
my_ecdsa_sign_avg, my_ecdsa_verify_avg = test_my_ecdsa(params, G, iter)
print(f"ECDSA Average Sign Time: {original_ecdsa_sign_avg:.7f} seconds")
print(f"ECDSA Average Verify Time: {original_ecdsa_verify_avg:.7f} seconds")
print(f"My ECDSA Average Sign Time: {my_ecdsa_sign_avg:.7f} seconds")
print(f"My ECDSA Average Verify Time: {my_ecdsa_verify_avg:.7f} seconds")
