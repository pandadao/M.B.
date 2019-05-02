from priodict import priorityDictionary
from collections import defaultdict
from collections import OrderedDict
import sys
graph_2  = {

'R1':{'R2':5,'R3':5},
'R2':{'R1':5,'R4':5},
'R3':{'R1':5,'R4':5},
'R4':{'R2':5,'R3':5,'R5':5},
'R5':{'R4':5}

}

graph_3 = {

'192.168.255.1':{'192.168.255.2':10,'192.168.255.3':10},
'192.168.255.2':{'192.168.255.1':10,'192.168.255.3':50},
'192.168.255.3':{'192.168.255.1':20,'192.168.255.2':50},
'192.168.255.4':{'192.168.255.3':20},
'192.168.255.3':{'192.168.255.4':20}
}

graph_4 = {
'R1':{'R2':5},
'R2':{'R1':5},
'R2':{'R3':5},
'R3':{'R2':5},
'R3':{'R4':5},
'R4':{'R3':5}
}

graph_5 = {

'A':{'B':5,'C':10,'E':2},
'B':{'A':5,'C':5},
'C':{'B':5,'A':10,'E':8,'D':4},
'D':{'C':4,'E':5},
'E':{'A':2,'D':5,'C':8}

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


print shortestPath(graph_2,'R5','R1')
print shortestPath(graph_3,'192.168.255.4','192.168.255.1')
print shortestPath(graph_4,'R4','R1')
print shortestPath(graph_5,'A','C')
