# -*- coding:utf-8 -*-
'''
third-party tool, install from web guide
'''
from gurobipy import *
import time
import numpy as np
from operator import itemgetter
import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
threshould = 0.5
totalslot = 0
queueingtime_sum = 0
#將tt資訊讀取出來並存成陣列
n = 0
tmp_list = []
tt_count = []

queueing_pd = pd.DataFrame() #儲存queueing delay的相關作圖資料
linkslot_pd = pd.DataFrame() #儲存每條link 的slot相關做圖資料

not_sorted_link = []# 紀錄尚未進行排程的link
link_dict = {}

totalqueueingtime = 0

variable_count = 0
constraint_count = 0

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

ttfilename = int(input("read how many tt flow? "))
#讀取所有TT flow資訊並紀錄
fp = open('Limited_flow_data-%d.txt'%(ttfilename), 'r')
for i in fp:
    globals()["tt{}".format(n+1)] = []
    globals()["tt{}_QD".format(n+1)] = [0]  # 儲存各自tt的qeueueing delay
    a = "tt"+str(n+1)
    tti = eval(a)
    period, start_node, dest_node, length, number ,e2e= i.rstrip('\n').split(" ")

    #TODO: Limited_flow_data.txt的資訊新增e2e,需要重新修改tti的陣列資訊

    tti.append(int(period))
    tti.append(start_node)
    tti.append(dest_node)
    tti.append(int(length))
    tti.append(int(number))
    tti.append(int(e2e))
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

fo = open('topology_information.txt', 'r')
linkcount = []
n = 0

#將link記錄下來,產生對應的time slot array
fo = open('topology_information.txt', 'r')
for i in fo:
    not_sorted_link.append(i.rstrip('\n'))
    b = i.rstrip('\n')
    #print("b is ", b)
    globals()["{}".format('l'+str(i.rstrip('\n')))] = [0]*hyper_period   # lExEy = [0, 1, 0], link的time slot
    globals()["tt{}".format(str(i.rstrip('\n')))] = []  # ttExtoEy = [], 儲存通過這個link有哪些tt
    globals()["nodeto{}".format(str(i.strip('\n')))] = [] # nodetoExtoEy = [{}] save the time slot is open or close, and the other information like start tt and close tt flow.  
    globals()["{}_slot".format(str(i.strip('\n')))] = [0] #儲存此link用了多少的slot數量
    a = 'l'+str(i.rstrip('\n'))
    linkcount.append(int(n))
    n = n+1
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
linkcount.append(len(linkcount))


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
    print(path)
    #print('1 ', path)

    for j in range(len(path)):  #處理字串方便之後運算, [['E1']] => ['E1']
        path.append(path[0][0])
        path.pop(0)
        #print('2 ',path)
    #print(path)
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

#print('link_dict is ', link_dict)
sorted_link_weight = {}
sorted_link_weight = sorted(link_dict.items(), key = itemgetter(1), reverse = True)
#print('sorted_link_weight is', sorted_link_weight)
#print(type(sorted_link_weight))  result is list
#print(type(link_dict))   result is dict



not_sorted_link.clear()
for i in range(len(sorted_link_weight)):
    not_sorted_link.append(sorted_link_weight[i][0])   #依照每條link的權重排序

#print(type(not_sorted_link))
#print(not_sorted_link)

#print(link_dict)
#print(sorted_link_weight)



