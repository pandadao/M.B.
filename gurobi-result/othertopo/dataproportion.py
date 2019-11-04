import numpy as np

from function_tool import combine, lcms

frame_numbers =int(input("how many flows: ")) #記錄目前打算排成的TT數量,random產生
print("generating %d tt flows"%(frame_numbers))
host_node = [1,2,3,4,5,6,7]
period_list = [100,200]

hyper_period = 1
for i in range(len(period_list)):
    hyper_period = lcms(period_list[i], hyper_period)
print(hyper_period)

fo = open("Limited_flow_data-%d.txt"%(frame_numbers), 'w')

for j in range(frame_numbers):
    src = np.random.choice(host_node)
    dest = np.random.choice(host_node)
    period = np.random.choice(period_list)
    size = np.random.randint(46,101)

    while src == dest:
        src = np.random.choice(host_node)
        dest = np.random.choice(host_node)
    fo.write(str(period)+' '+str(src)+' '+str(dest)+' '+str(size)+' '+str(j+1)+' '+str(int(hyper_period*0.2))+'\n')
fo.close()
'''
for j in range(75):

    src = np.random.choice(host_node)
    dest = np.random.choice(host_node)
    period = int(period_list[0])
    size = np.random.randint(46,80)
    while src == dest:
        src = np.random.choice(host_node)
        dest = np.random.choice(host_node)
    fo.write(str(period)+' '+str(src)+' '+str(dest)+' '+str(size)+' '+str(j+1)+' '+str(int(hyper_period*0.2))+'\n')

for j in range(75):

    src = np.random.choice(host_node)
    dest = np.random.choice(host_node)
    period = int(period_list[1])
    size = np.random.randint(46,80)
    while src == dest:
        src = np.random.choice(host_node)
        dest = np.random.choice(host_node)
    fo.write(str(period)+' '+str(src)+' '+str(dest)+' '+str(size)+' '+str(j+76)+' '+str(int(hyper_period*0.2))+'\n')
'''
'''
if (frame_numbers%2) == 1:
    
    middle_value = int(frame_numbers/2)
    for j in range(middle_value):

        src = np.random.choice(host_node)
        dest = np.random.choice(host_node)
        period = int(period_list[0])
        size = np.random.randint(46,80)
        while src == dest:
            src = np.random.choice(host_node)
            dest = np.random.choice(host_node)
        fo.write(str(period)+' '+str(src)+' '+str(dest)+' '+str(size)+' '+str(j+1)+'\n')


    for j in range(middle_value+1):

        src = np.random.choice(host_node)
        dest = np.random.choice(host_node)
        period = int(period_list[1])
        size = np.random.randint(46,80)
        while src == dest:
            src = np.random.choice(host_node)
            dest = np.random.choice(host_node)
        fo.write(str(period)+' '+str(src)+' '+str(dest)+' '+str(size)+' '+str(j+middle_value+1)+'\n')
    middle_value = int(frame_numbers/2)

else:

    middle_value = int(frame_numbers/2)
    for j in range(middle_value):

        src = np.random.choice(host_node)
        dest = np.random.choice(host_node)
        period = int(period_list[0])
        size = np.random.randint(46,80)
        while src == dest:
            src = np.random.choice(host_node)
            dest = np.random.choice(host_node)
        fo.write(str(period)+' '+str(src)+' '+str(dest)+' '+str(size)+' '+str(j+1)+'\n')


    for j in range(middle_value):

        src = np.random.choice(host_node)
        dest = np.random.choice(host_node)
        period = int(period_list[1])
        size = np.random.randint(46,80)
        while src == dest:
            src = np.random.choice(host_node)
            dest = np.random.choice(host_node)
        fo.write(str(period)+' '+str(src)+' '+str(dest)+' '+str(size)+' '+str(j+middle_value+1)+'\n')
'''



fo.close()
