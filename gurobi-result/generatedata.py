import numpy as np
from function_tool import combine, lcms
import math

host_node = [1,2,3,4,5,6]
period_list = [10, 15, 20]

periodkind = int(len(period_list))


fo = open("Limited_flow_data.txt", 'w')

Hperiod = 1

for i in range(len(period_list)):
    Hperiod = lcms(int(period_list[i]), Hperiod)
    
print("hyper period is ", Hperiod)

total_numbers = 0
for i in range(len(period_list)):
    total_numbers = total_numbers + int(Hperiod/period_list[i])

print("total numbers: ", total_numbers)

x = math.floor(Hperiod/total_numbers)
print(x)

total_use_slot = 0

for i in range(len(period_list)):
    total_use_slot = (Hperiod/period_list[i])*x + total_use_slot

remaining_slot = int(Hperiod - total_use_slot)
print("remaining slot is ", remaining_slot)
