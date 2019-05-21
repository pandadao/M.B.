from gurobipy import *
from function_tool import combine, lcms

m = Model('Protorype example_type1')


'''
tt1 = [6,1,1]
tt2 = [6,1,2]
tt3 = [3,1,3]
tt4 = [3,1,4]
'''
'''
6633排程
'''
M = 10000  # M是一個極大值,用來運作 cplex中的either-or 工能
hyper_period = 1 # LCM求出的最大週期,先以常數項代替
x_number = 0 # cplex的變數量, x1,x2,x3等
c_number = 0


#將tt資訊讀取出來並儲存成陣列
n = 0
tmp_list = []
tt_count = []
fp = open("tt_information.txt",'r')
for i in fp:
    globals()["tt{}".format(n+1)] = []
    a = "tt"+str(n+1)
    tti = eval(a)
    period, length, number = i.rstrip('\n').split(" ")
    tti.append(int(period))
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
    globals()['x{}'.format(i+1)] = m.addVar(lb = 0,ub = int(int(tti[0])-1),vtype = GRB.INTEGER, name = va)
    tti.append(eval(va))
    #print("tt list :", tti)
    x_number = x_number+1
    #va = "x"+str(i+1)

#宣告限制式
for i in pair:
    tt_i = "tt"+ str(i[0])  #賦名稱編號給tt_i,叫做tt幾
    tt_j = "tt"+ str(i[1])
    tti = eval(tt_i)        #讓tti取得自己的陣列編號
    ttj = eval(tt_j)
    print("tti: ", tti)
    print("ttj: ",ttj)
    a = int(hyper_period/int(tti[0]))
    b = int(hyper_period/int(ttj[0]))
    print("a=",a)
    print("b=",b)
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
            m.addConstr(ttj[3]-tti[3]+l*ttj[0]-k*tti[0]-M*eval(va)<=-1, ca)
            #宣告c0 c1 c2編號
            ca = "c"+str(c_number)
            c_number = c_number+1
            m.addConstr(tti[3]-ttj[3]+k*tti[0]-l*ttj[0]+M*eval(va)<=M-1, ca)
            x_number = x_number+1
            #print("x_number: => ",x_number)


m.setObjective(x1+x2+2*x3+2*x4+49.2,GRB.MAXIMIZE)
m.update()
m.optimize()

print('obj: %d'% m.objVal)

for v in m.getVars():
    print('%s:%d' %(v.varName, v.x))
