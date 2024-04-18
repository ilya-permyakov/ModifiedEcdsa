from BasePoint import BasePoint
from CurveConfig import GenCurveConfig
from Point import Point
import random


class ModifiedECDSA:
    def __init__(self, curve, base_point, subgroup_order):
        self.curve = curve
        self.base_point = base_point
        self.subgroup_order = subgroup_order

    def gen_keys(self):
        d = random.randint(1, self.subgroup_order - 1)
        print('d = ', d)
        print('subgroup_order = ', self.subgroup_order)
        print('base_point = ', self.base_point.x, self.base_point.y)
        Q = self.base_point.mult(self.base_point, pow(d, -1, self.subgroup_order))
        return d, Q


params = GenCurveConfig().generate_params()
print(params)
base_point, subgroup_order = BasePoint(params).find_base_point()
ecdsa = ModifiedECDSA(params, base_point, subgroup_order)
result = ecdsa.gen_keys()
print('subgroup_order = ', subgroup_order, 'd = ', result[0], 'x = ', result[1].x, 'y = ', result[1].y)
