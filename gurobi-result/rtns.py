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
tt_count = []   #紀錄全部的tt數量

not_sorted_link = []# 紀錄尚未進行排程的link
link_dict = {}
all_linkname = []  #儲存所有的link名稱

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



#將link記錄下來,產生對應的time slot array
fo = open('topology_information.txt', 'r')
for i in fo:
    not_sorted_link.append(i.rstrip('\n'))
    b = i.rstrip('\n')
    all_linkname.append(b)
    #print("all_linkname is", all_linkname)
    #print("b is ", b)
    globals()["{}".format('l'+str(i.rstrip('\n')))] = [0]*hyper_period   # lExEy = [0, 1, 0], link的time slot
    globals()["tt{}".format(str(i.rstrip('\n')))] = []  # ttExtoEy = [], 儲存通過這個link有哪些tt
    globals()["nodeto{}".format(str(i.strip('\n')))] = [] # nodetoExtoEy = [{}] save the time slot is open or close, and the other information like start tt and close tt flow.  
    a = 'l'+str(i.rstrip('\n'))
    #b = 'tt'+str(i.rstrip('\n'))
    #print(b)
    #link_tt = eval(b)
    #print(link_tt)
    print(a)  #a = lExtoEy
    link_name = eval(a)
    #print('link name')
    #print(link_name) # lExtoEy = [0,0,0,0,0,....]共hyper_period個

    link_dict[b] = 0

    #print(len(link_name))
    #print(type(link_name))
    #link_name[1] = 1
#print('link_dict is ', link_dict)
#print('not sorted link: ', not_sorted_link)
fo.close()


#將tt flow所經過的路徑進行統計權重
for i in range(len(tt_count)):
    tti_name = "tt"+str(i+1)
    tti = eval(tti_name)

    #計算tti在1Gbps擴僕下的transmission time, 並存進tti的資訊中
    tt_i = "tt"+str(i+1)
    tti = eval(tt_i)
    tti_L = (tti[3]+30)*8/1000  #頻寬為1Gbps, 算出來的單位是us
    tti.append(tti_L)

    #print(tti)
    count_in_hyperperiod = int(hyper_period/int(tti[0]))
    #print("%s repeat %d times in hyperperiod" %(tti_name, count_in_hyperperiod))
    src = 'E'+str(tti[1])
    dest = 'E'+str(tti[2])
    path = shortestPath(graph_3, src, dest)
    #print('1 ', path)

    for j in range(len(path)):  #處理字串方便之後運算, [['E1']] => ['E1']
        path.append(path[0][0])
        path.pop(0)
        #print('2 ',path)
    
    link_pass = []
    for k in range(len(path)-1):  #將tt經過的每條link區隔開來
        link_pass.append(path[k:k+2])
        link_name = link_pass[k][0]+'to'+link_pass[k][1]

        #print('link_name is',link_name)
        tmp_cal = link_dict[link_name]   #取出目前link的權重數
        tmp_cal = tmp_cal+1
        link_dict[link_name] = tmp_cal
        link_dict.update()

        #記錄每條link是哪些tt經過
        link_record = "tt"+link_name
        print("link_record", link_record)
        link_record = eval(link_record)
        link_record.append(str(i+1))
        print(link_record)

print('link_dict is ', link_dict)
sorted_link_weight = {}
sorted_link_weight = sorted(link_dict.items(), key = itemgetter(1), reverse = True)
print('sorted_link_weight is', sorted_link_weight)
#print(type(sorted_link_weight))  result is list
#print(type(link_dict))   result is dict


