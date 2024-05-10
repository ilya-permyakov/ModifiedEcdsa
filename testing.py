from Point import Point
from ModifiedEcdsa import ModifiedECDSA
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
        start_sign = time.perf_counter_ns()
        signature = orig_ecdsa.gen_sign(keys, data)
        end_sign = time.perf_counter_ns()
        sign_times.append((end_sign - start_sign) / 1e6)

        start_verify = time.perf_counter_ns()
        verify = orig_ecdsa.verification(data, signature, keys['Q'])
        end_verify = time.perf_counter_ns()
        verify_times.append((end_verify - start_verify) / 1e6)

    return statistics.mean(sign_times), statistics.mean(verify_times)


def test_my_ecdsa(curve, base_point, iterations):
    my_ecdsa = ModifiedECDSA(curve, base_point)
    keys = my_ecdsa.gen_keys()

    data = "/mnt/d/vkr/ModifiedEcdsa/test.txt"

    sign_times = []
    verify_times = []
    for _ in range(iterations):
        start_sign = time.perf_counter_ns()
        signature = my_ecdsa.gen_sign(keys, data)
        end_sign = time.perf_counter_ns()
        sign_times.append((end_sign - start_sign) / 1e6)

        start_verify = time.perf_counter_ns()
        verify = my_ecdsa.verification(data, signature, keys['Q'])
        end_verify = time.perf_counter_ns()
        verify_times.append((end_verify - start_verify) / 1e6)

    return statistics.mean(sign_times), statistics.mean(verify_times)


iter = 100
# params = GenCurveConfig().generate_params()
# G = BasePoint(params).find_base_point()
# params = {'a': 94, 'b': 134, 'p': 44216873401415158701553181970864582114607005578873503324380671624288035740323}
# G = {'base_point': Point(12317735490499994716251161198116947244326069763492380038307986727286914863496,
#                          39941234683063600542318056013589489742147132847289021868764112299247229235796),
#      'subgroup_order': 12383874154785912327384145814604689492670649296007897293317}
params = {'a': -3, 'b': 41058363725152142129326129780047268409114441015993725554835256314039467401291,
          'p': 115792089210356248762697446949407573530086143415290314195533631308867097853951}
G = {'base_point': Point(48439561293906451759052585252797914202762949526041747995844080717082404635286,
                         36134250956749795798585127919587881956611106672985015071877198253568414405109),
     'subgroup_order': 115792089210356248762697446949407573529996955224135760342422259061068512044369}
original_ecdsa_sign_avg, original_ecdsa_verify_avg = test_original_ecdsa(params, G, iter)
my_ecdsa_sign_avg, my_ecdsa_verify_avg = test_my_ecdsa(params, G, iter)
improvement_sign = ((original_ecdsa_sign_avg - my_ecdsa_sign_avg) / original_ecdsa_sign_avg) * 100
improvement_verify = ((original_ecdsa_verify_avg - my_ecdsa_verify_avg) / original_ecdsa_verify_avg) * 100
print(f"ECDSA average sign time: {original_ecdsa_sign_avg:.7f} ms")
print(f"ECDSA average verify time: {original_ecdsa_verify_avg:.7f} ms")
print(f"Modified ECDSA average sign time: {my_ecdsa_sign_avg:.7f} ms")
print(f"Modified ECDSA average verify time: {my_ecdsa_verify_avg:.7f} ms")
print(f"Improvement in signing time: {improvement_sign:.2f}%")
print(f"Improvement in verification time: {improvement_verify:.2f}%")


'''
result
ECDSA Average Sign Time: 23.1349993 ms
ECDSA Average Verify Time: 42.0900435 ms
My ECDSA Average Sign Time: 20.4137432 ms
My ECDSA Average Verify Time: 35.1436649 ms
Improvement in Signing Time: 11.76%
Improvement in Verification Time: 16.50%
'''