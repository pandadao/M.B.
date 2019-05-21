import copy

def combine(l,n):
    answer = []
    one = [0]*n
    
    def next_c(li = 0, ni = 0):
        if ni == n:
            answer.append(copy.copy(one))
            return
        for lj in range(li, len(l)):
            one[ni] = l[lj]
            next_c(lj+1, ni+1)
    next_c()
    return answer
