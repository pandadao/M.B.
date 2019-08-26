from gurobipy import *
from function_tool import combine, lcms
from getport import *
import time
from ecmp import *

import numpy as np

m = Model('Protorype example_type1')

#變數區
M = 10000  # M是一個極大值,用來運作 cplex中的either-or 工能
hyper_period = 1 # LCM求出的最大週期,先以常數項代替
x_number = 0 # cplex的變數量, x1,x2,x3等
c_number = 0 # 限制式編號變數
IFG = 96     # inter frame gap, 單位是bit,假設在1Gbps線路上傳,則是 96/1000us,若是100mbps,則是96/1000000000*1000000 = 0.96us
obj = 0.0  #目標式參數
procedelay = 1

start_time = time.time()

send_src = []   #紀錄哪些節點是host發送端
path_node = []  #紀錄哪些節點是中繼的switch

#將tt資訊讀取出來並儲存成陣列
n = 0
tmp_list = []
tt_count = []
'''
frame_numbers = 25 #記錄目前打算排成的TT數量,random產生
host_node = [1,2,3,4,5,6]
period_list = [100,150,200]

fo = open("Limited_flow_data.txt", 'w')
for j in range(frame_numbers):
    src = np.random.choice(host_node)
    dest = np.random.choice(host_node)
    period = np.random.choice(period_list)
    size = np.random.randint(46,101)

    while src == dest:
        src = np.random.choice(host_node)
        dest = np.random.choice(host_node)
    fo.write(str(period)+' '+str(src)+' '+str(dest)+' '+str(size)+' '+str(j+1)+'\n')
fo.close()
'''


#fp = open("tt_information.txt",'r')
fp = open("Limited_flow_data.txt",'r')
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


#取所有的tt組合配對: 1,2 1,3 1,4 2,3 2,4 3,4
#pair = combine([1,2,3,4], 2)
pair = combine(tt_count,2)
#a = 1
for i in range(len(tmp_list)):
    hyper_period = lcms(int(tmp_list[i]), hyper_period)
    #print("hyper_period is : ",hyper_period)

#宣告每個TT的offset變數
for i in range(n):
    a = "tt"+str(i+1)
    tti = eval(a)
    va = "x"+str(i+1)
    #globals()['x{}'.format(i+1)] = m.addVar(1,2,3,4,5,6,7,8,9,10,11,12,vtype = GRB.INTEGER, name = va)  #offset的變數宣告完畢
    globals()['x{}'.format(i+1)] = m.addVar(lb = 0,ub = int(int(tti[0])-1),vtype = GRB.INTEGER, name = va)  #offset的變數宣告完畢
    tti.append(eval(va))
    #print("tt list :", tti)
    x_number = x_number+1
    #va = "x"+str(i+1)


#檢查TT長度是否超過自身週期,限制式1:  0<= tti.offset + tti.L + IFG time <= tti.p
ttinumber = x_number  #記錄產生了多少個offset變數,注意x_number,假設有4條tt,則現在的x_number是4
for i in range(ttinumber):
    a = "tt"+str(i+1)
    tti = eval(a)
    tti_L = (tti[3]+30)*8/1000   #頻寬的值應該要是別的變數,這邊先用1000為值。TODO:之後要將頻寬加進來運算
    #print(tti_L, type(tti_L))
    tti.append(tti_L)
    ca = "c"+str(c_number)
    c_number = c_number+1
    print(tti)
    m.addConstr(tti[5]<=tti[0]-tti[6]-0.096, ca)
    


#宣告限制式
for i in pair:
    tt_i = "tt"+ str(i[0])  #賦名稱編號給tt_i,叫做tt幾
    tt_j = "tt"+ str(i[1])
    tti = eval(tt_i)        #讓tti取得自己的陣列編號
    ttj = eval(tt_j)
    #print("tti: ", tti)
    #print("ttj: ",ttj)
    a = int(hyper_period/int(tti[0]))
    b = int(hyper_period/int(ttj[0]))
#    print("a=",a)
#    print("b=",b)
    for k in range(a):
        #print(k)
        for l in range(b):
            # 宣告ｙ的變數xi, 之後產生限制式
            va = "x" + str(x_number+1)
            globals()['x{}'.format(x_number+1)] = m.addVar(lb = 0, ub = 1, vtype = GRB.INTEGER, name = va) 
            
            #宣告c0 c1 c2編號
            ca = "c"+str(c_number)
            c_number = c_number+1
            # 把x1和tt1結合起來,產生限制式
            m.addConstr(ttj[5]-tti[5]+l*ttj[0]-k*tti[0]-M*eval(va)<=-(ttj[6]+0.096), ca)  #要保留多少gate就可以直接在0.096後面加1或n
            #宣告c0 c1 c2編號
            ca = "c"+str(c_number)
            c_number = c_number+1
            m.addConstr(tti[5]-ttj[5]+k*tti[0]-l*ttj[0]+M*eval(va)<=M-(tti[6]+0.096), ca)
            x_number = x_number+1
            #print("x_number: => ",x_number)

