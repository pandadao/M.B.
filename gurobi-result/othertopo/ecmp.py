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

graph_4 = {

	'E1':{'E7':0.1},
	'E2':{'E7':0.2},
	'E3':{'E7':0.3},
	'E4':{'E8':0.1},
	'E5':{'E8':0.2},
	'E6':{'E8':0.3},
        'E7':{'E1':0.1, 'E2':0.2, 'E3':0.3, 'E8':0.1, 'E9':0.1, 'E10':0.1},
        'E8':{'E4':0.1, 'E5':0.2, 'E6':0.3, 'E7':0.1, 'E9':0.1, 'E11':0.1},
        'E9':{'E8':0.1, 'E7':0.1},
        'E10':{'E7':0.1, 'E11':0.1},
        'E11':{'E10':0.1, 'E8':0.1},

}
graph_3 = {


	'E1':{'E8':0.3},
	'E2':{'E9':0.3},
	'E3':{'E11':0.2},
	'E4':{'E11':0.1},
	'E5':{'E10':0.2},
	'E6':{'E10':0.3},
	'E7':{'E8':0.1},
	'E8':{'E1':0.3,'E7':0.1,'E10':0.1,'E9':0.1,},
	'E9':{'E2':0.3,'E8':0.1,'E10':0.1,'E11':0.1},
	'E10':{'E9':0.1,'E8':0.1,'E6':0.3,'E5':0.2},
	'E11':{'E3':0.2,'E9':0.1,'E4':0.1},
        
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
#TODO: this will return ecmp not shortest path, need to change
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

