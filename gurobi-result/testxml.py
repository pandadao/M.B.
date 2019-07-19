from xml.dom import minidom

doc = minidom.Document()
root = doc.createElement('schedule')
#root.setAttribute('name', 'robotcontroller')

doc.appendChild(root)

nodeCycle = doc.createElement('cycle')
nodeCycle.appendChild(doc.createTextNode(str(600)))

root.appendChild(nodeCycle)

managerList = [{'start':'50', 'queue':'7', 'dest':"00:00:00:00:00:00", 'size':83},{'start':'60', 'queue':'7', 'dest':"00:00:00:00:00:00", 'size':70}]

switchList = [{'length':600, 'bitvector':'00000001'}, {'length':600, 'bitvector':'00000001'}]

nodeHost = doc.createElement('host')
nodeHost.setAttribute('name', 'robotcontrollerer')

for i in managerList:

    nodeEntry = doc.createElement('entry')
    nodeStart = doc.createElement('start')
    nodeStart.appendChild(doc.createTextNode(str(i['start'])))

    nodeQueue = doc.createElement('queue')
    nodeQueue.appendChild(doc.createTextNode(str(i['queue'])))

    nodeDest = doc.createElement('dest')
    nodeDest.appendChild(doc.createTextNode(str(i['dest'])))

    nodeSize = doc.createElement('size')
    nodeSize.appendChild(doc.createTextNode(str(i['size'])))


    nodeEntry.appendChild(nodeStart)
    nodeEntry.appendChild(nodeQueue)
    nodeEntry.appendChild(nodeDest)
    nodeEntry.appendChild(nodeSize)

    nodeHost.appendChild(nodeEntry)
    root.appendChild(nodeHost)


nodeSwitch = doc.createElement('switch')
nodeSwitch.setAttribute('name', 'switch1')


nodePort = doc.createElement('port')
nodePort.setAttribute('id','0')

for i in switchList:
    nodeEntry = doc.createElement('entry')
    nodeLength = doc.createElement('length')
    nodeLength.appendChild(doc.createTextNode(str(i['length'])))

    nodeBitvector = doc.createElement('bitvector')
    nodeBitvector.appendChild(doc.createTextNode(str(i['bitvector'])))

    nodeEntry.appendChild(nodeLength)
    nodeEntry.appendChild(nodeBitvector)
    nodePort.appendChild(nodeEntry)
    nodeSwitch.appendChild(nodePort)
    root.appendChild(nodeSwitch)




fp = open("testxml.xml", "w")
doc.writexml(fp, indent = '\t', newl = '\n')
