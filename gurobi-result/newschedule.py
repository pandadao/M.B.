# -*- coding:utf-8 -*-
'''
third-party tool, install from web guide
'''
from gurobipy import *
import time
import numpy as np
from operator import itemgetter


'''
self develop function, package together
'''
from ecmp import *
from function_tool import combine, lcms
from getport import *


#通用變數區
M = 100000          # gurobi運算中的or所需之極大值,代替cplex中的either-or功能
hyper_period = 1    # 所以TT flow的lcm
IFG = 96            # inter frame gap , fixed number,單位是bit, 假設在1Gpbs上運行則是0.096us, 100M => 0.96 us
obj = 0.0           # 目標式參數

send_src = []       # 紀錄host發送端
path_node = []      # 紀錄哪些結點是中繼的switch

#將tt資訊讀取出來並存成陣列
n = 0
tmp_list = []
tt_count = []

not_sorted_link = []# 紀錄尚未進行排程的link
link_dict = {}

start_time = time.time()




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
pair = combine(tt_count, 2)
for i in range(len(tmp_list)):
    hyper_period = lcms(int(tmp_list[i]), hyper_period)

#print("hyper period is %d" %hyper_period)


#將link記錄下來,產生對應的time slot array
fo = open('topology_information.txt', 'r')
for i in fo:
    not_sorted_link.append(i.rstrip('\n'))
    b = i.rstrip('\n')
    #print("b is ", b)
    globals()["{}".format('l'+str(i.rstrip('\n')))] = [0]*hyper_period   # lExEy = [0, 1, 0], link的time slot
    globals()["tt{}".format(str(i.rstrip('\n')))] = []  # ttExtoEy = [], 儲存通過這個link有哪些tt
    a = 'l'+str(i.rstrip('\n'))
    #b = 'tt'+str(i.rstrip('\n'))
    #print(b)
    #link_tt = eval(b)
    #print(link_tt)
    #print(a)
    link_name = eval(a)
    #print(link_name)

    link_dict[b] = 0

    #print(len(link_name))
    #print(type(link_name))
    #link_name[1] = 1
print('link_dict is ', link_dict)
#print('not sorted link: ', not_sorted_link)
fo.close()

#將tt flow所經過的路徑進行統計權重
for i in range(len(tt_count)):
    tti_name = "tt"+str(i+1)
    tti = eval(tti_name)
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
        #print("link_record", link_record)
        link_record = eval(link_record)
        link_record.append(str(i+1))
        #print(link_record)

    
sorted_link_weight = {}
sorted_link_weight = sorted(link_dict.items(), key = itemgetter(1), reverse = True)
#print('sorted_link_weight is', sorted_link_weight)
#print(type(sorted_link_weight))  result is list
#print(type(link_dict))   result is dict

not_sorted_link.clear()
for i in range(len(sorted_link_weight)):
    not_sorted_link.append(sorted_link_weight[i][0])

#print(type(not_sorted_link))
#print(not_sorted_link)

#print(link_dict)
#print(sorted_link_weight)
# TODO 開始針對每個link進行排程
while not_sorted_link:    #如果還有link沒有進行排程,則不能結束
    schedule_link = 'tt'+not_sorted_link[0]
    print(schedule_link)
    schedule_link = eval(schedule_link)
    print(schedule_link)

    '''
    gurobi限制式所需的變數
    '''
    x_number =  0       # cplex的變數量, x1, x2, x3 ....
    c_number = 0        # 限制式的編號變數

    if len(schedule_link)>0:   #若link上有尚未進行排成的tt則進行最佳化
        m = Model('Protorype example_type1')
        tmp_schedule_tt = []
        
        for tt in schedule_link:
            tmp_schedule_tt.append(tt)
            #print(tmp_schedule_tt)
            
        #宣告每個TT的offset變數
        count_schedule_tt = len(tmp_schedule_tt)
        for numbers in range(count_schedule_tt):
            a = "tt"+str(tmp_schedule_tt[numbers])
            tti = eval(a)
            va = "x"+str(x_number+1)
            globals()['x{}'.format(x_number+1)] = m.addVar(lb = 0, ub = int(int(tti[0])-1), vtype = GRB.INTEGER, name = va)  #offset變數宣告完畢
            tti.append(eval(va))
            x_number = x_number+1
        
        # 檢查TT長度是否超過自身週期,限制式(1): 0<= tti.offset + tti.L+IFG time <= tt.p
        ttinumber = x_number  # 紀錄產生了多少個offset變數,注意x_number,假設有4條tt要排成,則現在的x_number為4
        for numbers in range(count_schedule_tt):
            a = "tt"+str(tmp_schedule_tt[numbers])
            tti = eval(a)
            print(a)
            tti_L = (tti[3]+30)*8/1000  #頻寬的值這邊統一為1Gbps,算出來的單位為us
            tti.append(tti_L)
            print(tti)
            ca = "c"+str(c_number)
            c_number = c_number +1
            m.addConstr(tti[5]<=tti[0]-tti[6]-0.096, ca)
            #print('1')

        #宣告限制式





        

        #排成過的tt需要清除掉,所以要將link上紀錄排程過的tt移除
        fo = open('topology_information.txt', 'r')
        for record in fo:
            linkname = "tt"+record.rstrip('\n')
            linkname = eval(linkname)
            for schedulett in range(count_schedule_tt):
                try:
                    linkname.remove(tmp_schedule_tt[schedulett])
                except:
                    pass
        fo.close()




    
    else:    #若link上沒有需要排成的tt則跳過這個link
        #print('else')
        pass
    

    tmp_schedule_tt.clear()
    #排完要pop掉這個link
    not_sorted_link.pop(0)



