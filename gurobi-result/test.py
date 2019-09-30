from gurobipy import *
import math

from operator import itemgetter

'''
b = [[1,2,3,4,5], [54,3,2,1], [6,7,5,3,7]]
yo = sorted(b, key = itemgetter(2))
print(yo)
'''
#not equal != 的實作

for i in range(4):
    m = Model('Protorype example_type1')

    M = 10000
    e = 0.0001

    y = m.addVar(lb = 0, ub = 1, vtype = GRB.BINARY, name = 'y')
    x1 = m.addVar(lb = int(i), vtype = GRB.INTEGER, name = 'z1')
    x2 = m.addVar(lb = int(i), vtype = GRB.INTEGER, name = 'z2')
    n3 = m.addVar(lb = int(i), vtype = GRB.INTEGER, name = 'm3')
    n4 = m.addVar(lb = int(i), vtype = GRB.INTEGER, name = 'm4')

    m.addConstr(n3 == int(i), 'c4')
    m.addConstr(n3-x1+M*y >= e, 'c5')
    m.addConstr(n3-x1+M*y <= M-e, 'c6')


    m.addConstr(n4 == int(i+1), 'b4')
    m.addConstr(n4-x1+M*y >= e, 'b5')
    m.addConstr(n4-x1+M*y <= M-e, 'b6')


    m.setObjective(x1+x2, GRB.MINIMIZE)

    m.update()
    m.optimize()

    for v in m.getVars():
        if v.varName == 'z1':
            print('z1 is %s:%d' %(v.varName, v.x))
            print(type(v))
            print(type(v.varName))
            print(type(v.x))
        else:
            #print('%s:%d' %(v.varName, v.x))
            pass
    #a = m.getVars()
    #print(a)
    #print(a[0])

    m.reset()
'''
M = 10000
m = Model('Protorype exanple_type1')
x1 = m.addVar(lb = 0, vtype = GRB.INTEGER, name = 'x1')
y = m.addVar(lb = 0, ub = 1, vtype = GRB.BINARY, name = 'y')
m.addConstr(x1+M*y>=1, 'c1')
m.addConstr(x1+M*y<=3, 'c2')

m.setObjective(x1, GRB.MINIMIZE)
m.update()
m.optimize()
'''
