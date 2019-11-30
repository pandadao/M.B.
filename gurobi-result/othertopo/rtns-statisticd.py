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
constraint_count = 0 #紀錄總共有幾條constraint, 用於宣告限制式時所需的變數
y_count = 0         #紀錄每次的big M solve

interframegap = 0.096
variable_count = 0  #紀錄總共有多少變數來求解
send_src = []       # 紀錄host發送端
path_node = []      # 紀錄哪些結點是中繼的switch

data = pd.DataFrame()   #儲存做圖資料
link_slot = pd.DataFrame()
#將tt資訊讀取出來並存成陣列
n = 0
tmp_list = []
tt_count = []   #紀錄全部的tt數量

#儲存總共有哪些offset的陣列
offsetlist = []

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

ttfilename = int(input(" read how much tt data?"))

# TODO: 應該要新增一個籃位讀取tti的e2e delay值,所以後續所有的tti陣列排序要重新修改,產生tti的程式也要進行修改
#讀取所有TT flow資訊並紀錄
fp = open("Limited_flow_data-%d.txt"%(ttfilename), 'r')
for i in fp:
    globals()["tt{}".format(n+1)] = []
    globals()["tt{}_offset".format(n+1)] = []
    globals()["tt{}_QD".format(n+1)] = 0  # 儲存各自tt的qeueueing delay
    a = "tt"+str(n+1)
    tti = eval(a)
    period, start_node, dest_node, length, number ,e2e= i.rstrip('\n').split(" ")
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
#TODO: 宣告每條link的變數,用來儲存link用了多少time slot
fo = open('topology_information.txt', 'r')
linkcount = []
n = 0

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
    globals()["nodeto{}".format(str(i.rstrip('\n')))] = [] # nodetoExtoEy = [{}] save the time slot is open or close, and the other information like start tt and close tt flow. 
    globals()["{}_schedule".format(str(i.rstrip('\n')))] = []  #儲存此link上的offset值, 格式為[[tt5,0], [tt5,100]]
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


#將tt flow所經過的路徑進行統計權重
for i in range(len(tt_count)):
    tti_name = "tt"+str(i+1)
    tti = eval(tti_name)

    #計算tti在1Gbps擴僕下的transmission time, 並存進tti的資訊中
    tt_i = "tt"+str(i+1)
    tti = eval(tt_i)
    tti_L = (tti[3]+29)*8/1000  #頻寬為1Gbps, 算出來的單位是us
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
        #link_record.append(str(i+1))
        link_record.append(i+1)
        print(link_record)

print('all_linkname is', all_linkname)
print('link_dict is ', link_dict)
sorted_link_weight = {}
sorted_link_weight = sorted(link_dict.items(), key = itemgetter(1), reverse = True)
print('sorted_link_weight is', sorted_link_weight)
#print(type(sorted_link_weight))  result is list
#print(type(link_dict))   result is dict


'''
***  這邊直接宣告gurobi module, 因為這篇Paper是所有的限制式宣告完一起做排程
'''
m = Model('Protorype example_type1')


#針對每一條link上的TT進行offset的變數宣告
for i in range(len(all_linkname)):
    nowlinkname = all_linkname[i]
    nowlink = "tt"+nowlinkname
    print('nowlink', nowlink)
    nowlink = eval(nowlink)
    print(nowlink)

    linkpair = all_linkname[i]+"_pair"
    globals()[linkpair] = combine(nowlink, 2)
    linkpair = eval(linkpair)
    print("linkpair is", linkpair)

    # 如果link內有tt則進行該tt的offset 宣告,如果沒有的話則繼續迴圈, offset變數為 => ExtoEy_tti (x,y,i)為可變數
    if len(nowlink)>0:
        for now in range(len(nowlink)):
            offsetname = nowlinkname+"_tt"+str(nowlink[now])
            print("offsetname is", offsetname)
            
            nowtt = "tt"+str(nowlink[now])
            print('nowtt', nowtt)
            nowtt = eval(nowtt)
            print(nowtt)
            a = int(hyper_period/int(nowtt[0]))

            globals()[offsetname] = m.addVar(lb = 0, ub = int(int(nowtt[0])-1), vtype = GRB.INTEGER, name = offsetname)
            variable_count = variable_count+1
            nowoffset = eval(offsetname)
            #offsetlist.append(nowoffset)
            
            #宣告限制式(1), 0<= offset+tti.L + IFG <= tti.period
            ca = "c"+str(constraint_count+1)
            constraint_count = constraint_count+1
            m.addConstr(nowoffset<=nowtt[0]-nowtt[6]-interframegap, ca)


            #print(nowoffset)
            obj = obj + nowoffset*a   #objective function is minimize obj 
            #print(obj)

    else:
        pass


