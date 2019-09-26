# -*- coding:utf-8 -*-
'''
third-party tool, install from web guide
'''
from gurobipy import *
import time
import numpy as np
from operator import itemgetter
import math

'''
self develop function, package together
'''
from ecmp import *
from function_tool import combine, lcms
from getport import *


#通用變數區
M = 100000          # gurobi運算中的or所需之極大值,代替cplex中的either-or功能
e = 0.0001       #gurobi運算中!=所需要的運算子
hyper_period = 1    # 所以TT flow的lcm
IFG = 96            # inter frame gap , fixed number,單位是bit, 假設在1Gpbs上運行則是0.096us, 100M => 0.96 us
obj = 0.0           # 目標式參數
interframegap = 0.096
send_src = []       # 紀錄host發送端
path_node = []      # 紀錄哪些結點是中繼的switch

#將tt資訊讀取出來並存成陣列
n = 0
tmp_list = []
tt_count = []

not_sorted_link = []# 紀錄尚未進行排程的link
link_dict = {}

start_time = time.time()


#搜尋出所有的host,並宣告該host所需的dict變數
allhost = []
hostnode = []
for i in topology_3:
    allhost.append(i)
print(allhost)
for i in allhost:
    try:
        if topology_3[i]['MAC']:
            hostnode.append(i)
            globals()["{}".format(str(i))] = []

        else:
            pass
    except :
        pass
print(hostnode)


#讀取所有TT flow資訊並紀錄
fp = open('Limited_flow_data.txt', 'r')
for i in fp:
    globals()["tt{}".format(n+1)] = []
    a = "tt"+str(n+1)
    tti = eval(a)
    period, start_node, dest_node, length, number = i.rstrip('\n').split(" ")
    tti.append(int(period))
    tti.append(start_node)
    tti.append(dest_node)
    tti.append(int(length))
    tti.append(int(number))
    tmp_list.append(tti[0])
    tt_count.append(n+1)
    n = n+1
    
fp.close()


# 求hyper period
#pair = combine(tt_count, 2)
#print(pair)
for i in range(len(tmp_list)):
    hyper_period = lcms(int(tmp_list[i]), hyper_period)
#print("hyper period is %d" %hyper_period)



