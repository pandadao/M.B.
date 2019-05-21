'''
dynamic call the list value,動態呼叫陣列並讀取陣列中的值

tt1 = []
tt2 = []
tt3 = []
tt1.append(1)
tt1.append(4)
tt2.append(2)
tt2.append(5)
tt3.append(3)
tt3.append(6)
for i in range(3):
    a = "tt"+ str(i+1)
    #print (eval(a))
    tti = eval(a)
    print(tti[1])
'''


'''
動態宣告變數名稱,可以將變數x1 x2 x3依照順序宣告賦值


for i in range(10):
    globals()['x{}'.format(i+1)] = i
    va = "x"+str(i+1)
    print(eval(va))
'''

'''
a = 12
b = 6
c = 3
d = 2
'''
'''
for i in range(int(a/b)):
    print (i)

for i in range(int(a/d)):
    print (i)
'''
'''
tt1 = [6,1,1]
va = "tt"+ str(1)
tti = eval(va)
for a in range(int(a/tti[0])):
    print (a)
'''

'''
實作combinations工能
import copy

def combine(l,n):
        answer = []
        one = [0]*n
        def next_c(li = 0, ni = 0):
            if ni ==n:
                answer.append(copy.copy(one))
                return 
            for lj in range(li, len(l)):
                one[ni] = l[lj]
                next_c(lj+1, ni+1)

        next_c()
        return answer
print (combine([1,2,3,4],2))
'''
