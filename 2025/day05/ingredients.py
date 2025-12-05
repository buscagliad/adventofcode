
ranges = []
ings = []

def overlap(r1, r2):
    if r1[1] < r2[0]: return False
    if r2[1] < r1[0]: return False
    return True
    
def newranges(oldr):
    newr = []
    merged = 0
    for i, r in enumerate(oldr):
        found = False
        for j, l in enumerate(newr):
            if overlap(r, l):
                newr[j] = [min(r[0], l[0]), max(r[1], l[1])]
                merged += 1
                found = True
                break   # out of for loop
        if not found:
            newr.append(r)
    return merged, newr

def init(fname):
    global ranges, ings
    rfirst = True
    for l in open(fname, "r"):
        if len(l) < 2: 
            rfirst = False
            continue
        if rfirst:
            n = l.strip().split('-')
            ranges.append([int(n[0]), int(n[1])])
        else:
            n = l.strip()
            ings.append(int(n))
def dump():
    global ranges, ings
    for r in ranges:
        print ("Ranges: ", r)
    for i in ings:
        print ("Ingredient: ", i)

def isfresh(g):
    global ranges
    for r in ranges:
        if r[0] <= g and g <= r[1]: return True
    return False

init("data.txt")
count = 0
for i in ings:
    if isfresh(i):
        count += 1
print("Part 1: ", count)
m, nr = newranges(ranges)
#print(ranges)
while m > 0:
    m, nr = newranges(nr)
    #print(m)

count = 0
for r in nr:
    count += r[1] - r[0] + 1

print("Part 2: ", count)