#  開始針對每個link進行排程
while not_sorted_link:    #如果還有link沒有進行排程,則不能結束
    schedule_link = 'tt'+not_sorted_link[0]    #ttExtoEy
    print("Now will schedule the link ",schedule_link)
    schedule_link = eval(schedule_link)
    #print(schedule_link)   #ttExEy = [1, 2, 3 ...]

    '''
    gurobi限制式所需的變數
    '''
    x_number =  0       # cplex的變數量, x1, x2, x3 ....
    c_number = 0        # 限制式的編號變數
    n_number = 0        #cplex用於!=的變數量, n1, n2, n3 ....
    y_number = 0        #!= 限制式使用的y變數

    if len(schedule_link)>0:   #若link上有尚未進行排成的tt則進行最佳化

        print("Now will schedule the link ",schedule_link)

        m = Model('Protorype example_type1')
        tmp_schedule_tt = []
        
        #y = m.addVar(lb = 0, ub = 1, vtype = GRB.BINARY, name = 'y')

        for tt in schedule_link:
            tmp_schedule_tt.append(tt)   #紀錄目前要進行排成的tt是哪些
            #print(tmp_schedule_tt)
        pair = []
        pair = combine(tmp_schedule_tt, 2)  #因為每個tt要互相排程,所以將所有組合產出
        #print("pair", pair)
        #宣告每個TT的offset變數
        #這個offset變數應該要先檢查是否有足夠的time slot, 需要設定!= 條件
        count_schedule_tt = len(tmp_schedule_tt)  #計算有多少條tt要進行排程
        for numbers in range(count_schedule_tt):
            a = "tt"+str(tmp_schedule_tt[numbers])  #針對tti進行offset的變數宣告
            tti = eval(a)
            va = "x"+str(x_number+1)
            globals()['x{}'.format(x_number+1)] = m.addVar(lb = 0, ub = int(int(tti[0])-1), vtype = GRB.INTEGER, name = va)  #offset變數宣告完畢
            variable_count = variable_count+1
            tti.append(eval(va))
            x_number = x_number+1

            #檢查tt的offset值是否不能等於某些數,如果某個time slot已經被排程則不能塞進這個time slot內部
            ttsrc = 'E'+ tti[1]
            ttdest = 'E' + tti[2]
            path = shortestPath(graph_3, ttsrc, ttdest)
            lname = 'l'+path[0][0]+'to'+path[1][0]
            lname = eval(lname)
            #print('lname: ', lname)
            '''
            lE3toE7[0] = 1
            lE3toE7[2] = 1
            lE1toE7[0] = 1
            lE1toE7[1] = 1
            lE4toE8[0] = 1
            lE4toE8[1] = 1
            lE4toE8[98] = 1
            print(lE4toE8)
            #print(lE6toE8)
            '''
            position = []
            for posi in range(len(lname)):
                
                if lname[posi] == 1:
                    position.append(posi)
                else:
                    pass
                '''
                if lname[posi] == 0:
                    pass
                else:
                    position.append(posi)
                '''
            print('can not use time slot is ')
            print(position)
            if position:
                for notuse in range(len(position)):
                    #不能用的數字宣告成進gurobi的變數中
                    na = 'n'+str(n_number)
                    print('na is ', na)
                    globals()['n{}'.format(n_number)] = m.addVar(lb = 0, ub = int(hyper_period), vtype = GRB.INTEGER, name = na)
                    variable_count = variable_count+1
                    na = eval(na)
                    print('na is', na)

                    #給每個y有各自的變數
                    ya = 'y'+str(y_number)
                    globals()['y{}'.format(y_number)]=m.addVar(lb=0, ub =1, vtype=GRB.BINARY, name=ya)
                    variable_count = variable_count+1
                    ya = eval(ya)
                    y_number = y_number+1

                    tmp_number = position[notuse]  #知道tti第一條link上第幾個time slot不能用, 進行!= 限制事宣告
                    print('tmp_number is', tmp_number)
                    ca = "c"+str(c_number)
                    m.addConstr(na == int(tmp_number), ca)
                    constraint_count = constraint_count+1
                    n_number = n_number+1
                    c_number = c_number+1

                    ca = "c"+str(c_number)
                    m.addConstr(na-tti[6]+M*ya>=e, ca)
                    constraint_count = constraint_count+1
                    c_number = c_number+1
                    ca = "c"+str(c_number)
                    m.addConstr(na-tti[6]+M*ya<=M-e, ca)
                    constraint_count = constraint_count+1
                    c_number = c_number+1

            else:
                print("link's time slots all can use")
            

        
        # 檢查TT長度是否超過自身週期,限制式(1): 0<= tti.offset + tti.L+IFG time <= tt.p
        ttinumber = x_number  # 紀錄產生了多少個offset變數,注意x_number,假設有4條tt要排成,則現在的x_number為4
        for numbers in range(count_schedule_tt):
            a = "tt"+str(tmp_schedule_tt[numbers])
            tti = eval(a)
            print(a)
            tti_L = (tti[3]+29)*8/1000  #頻寬的值這邊統一為1Gbps,算出來的單位為us
            tti.append(tti_L)
            print(tti)
            ca = "c"+str(c_number)
            m.addConstr(tti[6]<=tti[0]-tti[7]-0.096, ca)
            constraint_count = constraint_count+1
            c_number = c_number +1
            #print('1')
        


        #宣告限制式(2), 進行frame一前一後排程
        for i in pair:
            tt_i = "tt"+str(i[0])
            tt_j = "tt"+str(i[1])
            tti = eval(tt_i)
            ttj = eval(tt_j)
            tti_A = 0
            ttj_B = 0

            a = int(hyper_period/int(tti[0]))
            b = int(hyper_period/int(ttj[0]))

            #推算此node前的所有耗費時間
            tti_src = 'E'+str(tti[1])
            tti_dest = 'E'+str(tti[2])

            ttj_src = 'E'+str(ttj[1])
            ttj_dest = 'E'+str(ttj[2])
            
            ttipath = shortestPath(graph_3, tti_src, tti_dest)
            for j in range(len(ttipath)):
                ttipath.append(ttipath[0][0])
                ttipath.pop(0)
            #print(ttipath)
            ttjpath = shortestPath(graph_3, ttj_src, ttj_dest)
            for j in range(len(ttjpath)):
                ttjpath.append(ttjpath[0][0])
                ttjpath.pop(0)
                

            tmp_varaible = "tt"+not_sorted_link[0]
            tmp, nodesrc, nodedest = tmp_varaible.split('E')
            nodesrc, tmp = nodesrc.split('t')  # nodesrc和noddedest是排程中的link的src & dest, 以純數字表示
            nodesrc = 'E'+str(nodesrc)
            nodedest = 'E'+str(nodedest)

            tti_n_hop = ttipath.index(nodesrc)
            #print('tti_n_hop ', tti_n_hop)
            ttj_n_hop = ttjpath.index(nodesrc)
            #print('ttj_n_hop ', ttj_n_hop)


            #計算tti在這個node之前所有的transmission time 和propagation time等時間
            if tti_n_hop > 0:
                for ttith in range(tti_n_hop):
                    tmp_src = ttipath[ttith]
                    #print('tmp_src', tmp_src)
                    tmp_dest = ttipath[ttith+1]
                    #print('transmittion time is', tti[6])
                    #print(topology_3[tmp_src][tmp_dest]['propDelay'])
                    tti_A = tti_A + tti[7] + topology_3[tmp_src][tmp_dest]['propDelay']
            else:
                pass
            #計算ttj在這個node之前所有的transmission time 和propagation time等時間

            if ttj_n_hop > 0:
                for ttjth in range(ttj_n_hop):
                    tmp_src = ttjpath[ttjth]
                    tmp_dest = ttjpath[ttjth+1]
                    ttj_B = ttj_B + ttj[7] + topology_3[tmp_src][tmp_dest]['propDelay']
            else:
                pass
            print('tti_A ', tti_A)
            print('ttj_B ', ttj_B)

            for k in range(a):
                for l in range(b):
                    va = "x"+str(x_number+1)
                    globals()['x{}'.format(x_number+1)] = m.addVar(lb = 0, ub = 1, vtype = GRB.INTEGER, name = va)
                    variable_count = variable_count+1
                    #宣告c0 c1 c2等編號
                    ca = "c"+str(c_number)
                    #把x1跟tt1結合起來,產生限制式
                    m.addConstr(ttj[6]-tti[6]+l*ttj[0]-k*tti[0]-M*eval(va)<= tti_A-(ttj_B+ttj[7]+0.096),ca)
                    constraint_count = constraint_count+1
                    c_number = c_number+1
                    #如果想讓gate多保留time slot,就在0.096後面加1或n
                    ca = "c"+str(c_number)
                    m.addConstr(tti[6]-ttj[6]+k*tti[0]-l*ttj[0]+M*eval(va)<= M+ttj_B-tti_A-(tti[7]+0.096),ca)
                    constraint_count = constraint_count+1
                    c_number = c_number+1
                    x_number = x_number+1

        
        #修改目標式,單純對offset進行summary
        obj = 0.0
        for i in range(count_schedule_tt):
            tt_i = "tt"+str(tmp_schedule_tt[i])
            tti = eval(tt_i)
            a = int(hyper_period/int(tti[0]))
            obj = obj+tti[6]*a


        m.setObjective(obj, GRB.MINIMIZE)
        m.update()
        m.optimize()

        count = 0
        '''
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
        '''


        offsetname = []
        for i in range(count_schedule_tt):
            s = 'x'+str(i+1)
            offsetname.append(s)
        for v in m.getVars():
            for n in range(len(offsetname)):
                if offsetname[n] == v.varName:
                    print('%s:%d'%(v.varName, v.x))
                    tti = 'tt'+str(tmp_schedule_tt[n])
                    tti = eval(tti)
                    tti[6] = int(v.x)
                    print(tti)
                else:
                    pass
            
        #將link上的tt依照所有的offset值排序, 0,1,100,101 sort
        tmp_array = []
        for i in range(count_schedule_tt):
            operating_tt_name = 'tt'+str(tmp_schedule_tt[i])
            operating_tt = eval(operating_tt_name)
            for timess in range(int(int(hyper_period)/operating_tt[0])):
                tmp_array.append([operating_tt_name, operating_tt[6]+timess*operating_tt[0]])
        link_group_tt = sorted(tmp_array, key = itemgetter(1))
        print("\033[1;31;40m\tlink_group_tt %s\033[0m"%( link_group_tt))  #link_group_tt is [['tt1',0],['tt2',2],['tt1',100],['tt2',102]]
        #print("\033[1;31;40m\tlink_group_tt length is %d\033[0m"%(len(link_group_tt)))



        #依照每個tt進行time slot的推算
        length_link_group_tt = len(link_group_tt)
        for i in range(length_link_group_tt):
            operating_ttname = link_group_tt[i][0]
            print("目前要排成 ", operating_ttname)
            operating_tt = eval(operating_ttname)
            print("目前要排成 ", operating_tt)
            tt_start = 'E'+ str(operating_tt[1])
            tt_end = 'E' + str(operating_tt[2])

            #宣告tti_QD變數
            tti_qd = operating_ttname+"_QD"
            ttiqd = eval(tti_qd)

            path = shortestPath(graph_3, tt_start, tt_end)
            #字串處理
            for p in range(len(path)):
                path.append(path[0][0])
                path.pop(0)
            print("處理過的path", path)
            first_offset = operating_tt[6]
            #找出要推算的link
            hop = len(path)
            for nodeth in range(hop-1):
                #print(nodeth)
                #if path[nodeth] == tt_start:
                if path[nodeth] in hostnode:
                    #找出現在要計算哪一條link
                    nodesrc  = path[nodeth]
                    nodedest = path[nodeth+1]
                    linkname = "l"+nodesrc+"to"+nodedest
                    print("now calculating the link ", linkname)
                    linkname = eval(linkname)
                    #print(linkname)
                    evalhost = eval(nodesrc)  # 變數E1 ,格式為 [{}]
                    print('nodesrc is', evalhost)

                    
                    #求出這條link的propagation delay
                    linkpropagationdelay = topology_3[nodesrc][nodedest]['propDelay']
                    print("this link's propagation delay is ", linkpropagationdelay)

                    #get dest MAC
                    mac_addr = topology_3[tt_end]['MAC']

                    ttoffset = link_group_tt[i][1]
                    endtrans = ttoffset+operating_tt[7]+0.096 #該tt從offset開始到傳送結束的時間
                    ttoffsetkeep = math.ceil(endtrans)-ttoffset

                    #儲存host相關xml所需資料
                    evalhost.append({'send':link_group_tt[i][0], 'start':ttoffset, 'end':endtrans, 'queue':7, 'dest': mac_addr, 'size':operating_tt[3], 'transtime':operating_tt[7]})
                    print(nodesrc, ' is', evalhost)
                    
                    #佔用的time slot記錄下來,其它條TT不能佔用
                    for used in range(ttoffsetkeep):

                        linkname[ttoffset+used] = linkname[ttoffset+used] + 1

                    nexthop_tt_start_time = ttoffset + operating_tt[7]+linkpropagationdelay
                    print(linkname)
                    

                else:
                    nodesrc = path[nodeth]
                    nodedest = path[nodeth+1]
                    linkname = "l"+nodesrc+"to"+nodedest  #lExtoEy , link's time slot
                    xmlentry_name = "nodeto"+nodesrc+"to"+nodedest #link's xml entry information
                    print("xmlentry name is", xmlentry_name)
                    xmlentry = eval(xmlentry_name)
                    print("xmlentry is", xmlentry)

                    
                    #xmlentry = sorted(xmlentry, key = itemgetter('start'))
                    print("now calculating the link ", linkname)
                    linkname = eval(linkname)
                    #print(linkname)
                    
                    #求出這條link的propagation delay
                    linkpropagationdelay = topology_3[nodesrc][nodedest]['propDelay']
                    
                    #計算是否有重疊,處理完所有重疊後再求gatetime
                    flag = 'checkoverlap'
                    tmpuse = nexthop_tt_start_time
                    s2 = nexthop_tt_start_time
                    e2 = nexthop_tt_start_time+operating_tt[7]+interframegap
                    listvariable = 0
                    
                    for listvariable in xmlentry:

                        s1 = listvariable['start']
                        e1 = listvariable['end']
                        if (s2>=e1) or (e2<=s1):   # no overlap
                            pass
                            

                        else:   #overlap, 將發送時間向後移動
                            print("shift")
                            #totalqueueingtime = totalqueueingtime+ e1-s2
                            #print("totalqueueingtime is", totalqueueingtime)
                            s2 = e1
                            e2 = s2+operating_tt[7]+interframegap

                    
                    #判斷transmission time是否超過一格time slot,如果本身傳輸時間超過一個time slot,則沒關係,如果本身傳輸時間小於一單位的time slot,則向後延遲傳輸
                    e2floor = math.floor(e2)
                    s2floor = math.floor(s2)
                    transfloor = math.floor(operating_tt[7])
                    #先判斷是否有因為overlap而改變傳輸時間
                    if s2 == tmpuse:

                        if (e2floor-s2floor)>0: #牌成的傳輸時間超出一格
                            if transfloor >1: #自身傳輸時間就需要超出一格,不動作
                                gate_open_time = math.floor(s2)
                                gate_keep_time = math.ceil(e2)-gate_open_time
                                nexthop_tt_start_time = e2-interframegap+linkpropagationdelay
                                xmlentry.append({'send':link_group_tt[i][0], 'start':s2, 'end':e2, 'open':gate_open_time, 'length':gate_keep_time, 'bitvector':'00000001'})
                                for used in range(gate_keep_time):
                                    linkname[gate_open_time+used] = linkname[gate_open_time+used]+1

                            else: #自身所需的time slot小於一格,但是佔用了兩格time slot做傳輸,將此TT向後移動
                                gate_open_time = math.ceil(s2)
                                e2 = gate_open_time+operating_tt[7]+interframegap
                                totalqueueingtime = totalqueueingtime+gate_open_time-tmpuse
                                ttiqd[0] = ttiqd[0]+gate_open_time-tmpuse
                                gate_keep_time = math.ceil(e2)-gate_open_time
                                nexthop_tt_start_time = e2-interframegap+linkpropagationdelay
                                xmlentry.append({'send':link_group_tt[i][0], 'start':gate_open_time, 'end':e2, 'open':gate_open_time, 'length':gate_keep_time, 'bitvector':'00000001'})
                                for used in range(gate_keep_time):
                                    linkname[gate_open_time+used] = linkname[gate_open_time+used]+1
                        
                        else: #本身傳輸時間就小於一格time slot
                            gate_open_time = math.floor(s2)
                            gate_keep_time = math.ceil(e2)-gate_open_time
                            nexthop_tt_start_time = e2-interframegap+linkpropagationdelay
                            xmlentry.append({'send':link_group_tt[i][0], 'start':s2, 'end':e2, 'open':gate_open_time, 'length':gate_keep_time, 'bitvector':'00000001'})
                            for used in range(gate_keep_time):
                                linkname[gate_open_time+used] = linkname[gate_open_time+used]+1


                    else: #有因為overlap而移動過,就接續傳輸,可以節省頻寬跟降低queueing delay,不需要再更動
                        gate_open_time = math.floor(s2)
                        gate_keep_time = math.ceil(e2)-gate_open_time
                        totalqueueingtime = totalqueueingtime+s2-tmpuse
                        ttiqd[0] = ttiqd[0]+s2-tmpuse 
                        nexthop_tt_start_time = e2-interframegap+linkpropagationdelay
                        xmlentry.append({'send':link_group_tt[i][0], 'start':s2, 'end':e2, 'open':gate_open_time, 'length':gate_keep_time, 'bitvector':'00000001'})
                        
                        for used in range(gate_keep_time):
                            linkname[gate_open_time+used] = linkname[gate_open_time+used]+1




        m.reset()
        print('\n')
                
        #列印出每個host要送的tt資訊
        for mm in hostnode:
            hostname = mm
            print(hostname)
            hostname = eval(hostname)
            print(hostname)


        #列印出每條offset值的狀態
        fq = open('topology_information.txt', 'r')
        for ll in fq:
            linkname = "nodeto"+ll.rstrip('\n')
            print(linkname)
            linkname = eval(linkname)
            print(linkname)
        
        
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

