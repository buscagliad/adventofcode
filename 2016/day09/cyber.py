# test.txt should be 42
import copy

def decomp(l, part1 = True):
    if not l[0] == '(' : return 1
    ## assumed first part is (NxR)
    j = l.find(')')
    w = l[1:j].split('x')
    cnt = int(w[0]) * int(w[1])
    if part1: return cnt
    cnt *= decomp(l[j+1:])
    return cnt

def breakout(l):
    if not l[0] == '(' : return 1
    ## assumed first part is (NxR)
    j = l.find(')')
    w = l[1:j].split('x')
    return int(w[0]), int(w[1])

def process(l):
    i = 0
    count = 0
    while i < len(l)-1:
        #print(count, " ", l[i:])
        if l[i] == '\n' : return count
        elif l[i] == '(':
            ## process marker
            ## letcount x repeat
            j = l[i:].find(')')
            pr = copy.deepcopy(l[i+1:j+i])
            w = pr.split('x')
            #cnt = int(w[0]) * int(w[1])
            #print(pr, w, cnt)
            count += decomp(l[i:], True)
            #count += cnt
            i = i+j+int(w[0])+1
        else:
            count += 1
            i += 1
    return count

def processx(l, m, n):
    if (m > n):
        #print("*******************")
        return 0
    if m >= n: return 0
    elif l[m] == '(':
        c, r = breakout(l[m:])
        #print (m,l[m],n,l[n-1],c,l[c],r)
        k = l[m:].find(')') + 1 + m
        return r * process2(l, k, k+c-1) + process2(l, k+c, n)
    else:
        k = l[m:].find('(')
        if k == -1:
            return n - m + 1
        return k + process2(l, k+m, n)

    
def process2(l):
    rv = 0
    i = 0
    while i < len(l):
        if l[i] == '(':
            c, r = breakout(l[i:])
            #print (m,l[m],n,l[n-1],c,l[c],r)
            # k = l[i:].find(')') + 1 + i
            i = l.index(')', i+1) + 1
            rv += r * process2(l[i:i+c])
            i += c
        else:
            rv += 1
            i += 1
    return rv
        
for line in open('data.txt'):
#    print(process2(line.strip(), 0, len(line)-2))
    c1 = process(line.strip())
    print("Part 1: decompressed count is: ", c1)
    c2 = process2(line.strip())
    print("Part 2: decompressed count is: ", c2)
    # 407575789 is too low
    # too low:  10387474864
    # Part 2: decompressed count is:  10723077687
    # 10915059201
