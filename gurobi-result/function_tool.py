# 找出不重複的所有解
import copy

def combine(l,n):
    answer = []
    one = [0]*n
    
    def next_c(li = 0, ni = 0):
        if ni == n:
            answer.append(copy.copy(one))
            return
        for lj in range(li, len(l)):
            one[ni] = l[lj]
            next_c(lj+1, ni+1)
    next_c()
    return answer


#找出LCM公式
from functools import reduce
from math import gcd

def lcm(a,b):
    return int(a*b /gcd(a,b))

def lcms(*numbers):
    return reduce(lcm, numbers)


def read_tt_information():

    n = 0
    for i in fp:
        globals()["tt{}".format(n+1)] = []
        a = "tt"+ str(n)
        tti = eval(a)
        period, length, number = i.split(" ")
        tti.append(period)
        tti.append(length)
        tti.append(number)
        n = n+1
        print(eval(tti[2]))
