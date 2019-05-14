from gurobipy import *

m = Model('Protorype example_type1')

x1 = m.addVar(lb=0,ub=2,vtype=GRB.INTEGER, name = 'x1')
x2 = m.addVar(lb=0,ub=2,vtype=GRB.INTEGER, name = 'x2')
x3 = m.addVar(lb=0,ub=2,vtype=GRB.INTEGER, name = 'x3')

#x4 = m.addVar(lb=0,ub=1,vtype=GRB.BINARY, name = 'x4')
x4 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x4')
x5 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x5')
x6 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x6')

m.update()

m.setObjective(x1+x2+x3,GRB.MAXIMIZE)

m.addConstr(x2-x1-10000*x4<=-1, 'c0')
m.addConstr(x1-x2+10000*x4<=9999, 'c1')
m.addConstr(x3-x1-10000*x5<=-1, 'c2')
m.addConstr(x1-x3+10000*x5<=9999, 'c3')
m.addConstr(x2-x3-10000*x6<=-1, 'c4')
m.addConstr(x3-x2+10000*x6<=9999, 'c5')


m.optimize()

print('obj: %d' %m.objVal)
for v in m.getVars():
    print('%s:%d' %(v.varName, v.x))

