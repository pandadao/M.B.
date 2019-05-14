from gurobipy import *

m = Model('Protorype example_type1')

#x1 = m.addVar(lb=0,ub=2,vtype=GRB.CONTINUOUS, name = 'x1')
x1 = m.addVar(lb=0,ub=2,vtype=GRB.BINARY, name = 'x1')
x2 = m.addVar(lb=0,ub=2,vtype=GRB.BINARY, name = 'x2')
#x3 = m.addVar(lb=0,vtype=GRB.BINARY, name = 'x3')
#x4 = m.addVar(lb=0,vtype=GRB.BINARY, name = 'x4')


x5 = m.addVar(lb=0,vtype=GRB.BINARY, name = 'x5')

m.update()

m.setObjective(x1+x2,GRB.MINIMIZE)
#m.setObjective(x1+x2+3*x3+3*x4,GRB.MAXIMIZE)

m.addConstr(-x1+x2-10000*x5<=-1,'c0')
m.addConstr(-x2+x1+10000*x5<=9999,'c1')
#m.addConstr(x3==0,'c2')
#m.addConstr(x4==0,'c3')
m.addConstr(x5<=1,'c4')

#x.vtype=GRB.BINARY
m.optimize()

print('obj:%d' % m.objVal)
for v in m.getVars():
    print('%s:%d' %(v.varName, v.x))

