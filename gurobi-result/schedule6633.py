from gurobipy import *

m = Model('Protorype example_type1')

x1 = m.addVar(lb=0,ub=5,vtype=GRB.INTEGER, name = 'x1')
x2 = m.addVar(lb=0,ub=5,vtype=GRB.INTEGER, name = 'x2')
x3 = m.addVar(lb=0,ub=2,vtype=GRB.INTEGER, name = 'x3')
x4 = m.addVar(lb=0,ub=2,vtype=GRB.INTEGER, name = 'x4')


x5 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x5')
x6 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x6')
x7 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x7')
x8 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x8')
x9 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x9')
x10 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x10')
x11 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x11')
x12 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x12')
x13 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x13')
x14 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x14')
x15 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x15')
x16 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x16')
x17 = m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name = 'x17')


m.addConstr(x4-x3-10000*x5<=-1, 'c0')
m.addConstr(x3-x4+10000*x5<=9999, 'c1')
m.addConstr(x4-x3-10000*x6<=2, 'c2')
m.addConstr(x3-x4+10000*x6<=9999, 'c3')
m.addConstr(x2-x1-10000*x7<=-1, 'c4')
m.addConstr(x1-x2+10000*x7<=9999, 'c5')
m.addConstr(x3-x1-10000*x8<=-1, 'c6')
m.addConstr(x1-x3+10000*x8<=9999, 'c7')
m.addConstr(x3-x1-10000*x9<=-4, 'c8')
m.addConstr(x1-x3+10000*x9<=9999, 'c9')
m.addConstr(x4-x1-10000*x10<=-1, 'c10')
m.addConstr(x1-x4+10000*x10<=9999, 'c11')
m.addConstr(x4-x1-10000*x11<=-4, 'c12')
m.addConstr(x1-x4+10000*x11<=10002, 'c13')
m.addConstr(x3-x2-10000*x12<=-1, 'c14')
m.addConstr(x2-x3+10000*x12<=9999, 'c15')
m.addConstr(x3-x2-10000*x13<=-4, 'c16')
m.addConstr(x2-x3+10000*x13<=10002, 'c17')
m.addConstr(x4-x2-10000*x14<=-1, 'c18')
m.addConstr(x2-x4+10000*x14<=9999, 'c19')
m.addConstr(x4-x2-10000*x15<=-4, 'c20')
m.addConstr(x2-x4+10000*x15<=10002, 'c21')
m.addConstr(x4-x3-10000*x16<=-1, 'c22')
m.addConstr(x3-x4+10000*x16<=9999, 'c23')
m.addConstr(x4-x3-10000*x17<=-4, 'c24')
m.addConstr(x3-x4+10000*x17<=10002, 'c25')



m.update()
m.optimize()
m.setObjective(x1+x2+2*x3+2*x4+49.2,GRB.MINIMIZE)

print('obj: %d'% m.objVal)

for v in m.getVars():
    print('%s:%d' %(v.varName, v.x))
