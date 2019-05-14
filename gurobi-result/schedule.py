# -*- coding:utf-8 -*-

from gurobipy import *
import numpy as np

# list show as integer
np.set_printoptions(suppress = True)

# check the tti.L less than tti.period, from foumulation 1.1
def Check_frame_transmition_time_less_than_frame_period():
       
    ttinumber = 1
    tt_data = np.zeros((50,5))
    # read file and get data
    #f = open('tt_information.txt', 'r', encoding = 'UTF-8')
    
    with open('tt_information.txt') as fp:
        for i in fp:

            #    for i in open('tt_information.txt', 'r'):
            #print (i, end = '')
            #tt src, tt.period, tt.frame_length, tt.destination
            ESname, tip, tifl, tidest = i.split(" ")
            '''
            # add tt data to tt_data list
            tt_data.append([])
            tt_data[int(ESname)-1].append([])
            tt_data[int(ESname)-1][int(ttinumber)-1].append([])
            tt_data[int(ESname)-1][int(ttinumber)-1][0] = tip
            tt_data[int(ESname)-1][int(ttinumber)-1].append([])
            tt_data[int(ESname)-1][int(ttinumber)-1][1]=tifl
            tt_data[int(ESname)-1][int(ttinumber)-1].append([])
            tt_data[int(ESname)-1][int(ttinumber)-1][2]=tidest
            '''

            tt_data[ttinumber-1][0] = int(ESname)
            tt_data[ttinumber-1][1] = int(ttinumber)
            tt_data[ttinumber-1][2] = int(tip)
            tt_data[ttinumber-1][3] = int(tifl)
            tt_data[ttinumber-1][4] = int(tidest)
        
            ttinumber = ttinumber+1
    #tt_data.astype(np.int32)
    print (tt_data)




def main():
    
    # 1. get the time triggered frame information from the file
    Check_frame_transmition_time_less_than_frame_period()


if __name__ == "__main__":
    main()