#宣告constraint (2)跟(5)
for i in range(len(all_linkname)):
    #print("i is", all_linkname[i])
    nowlinkname = all_linkname[i]
    nowlink = "tt"+nowlinkname
    nowlink = eval(nowlink)
    
    if len(nowlink)>0:

        linkpair_name = all_linkname[i]+"_pair"
        linkpair = eval(linkpair_name)

        #開始宣告限制式(2)
        for j in linkpair:
            nowtt_i = "tt"+str(j[0])
            nowtt_j = "tt"+str(j[1])
            nowtti = eval(nowtt_i)
            nowttj = eval(nowtt_j)

            a = int(hyper_period/int(nowtti[0]))
            b = int(hyper_period/int(nowttj[0]))

            i_offsetname = nowlinkname+"_"+nowtt_i
            j_offsetname = nowlinkname+"_"+nowtt_j
            i_offset = eval(i_offsetname)
            j_offset = eval(j_offsetname)

            for k in range(a):
                for l in range(b):
                    ya = "y"+str(y_count+1) # big M solve的y變數
                    globals()['y{}'.format(y_count+1)] = m.addVar(lb = 0, ub = 1, vtype = GRB.BINARY, name = ya)
                    variable_count = variable_count+1

                    ca = "c"+str(constraint_count+1)
                    y_count = y_count+1
                    constraint_count = constraint_count+1

                    m.addConstr(j_offset-i_offset+l*nowttj[0]-k*nowtti[0]-M*eval(ya)<=-(nowttj[6]+interframegap), ca)

                    ca = "c"+str(constraint_count+1)
                    constraint_count = constraint_count+1
                    m.addConstr(i_offset-j_offset+k*nowtti[0]-l*nowttj[0]+M*eval(ya)<=M-(nowtti[6]+interframegap) ,ca)


        #宣告限制式(5)
        linksrc, linkdest = all_linkname[i].split('to')   #確認該link是否為src, 因為src端不會有限制式(5)的問題
        #if linksrc in allhost:
        if linksrc in hostnode:
            pass
        else:
            for j in linkpair:
                nowtt_i = "tt"+str(j[0])
                nowtt_j = "tt"+str(j[1])
                nowtti = eval(nowtt_i)
                nowttj = eval(nowtt_j)

                a = int(hyper_period/int(nowtti[0]))
                b = int(hyper_period/int(nowttj[0]))
                
                nowtti_src = "E"+str(nowtti[1])
                nowtti_dest = "E"+str(nowtti[2])
                nowtti_path = shortestPath(graph_3, nowtti_src, nowtti_dest)

        
                for k in range(len(nowtti_path)):  #處理字串方便之後運算, [['E1']] => ['E1']
                    nowtti_path.append(nowtti_path[0][0])
                    nowtti_path.pop(0)
                

                nowttj_src = "E"+str(nowttj[1])
                nowttj_dest = "E"+str(nowttj[2])
                nowttj_path = shortestPath(graph_3, nowttj_src, nowttj_dest)

                for k in range(len(nowttj_path)):  #處理字串方便之後運算, [['E1']] => ['E1']
                    nowttj_path.append(nowttj_path[0][0])
                    nowttj_path.pop(0)

                nowtti_hop = nowtti_path.index(linksrc)
                nowttj_hop = nowttj_path.index(linksrc)

                tti_prenode = nowtti_path[nowtti_hop-1]
                ttj_prenode = nowttj_path[nowttj_hop-1]

                tti_prelink_name = nowtti_path[nowtti_hop-1]+"to"+linksrc+"_"+nowtt_i
                ttj_prelink_name = nowttj_path[nowttj_hop-1]+"to"+linksrc+"_"+nowtt_j

                #get prelink offset
                tti_preoffset = eval(tti_prelink_name)
                ttj_preoffset = eval(ttj_prelink_name)

                #get prelink propagation delay
                tti_prepropagation = topology_3[tti_prenode][linksrc]['propDelay']
                ttj_prepropagation = topology_3[ttj_prenode][linksrc]['propDelay']


                for k in range(a):
                    for l in range(b):
                        ya = "y"+str(y_count+1)
                        globals()['y{}'.format(y_count+1)] = m.addVar(lb = 0, ub = 1, vtype = GRB.BINARY, name = ya)
                        variable_count = variable_count+1
                        y_count = y_count+1

                        ca = "c"+str(constraint_count+1)
                        constraint_count = constraint_count+1

                        m.addConstr((ttj_preoffset-tti_preoffset+l*nowttj[0]-k*nowtti[0]-M*eval(ya)<=tti_prepropagation-ttj_prepropagation), ca)   #若是要加上transmission delay請參照推導的公式

                        ca = "c"+str(constraint_count+1)
                        constraint_count = constraint_count+1

                        m.addConstr((tti_preoffset-ttj_preoffset+k*nowtti[0]-l*nowttj[0]+M*eval(ya)<=M+ttj_prepropagation-tti_prepropagation), ca)
                

    else:
        pass


