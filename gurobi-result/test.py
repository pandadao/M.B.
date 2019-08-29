from gurobipy import *

for i in range(4):
    m = Model('Protorype example_type1')

    M = 10000
    e = 0.0001

    y = m.addVar(lb = 0, ub = 1, vtype = GRB.BINARY, name = 'y')
    x1 = m.addVar(lb = int(i), vtype = GRB.INTEGER, name = 'x1')
    x2 = m.addVar(lb = int(i), vtype = GRB.INTEGER, name = 'x2')
    n3 = m.addVar(lb = int(i), vtype = GRB.INTEGER, name = 'n3')
    n4 = m.addVar(lb = int(i), vtype = GRB.INTEGER, name = 'n4')

    m.addConstr(n3 == int(i), 'c4')
    m.addConstr(n3-x1+M*y >= e, 'c5')
    m.addConstr(n3-x1+M*y <= M-e, 'c6')


    m.addConstr(n4 == int(i+1), 'c7')
    m.addConstr(n4-x1+M*y >= e, 'c8')
    m.addConstr(n4-x1+M*y <= M-e, 'c9')


    m.setObjective(x1+x2, GRB.MINIMIZE)

    m.update()
    m.optimize()

    for v in m.getVars():
        print('%s:%d' %(v.varName, v.x))

    m.reset()
