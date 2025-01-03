import copy

keys=[]
locks=[]
height=-1
width=-1

def process(fn):
    global keys, locks, height, width
    KEY = 1
    LOCK = 2
    UNK = 0
    kltype = UNK
    n = 0
    for nl in open(fn):
        l = nl.strip()
        if len(l) < 1:
            if height < 0: height = n
            if kltype == KEY: keys.append(copy.deepcopy(kl))
            elif kltype == LOCK: locks.append(copy.deepcopy(kl))
            else: print("ERROR at ", l)
            kltype = UNK
            continue
        if kltype == UNK:
            if width < 0 : width = len(l)
            n = 1
            kl = [0] * len(l)
            if l[0] == '#':
                kltype = KEY
                for i in range(len(l)):
                    kl[i] = 1
            else:
                kltype = LOCK
                for i in range(len(l)):
                    kl[i] = 0
                
            continue
        n += 1
        for j, a in enumerate(l):
            if a == '#': kl[j] += 1
           
process('data.txt')
'''
print("KEYS: ")
print(keys)
print("LOCKS:")
print(locks)
print(height)
'''

count = 0
for l in locks:
    for k in keys:
        match = True
        #print(l, " vs ", k)
        for i in range(width):
            if k[i] + l[i] > height:
                match = False
                break
        if match: count += 1

print("Part 1: number of possible lock/key combos is: ", count)