#宣告限制式(3)跟(4)
for i in range(len(tt_count)):
    tt_i = "tt"+str(i+1)
    tti = eval(tt_i)
    ttsrc = 'E'+str(tti[1])
    ttdest = 'E'+str(tti[2])
    ttpath = shortestPath(graph_3, ttsrc, ttdest)
    for k in range(len(ttpath)):
        ttpath.append(ttpath[0][0])
        ttpath.pop(0)

    #constraint (3), 該tt須等待前面link傳完才能在現在的link開始傳送
    print("ttpath is ",ttpath)
    for j in range(len(ttpath)-1):
        tmp_src = ttpath[j]
        tmp_dest = ttpath[j+1]

        print("tmp_src is", tmp_src)
        print("tmp_dest is", tmp_dest)
        print("allhost is", allhost)
        if tmp_src in hostnode:
            pass
        else:
            presrc = ttpath[j-1]
            prelink_offsetname = presrc+"to"+tmp_src+"_"+tt_i
            nowlink_offsetname = tmp_src+"to"+tmp_dest+"_"+tt_i

            print("prelink_offsetname is", prelink_offsetname)
            print("nowlink_offsetname is", nowlink_offsetname)

            prelink_offset = eval(prelink_offsetname)
            nowlink_offset = eval(nowlink_offsetname)

            prelink_propagation = topology_3[presrc][tmp_src]['propDelay']
            
            ca = "c"+str(constraint_count+1)
            constraint_count = constraint_count+1
            m.addConstr(prelink_offset-nowlink_offset<=-(tti[6]+prelink_propagation), ca)

    #constraint (4) end to end delay set
    startoffsetname = ttsrc+"to"+ttpath[1]+"_"+tt_i
    startoffset = eval(startoffsetname)

    lastoffsetname = ttpath[-2]+"to"+ttpath[-1]+"_"+tt_i
    lastoffset = eval(lastoffsetname)
    lastlinksrc = ttpath[-2]
    lastlinkdest = ttpath[-1]
    lastlinkprop = topology_3[lastlinksrc][lastlinkdest]['propDelay']
    
    ca = "c"+str(constraint_count+1)
    constraint_count = constraint_count+1
    m.addConstr(lastoffset-startoffset<=tti[5]-tti[6]-lastlinkprop, ca)


m.setObjective(obj, GRB.MINIMIZE)
m.update()
m.optimize()


runtime = time.time()-start_time

schedule_ans = []
for v in m.getVars():
    if "_" in v.varName:
        srcdest, tt_i = v.varName.split("_")
        src, dest = srcdest.split("to")
        tti = eval(tt_i)
        
        #get each link propagation
        nowlink_propagation = topology_3[src][dest]['propDelay']
        
        #calculate the arrival time of next node
        nexthoptime = int(v.x)+tti[6]+nowlink_propagation
        #print(nextahoptime)
        ttx_offsetname = tt_i+"_offset"
        ttx_offset = eval(ttx_offsetname)
        ttx_offset.append([srcdest, int(v.x), tti[0], tti[6],nexthoptime])
        #ttx_noffset = sorted(ttx_offset, key = itemgetter(1))
        #print(ttx_noffaset)
        #ttx_offset = ttx_noffset
        #print(ttx_offsetname, ttx_offset)

        schedule_ans.append([v.varName, int(v.x), tti[0], tti[2], tti[3], tti[6]])
        #print("%s:%d %d h%s %s(bytes) %.4f"%(v.varName, v.x, tti[0],tti[2], tti[3],tti[6]))

        tmpschedulename = srcdest+"_schedule"
        #print("tmpschedulename is", tmpschedulename)
        tmpschedule = eval(tmpschedulename)
        a = int(hyper_period/tti[0])
        for i in range(a):
            tmpoffset = int(v.x + i*tti[0])
            tmpschedule.append([tt_i, tmpoffset])
        tmpschedule = sorted(tmpschedule, key=lambda x:x[1])
        #print(tmpschedulename," offset value ", tmpschedule)
        #print("")
    else:
        pass


