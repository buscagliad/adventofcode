import copy

def spin(p, c):
    r = copy.deepcopy(p)
    k = len(p) - c
    r = r[k:] + r[:k]
    for i, a in enumerate(r):
        p[i] = a

def swap(p, f, t):
    a = p[f]
    p[f] = p[t]
    p[t] = a

def modp(p, cmd):
    c = cmd[0]
    if c == 's':
        sc = int(cmd[1:])
        spin(p, sc)
    elif c == 'x':
        if cmd[2].isdigit():
            sf = int(cmd[1:3])
            st = int(cmd[4:])
        else:
            sf = int(cmd[1])
            st = int(cmd[3:])
        swap(p, sf, st)
    elif c == 'p':
        sf = p.index(cmd[1])
        st = p.index(cmd[3])
        swap(p, sf, st)
    else:
        print("ERROR")
        exit(1)


start = "abcdefghijklmnop"
p = list(start)
'''
print(p)

modp(p, "s1")
print(p)
modp(p, "x3/4")
print(p)
modp(p, "pe/b")
'''

seen=[]
count = 0
stopflag = -1
for _ in range(1000000000):
    count += 1
    for line in open('data.txt'):
        w = line.strip().split(',')
        for cmd in w:
            modp(p, cmd)
        res = ''.join(p)
        if stopflag < 0 and res in seen:
            ls = len(seen)
            stopflag = 1000000000 % ls + ls
            #print(count, res, seen.index(res), stopflag, ls)
        else:
            seen.append(res)
    if count == stopflag:
        print("Part 2: after cycling thru 1000000000 cycles, letters are: ", res)
        break
    if count == 1:
        print("Part 1: after cycling thru commands, letters are: ", res)
