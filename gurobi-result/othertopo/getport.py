# -*- coding:utf-8 -*-


'''
topology_3 = {

	'E1':{'E7':0}, #from E1 port to E7, the number is E1's port
	'E2':{'E7':0},
	'E3':{'E7':0},
	'E4':{'E8':0},
	'E5':{'E8':0},
	'E6':{'E8':0},
        'E7':{'E1':0, 'E2':1, 'E3':2, 'E8':4}, #E7 to E1 is going from port 0
        'E8':{'E4':5, 'E5':4, 'E6':3, 'E7':1},
}
'''

topology_4 = {
        
        'E1':{'portNumber':1, 'MAC':'00:00:00:00:00:01', 'E7':{'propDelay':0.1, 'port': 0}}, # E7後面的數字為E1連接到E7的port號,不是E7的port號
        'E2':{'portNumber':1, 'MAC':'00:00:00:00:00:02', 'E7':{'propDelay':0.2, 'port': 0}},
        'E3':{'portNumber':1, 'MAC':'00:00:00:00:00:03', 'E7':{'propDelay':0.3, 'port': 0}},
        'E4':{'portNumber':1, 'MAC':'00:00:00:00:00:04', 'E8':{'propDelay':0.1, 'port': 0}},
        'E5':{'portNumber':1, 'MAC':'00:00:00:00:00:05', 'E8':{'propDelay':0.2, 'port': 0}},
        'E6':{'portNumber':1, 'MAC':'00:00:00:00:00:06', 'E8':{'propDelay':0.3, 'port': 0}},
        'E7':{'portNumber':4, 'E1':{'propDelay':0.1, 'port': 0}, 
                              'E2':{'propDelay':0.2, 'port':1}, 
                              'E3':{'propDelay':0.3, 'port':2}, 
                              'E8':{'propDelay':0.1, 'port':4},
            },
        'E8':{'portNumber':4, 'E4':{'propDelay':0.1, 'port':5}, 
                              'E5':{'propDelay':0.2, 'port':4}, 
                              'E6':{'propDelay':0.3, 'port':3}, 
                              'E7':{'propDelay':0.1, 'port':1},
            },
        }

topology_3 = {
        
        'E1':{'portNumber':1, 'MAC':'00:00:00:00:00:01', 'E8':{'propDelay':0.3, 'port': 0}}, # E7後面的數字為E1連接到E7的port號,不是E7的port號
        'E2':{'portNumber':1, 'MAC':'00:00:00:00:00:02', 'E9':{'propDelay':0.3, 'port': 0}}, 
        'E3':{'portNumber':1, 'MAC':'00:00:00:00:00:03', 'E11':{'propDelay':0.2, 'port': 0}}, 
        'E4':{'portNumber':1, 'MAC':'00:00:00:00:00:04', 'E11':{'propDelay':0.1, 'port': 0}}, 
        'E5':{'portNumber':1, 'MAC':'00:00:00:00:00:05', 'E10':{'propDelay':0.2, 'port': 0}}, 
        'E6':{'portNumber':1, 'MAC':'00:00:00:00:00:06', 'E10':{'propDelay':0.3, 'port': 0}}, 
        'E7':{'portNumber':1, 'MAC':'00:00:00:00:00:07', 'E8':{'propDelay':0.1, 'port': 0}}, 
        'E8':{'portNumber':4, 'E1':{'propDelay':0.3, 'port': 0},
                              'E7':{'propDelay':0.1, 'port': 1},
                              'E10':{'propDelay':0.1, 'port': 2},
                              'E9':{'propDelay':0.1, 'port': 3},



            }, 
        'E9':{'portNumber':4, 'E2':{'propDelay':0.3, 'port': 0},
                              'E8':{'propDelay':0.1, 'port': 1},
                              'E10':{'propDelay':0.1, 'port': 2},
                              'E11':{'propDelay':0.1, 'port': 3},



            }, 
        'E10':{'portNumber':4,'E9':{'propDelay':0.1, 'port': 0},
                              'E8':{'propDelay':0.1, 'port': 1},
                              'E6':{'propDelay':0.3, 'port': 2},
                              'E5':{'propDelay':0.2, 'port': 3},



            }, 
        'E11':{'portNumber':3,'E3':{'propDelay':0.2, 'port': 0},
                              'E9':{'propDelay':0.1, 'port': 1},
                              'E4':{'propDelay':0.1, 'port': 2},


            },

        
        }
#print (topology_3['E7']['E2'])
