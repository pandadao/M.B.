from priodict import priorityDictionary
from collections import defaultdict
from collections import OrderedDict
import sys

graph_2 = {
        
        'R1':{'R2':5,'R3':5},
	'R2':{'R1':5,'R4':5},
	'R3':{'R1':5,'R4':5},
	'R4':{'R2':5,'R3':5,'R5':5},
	'R5':{'R4':5}
        
        }

graph_3 = {

	'E1':{'E8':1},
	'E2':{'E8':1},
	'E3':{'E9':1},
	'E4':{'E10':1},
	'E5':{'E11':1},
	'E6':{'E11':1},
	'E7':{'E12':1},
        'E8':{'E1':1, 'E2':1, 'E9':1, 'E11':1, 'E10':1},
        'E9':{'E8':1, 'E3':1, 'E11':1, 'E10':1},
        'E10':{'E8':1, 'E9':1, 'E11':1, 'E4':1},
        'E11':{'E10':1, 'E8':1, 'E9':1, 'E12':1, 'E6':1, 'E5':1},
        'E12':{'E11':1, 'E7':1}

}


def Dijkstra(g,start,end=None):

    d = {}  # dictionary of final distances
    p = {}  # dictionary of predecessors
    q = priorityDictionary()   # est.dist. of non-final vert.
    q[start] = 0
    for v in q:
        d[v] = q[v]
        if v == end: break      
        for w in g[v]:
            vwLength = d[v] + g[v][w]
            if w in d:
                if vwLength < d[w]:
                    raise ValueError
            elif w not in q or vwLength < q[w]:
                q[w] = vwLength
                p[w] = [v]
            elif  w not in q or vwLength == q[w]:
                q[w] = vwLength
                p[w] += [v] 
    return (d,p)        

def shortestPath(g,start,end):

    d,p = Dijkstra(g,start,end)
    path = [[end]]
    while True:
        if len(p[end]) > 1:
            path.append(p[end])
            for node in p[end]:
                if node != start:
                    if ''.join(p[end]) == start: break
                    end = node
        path.append(p[end])
        if ''.join(p[end]) == start: break
        for node in p[end]:
            if node == start: break
            end = node  
    return path[::-1]


#print shortestPath(graph_3, 'E3', 'E1')


#recursive print the ECMP result
for i in range(7):
    for j in range(7):
        src = 'E'+str(i+1)
        dest = 'E' + str(j+1)
        if (i != j):
            print shortestPath(graph_3, src, dest)
        else:
            None
            
'''
a = 1
while (a == 1):
    src = raw_input("start src node: ")
    dest = raw_input("destination node: ")
    print shortestPath(graph_3, src, dest)
    a = input()
'''
'''
print shortestPath(graph_2,'R5','R1')
print shortestPath(graph_3,'192.168.255.4','192.168.255.1')
print shortestPath(graph_4,'R4','R1')
print shortestPath(graph_5,'A','C')
'''
