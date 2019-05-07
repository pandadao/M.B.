# -*- coding:utf-8 -*-

# Can get the LCM value from source

from functools import reduce

from math import gcd



def lcm(a, b):

    return int(a * b / gcd(a, b))



def lcms(*numbers):

    return reduce(lcm, numbers)

a = lcms(3,4,5)
print (a)
