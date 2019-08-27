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
#print('link_dict is ', link_dict)
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

    
print('link_dict is ', link_dict)
sorted_link_weight = {}
sorted_link_weight = sorted(link_dict.items(), key = itemgetter(1), reverse = True)
print('sorted_link_weight is', sorted_link_weight)
#print(type(sorted_link_weight))  result is list
#print(type(link_dict))   result is dict

not_sorted_link.clear()
for i in range(len(sorted_link_weight)):
    not_sorted_link.append(sorted_link_weight[i][0])

#print(type(not_sorted_link))
#print(not_sorted_link)

#print(link_dict)
#print(sorted_link_weight)
#  開始針對每個link進行排程
while not_sorted_link:    #如果還有link沒有進行排程,則不能結束
    schedule_link = 'tt'+not_sorted_link[0]
    print(schedule_link)
    schedule_link = eval(schedule_link)
    print(schedule_link)   #ttExEy = [1, 2, 3 ...]

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
        pair = []
        pair = combine(tmp_schedule_tt, 2)
        print("pair", pair)
        #宣告每個TT的offset變數
        #TODO 這個offset變數應該要先檢查是否有足夠的time slot, 需要設定!= 條件
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

        #宣告限制式(2), 進行frame一前一後排程
        for i in pair:
            tt_i = "tt"+str(i[0])
            tt_j = "tt"+str(i[1])
            tti = eval(tt_i)
            ttj = eval(tt_j)

            a = int(hyper_period/int(tti[0]))
            b = int(hyper_period/int(ttj[0]))
            
            for k in range(a):
                for l in range(b):
                    va = "x"+str(x_number+1)
                    globals()['x{}'.format(x_number+1)] = m.addVar(lb = 0, ub = 1, vtype = GRB.INTEGER, name = va)
                    #宣告c0 c1 c2等編號
                    ca = "c"+str(c_number)
                    c_number = c_number+1
                    #把x1跟tt1結合起來,產生限制式
                    m.addConstr(ttj[5]-tti[5]+l*ttj[0]-k*tti[0]-M*eval(va)<= -(ttj[6]+0.096),ca)
                    #如果想讓gate多保留time slot,就在0.096後面加1或n
                    ca = "c"+str(c_number)
                    c_number = c_number+1
                    m.addConstr(tti[5]-ttj[5]+k*tti[0]-l*ttj[0]+M*eval(va)<= M-(tti[6]+0.096),ca)
                    x_number = x_number+1


        for i in range(count_schedule_tt):
            tt_i = "tt"+str(tmp_schedule_tt[i])
            tti = eval(tt_i)
            tmp_varaible = "tt"+not_sorted_link[0]
            tmp, nodesrc, nodedest = tmp_varaible.split('E')
            nodesrc, tmp = nodesrc.split('t')
            print(tmp, nodesrc, nodedest)
            src = 'E'+str(tti[1])
            dest = 'E'+str(tti[2])
            path = []
            path = shortestPath(graph_3, src,dest)
            print(path)
            #hop = len(path) - (path.index('E'+nodesrc)+1)
            #hop = len(path) - 2
            Enodesrc = 'E'+str(nodesrc)
            print('Enodesrc:',Enodesrc)
            inde = path.index([Enodesrc])
            print('inde:', inde)
            hop = len(path) - (inde+1)      #推算從路徑上某個node到這個tt終點還剩下幾個hop
            print('hop', hop)
            a = int(hyper_period/int(tti[0]))
            
            propagation_count = 0

            for j in range(len(path)):  #處理字串方便之後運算, [['E1']] => ['E1']
                path.append(path[0][0])
                path.pop(0)
            
            for calculate in range(hop):
                nowsrc = path[inde]
                nowdest = path[inde+1]
                yo = topology_3[nowsrc][nowdest]['propDelay']
                print('yo', yo)
                propagation_count = propagation_count+yo
                print('propagation ', propagation_count)
                inde = inde+1




            for pi in range(a):#計算一個hyperperiod內要傳送幾次tti
                #obj = tti[5]+pi*tti[0]+hop*tti[6]+0.1*hop  #TODO 0.1是propagation delay, 應該要依照真實topology求出來=>  done
                obj = tti[5]+pi*tti[0]+hop*tti[6]  
                print(type(obj))
            obj = obj + propagation_count
            #print(obj)

        m.setObjective(obj, GRB.MINIMIZE)
        m.update()
        m.optimize()

        count = 0

        for v in m.getVars():
            count = count+1
            if count > count_schedule_tt:
                break
            else:
                print('%s:%d' %(v.varName, v.x))
                #將offset放進對應的tt內部
                tti = 'tt'+str(tmp_schedule_tt[count-1])
                tti = eval(tti)
                tti[5] = int(v.x)
                print(tti)

       
       #TODO offset求出後,需要回推至每條link上,將time slot填進每個link的時間軸上









            '''
            查找列表中所有特定值的位置
            [i for i in range(len(a)) if a[i] == 1]
            print(a) #[1,2,3,1]
            #result => [0,3]
            '''

            #TODO 產生目標式
        m.reset()
        print('\n')







        

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