#動態產生目標式
for i in range(len(tt_count)):  #0 1 2 3 ...
    tt_i = "tt"+str(i+1)
    tti = eval(tt_i)
    src = 'E'+str(tti[1])
    dest = 'E'+str(tti[2])
    hop = len(shortestPath(graph_3,src,dest))-1
    a = int(hyper_period/int(tti[0]))
#    offset = 'x'+str(i+1)
#    xi = eval(offset)

    for pi in range(a):  #計算一個hyperperiod內要傳送幾次tti
        obj = tti[5]+pi*tti[0]+hop*tti[6]+0.1*hop+procedelay*(hop-1)  #這邊的propagation delay先預設0.1, TODO 需要可以動態變動

m.setObjective(obj, GRB.MINIMIZE)



m.update()
m.optimize()
count = 0
#print('obj: %d'% m.objVal)
'''
for v in m.getVars():
    print('%s:%d' %(v.varName, v.x))
'''
for v in m.getVars():
    count = count + 1
    if count > len(tt_count):
        break
    else:
        print('%s:%d' %(v.varName, v.x))

        #將offset值放入tti[5]內
        tti = "tt"+str(count)
        tti = eval(tti)
        tti[5] = int(v.x)


for i in range(len(tt_count)):
    tti = "tt"+str(i+1)
    tti = eval(tti)
    print(tti)
print(hyper_period)
print(time.time()-start_time)
'''
#TODRRRrO 利用offset值推算每個 node的xml時間檔
for i in range(len(tt_count)):
    tti = "tt"+str(i+1)
    tti = eval(tti)
    print(tti)aaaaa
    
    count_in_hyperperiod = int(hyper_period/int(tti[0]))  # how many times in a hyperperiod
    for tt in range(count_in_hyperperiod):
        src = 'E'+str(tti[1])
        dest = 'E'+str(tti[2])
        path = shortestPath(graph_3, src, dest)

        L = len(path)
        for path_record in range(L-1):
            send_node = path[path_record][0]
            receive_node = path[path_record+1][0]
            send_port = topology_3[send_node][receive_node]['port']
            if send_node == src:  #如果send_node是發送端,儲存成host格式
                
                #如果send_src陣列中還沒存進新的host,則新增
                if send_node in send_src:
                    pass
                else:
                    send_src.append(send_node)
                    #print('src')

                #加入xml相關資訊
                try:
                    Ei = eval(send_node)
                    time_record = tti[5]+tt*tti[0]
                    Ei.append({'start': time_record, 'queue':'7', 'dest': topology_3[dest]['MAC'], 'size': tti[3]})
                    #print(E1)

                except:
                    globals()[send_node] = []

                    Ei = eval(send_node)
                    time_record = tti[5]+tt*tti[0]
                    Ei.append({'start': time_record, 'queue':'7', 'dest': topology_3[dest]['MAC'], 'size': tti[3]})
                    #print(E1)


            #如果send_node是path上的中繼站(switch),則存成switch格式

            else:                                 
                #如果path_node陣列中沒有swith的紀錄,則新增進紀錄
                if send_node in path_node:
                    pass
                else:
                    path_node.append(send_node)
                    #print('switch')

                try:
                    Ei = eval(send_node)
                    # TODO 有點麻煩,需要用前一個node的發送時間去推算

# NOTE: gate open time have to keep until frame trasmit over
'''
'''
    #TODO 推算每個node的時間表
    src = 'E'+str(tti[1])
    dest = 'E'+str(tti[2])
    path = shortestPath(graph_3, src, dest)
    
    # 印出路徑上的node編號
    #print (path[1][0])
    #最後面的[1:]是將代號變為integer,例如E1變成1
    #node_record = path[0][0][1:]   #node_record 變數為路徑上的中繼點代號
    L = len(path)
    print(path)
    #print(L)
    for i in range(L-1):       #算出每個node上的gate開啟時間
        #print(path[i][0])     # start node
        #print(path[i+1][0])   # receive node
        send_node = path[i][0]
        receive_node = path[i+1][0]
        print(topology_3[send_node][receive_node])   #印出send_node的port號

        
        #TODO 推算gate時間

            檢查list是否宣吿過
            try:
                list[0]
            except:
                print('no')

        #向上取整數 => math.ceil(0.1)
        #向下取整數 => math.floor(0.1)

        #檢查dict是否存在
        try:
            dict["name"] = "dada"
        except:
            dict = {}
            dict["name'] = "dada995"
'''            