queuetime_sum = 0.0
totalslot = 0
number = []
#計算總queueing delay值
for i in tt_count:
    tt_i = "tt"+str(i)
    #print(tt_i)
    tti = eval(tt_i)
    #print("tti ", tti)
    tti_translot = math.ceil(tti[6]+0.096)

     #記算每條tt的queueing delay
    ttx_offsetname = tt_i+"_offset"
    ttx_offset = eval(ttx_offsetname)
    print(ttx_offset)
    tti_qd = tt_i+"_QD"
    ttiqd = eval(tti_qd)
    ttxnoffset = sorted(ttx_offset, key = itemgetter(1))
    print("ttxnoffset is ", ttxnoffset)
    totalslot = totalslot+((tti_translot*len(ttxnoffset))*(hyper_period/tti[0]))
    for j in range(len(ttxnoffset)-1):
        linkoffset = ttxnoffset[j+1][1]
        nexthoptime = ttxnoffset[j][4]
        ttiqd = ttiqd+linkoffset-nexthoptime
    for k in range(len(ttxnoffset)):
        linkname = ttxnoffset[k][0]
        link_name = linkname+"_slot"
        linkname = eval(link_name)
        tmpcount = math.ceil(ttxnoffset[j][3]+0.096)
        #print("tmpcount is ", tmpcount)
        #tmpcount = int(tmpcount)
        tmpcount = tmpcount*(hyper_period/tti[0])
        linkname[0] = linkname[0]+tmpcount
        print(link_name, linkname)
    ttiqd = ttiqd*(hyper_period/tti[0])
    print(tt_i," queueing delay is ", ttiqd)
    ti = pd.DataFrame([ttiqd], index = [tt_i], columns = pd.Index(['queueing time']))
    number.append(int(i)-1)
    #ti['編號'] = number
    data = data.append(ti)
    queuetime_sum = queuetime_sum + ttiqd

#處理link的slot數據顯示於圖表
fo = open('topology_information.txt', 'r')
for i in fo:
    link_name = str(i.strip('\n'))+"_slot"
    linkname = eval(link_name)
    #print(link_name +" use "+str(linkname) +" slots")
    tmpcount = int(linkname[0])
    print("508tmpcount is ", tmpcount)
    linkslot = pd.DataFrame([tmpcount], index = [link_name], columns = pd.Index(['link name']))
    link_slot = link_slot.append(linkslot)

fo.close()


linkslot = pd.DataFrame([totalslot], index = ['totalslot'], columns = pd.Index(['link name']))
link_slot = link_slot.append(linkslot)
print(link_slot)
print(linkcount)
linkcount.append(len(linkcount))
link_slot['number'] = linkcount


#show figure 
print("TT flows total using slot: ", totalslot)
print("rtns total run time is ", runtime, "s")
print("total queueing time(us) is", queuetime_sum)        
ti = pd.DataFrame([queuetime_sum], index = ["total"], columns = pd.Index(['queueing time']))
number.append(int(len(tt_count)))
#ti.insert(1,"編號", number, True)
print(number)
data = data.append(ti)
data['number'] = number
print(data)
#data.plot.bar()
#plt.xlabel("tt number")
#plt.ylabel('Queueing time (us)')
#plt.title("Queueing Time ")

#plt.show()
link_slot['link name'].plot.bar()
for a,b in zip(link_slot['number'], link_slot['link name']):
    plt.text(a, b+0.001, '%d' %b, ha = 'center', va = 'bottom', fontsize=9)

plt.xlabel("link's name")
plt.ylabel('slot count (unit slot)')
plt.title("rtns each link use slots ")
plt.show()

data['queueing time'].plot.bar()
#plt.grid(axis='y')
for a,b in zip(data['number'],data['queueing time']):
    plt.text(a, b+0.001, '%.2f' %b, ha = 'center', va = 'bottom', fontsize=9)
plt.xlabel("tt number")
plt.ylabel('Queueing time (us)')
plt.title("rtns Queueing Time ")
plt.show()
print("constraint count ", constraint_count)
print("variable count ", variable_count)
