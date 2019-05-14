# -*- coding:utf-8 -*-

# Can get the LCM value from source

from functools import reduce

from math import gcd



def lcm(a, b):

    return int(a * b / gcd(a, b))



def lcms(*numbers):

    return reduce(lcm, numbers)
a = 1
period = [4,6,8,10,16]
for i in range(len(period)):
    a = lcms(period[i],a)
#a = lcms(period)
print (a)
