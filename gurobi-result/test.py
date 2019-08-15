from gurobipy import *

m = Model('Protorype example_type1')

M = 10000
e = 0.0001

y = m.addVar(lb = 0, ub = 1, vtype = GRB.INTEGER, name = 'y')
x1 = m.addVar(lb = 1, vtype = GRB.INTEGER, name = 'x1')
x2 = m.addVar(lb = 1, vtype = GRB.INTEGER, name = 'x2')
x3 = m.addVar(lb = 1, vtype = GRB.INTEGER, name = 'x3')

m.addConstr(x3 == 1, 'c4')
m.addConstr(x2-x1+M*y >= e, 'c5')
m.addConstr(x2-x1+M*y <= M-e, 'c6')

m.setObjective(x1+x2, GRB.MINIMIZE)

m.update()
m.optimize()

for v in m.getVars():
    print('%s:%d' %(v.varName, v.x))