runtime = time.time()-start_time
#列印出每個host要送的tt資訊
for mm in hostnode:
    hostname = mm
    print(hostname)
    hostname = eval(hostname)
    print(hostname)

fo = open('topology_information.txt', 'r')
for i in fo:
    not_sorted_link.append(i.rstrip('\n'))
    b = i.rstrip('\n')
    linkname = 'l'+str(i.rstrip('\n'))
    linkname = eval(linkname)

    #儲存每條link的slot數量
    linkname_pd = str(i.strip('\n'))+"_slot"
    linknamepd = eval(linkname_pd)

    for j in range(len(linkname)):
        if linkname[j]>0:
            totalslot = totalslot+1
            linknamepd[0] = linknamepd[0]+1
        else:
            pass
    tmpcount = int(linknamepd[0])
    linkslot = pd.DataFrame([tmpcount], index = [linkname_pd], columns = pd.Index(['link name']))
    linkslot_pd = linkslot_pd.append(linkslot)
fo.close
linkslot = pd.DataFrame([totalslot], index = ['total slot'], columns = pd.Index(['link name']))
linkslot_pd = linkslot_pd.append(linkslot)
linkslot_pd['number'] = linkcount

#列印出每條offset值的狀態
fq = open('topology_information.txt', 'r')
for ll in fq:
    linkname = "nodeto"+ll.rstrip('\n')
    print(linkname)
    linkname = eval(linkname)
    print(linkname)
