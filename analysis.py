#-*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def parse_if_number(s):
    try: return float(s)
    except:return True if s=="true" else False if s == "false" else s if s else None

def parse_ndarray(s):
    return np.fromstring(s, sep=' ') if s else None

#anaf = pd.read_csv('/home/zdlee/omnetpp-5.4.1/newNesting/nesting/simulations/examples/results_SimpleTopo4/vec.csv')

#print(anaf.head())
'''
fo = open('/home/zdlee/omnetpp-5.4.1/newNesting/nesting/simulations/examples/results_SimpleTopo4/routing.csv')

count = 0
for line in fo:
    if 'queues[7]' in line:
        print(line)
        count = count +1
    else:
        pass
print(count)
'''

routing = pd.read_csv('/home/zdlee/omnetpp-5.4.1/newNesting/nesting/simulations/examples/results_SimpleTopo4/routing.csv', converters = {
    'attrvalue': parse_if_number,
    'binedges': parse_ndarray,
    'binvalues': parse_ndarray,
    'vectime': parse_ndarray,
    'vecvalue': parse_ndarray})

vectors = routing[routing.type == 'vector']
#print(len(vectors))
#print(vectors.name.unique(), vectors.module.unique())

vec = vectors[vectors.name == 'queueingTime:vector']
'''
plt.plot(vec.vectime, vec.vecvalue, drawstyle = 'steps-post')
plt.xlim(0,100)
plt.show()
'''
for row in vec.itertuples():
    plt.plot(row.vectime, row.vecvalue, drawstyle = 'steps-post')
plt.title(vec.name.values[0])
plt.legend(vec.module)
plt.ylim(0,)
plt.show()