print("total timeslot is ", totalslot)
print("total runtime is ", runtime)
print("total queueing time is ", totalqueueingtime)


#show figure of each link slot
linkslot_pd['link name'].plot.bar()
for a,b in zip(linkslot_pd['number'], linkslot_pd['link name']):
    plt.text(a, b+0.001, '%d' %b, ha = 'center', va = 'bottom', fontsize=9)

plt.xlabel("link's name")
plt.ylabel('slot count (unit slot)')
plt.title("BLF each link use slots ")
plt.show()

# show figure of each tti
ttcount = []
for i in range(len(tt_count)):
    tti_qd = "tt"+str(i+1)+"_QD"
    tt_i = "tt"+str(i+1)
    ttcount.append(i)
    ttiqd = eval(tti_qd)
    ti = pd.DataFrame([ttiqd[0]], index = [tt_i], columns = pd.Index(['queueing time']))
    queueing_pd = queueing_pd.append(ti)

ttcount.append(len(ttcount))
ti = pd.DataFrame([totalqueueingtime], index = ['total'], columns = pd.Index(['queueing time']))
queueing_pd = queueing_pd.append(ti)
queueing_pd['number'] = ttcount

queueing_pd['queueing time'].plot.bar()
#plt.grid(axis='y')
for a,b in zip(queueing_pd['number'],queueing_pd['queueing time']):
    plt.text(a, b+0.001, '%.2f' %b, ha = 'center', va = 'bottom', fontsize=9)
plt.xlabel("tt number")
plt.ylabel('Queueing time (us)')
plt.title("BLF Queueing Time ")
plt.show()

print("constraint count ", constraint_count)
print("variable count ", variable_count)
