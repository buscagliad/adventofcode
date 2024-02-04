import copy

def mostchar(clist):
    maxcount = 0
    mincount = 1000000000
    maxchar = ' '
    minchar = ' '
    for ch in "abcdefghijklmnopqrstuvwxyz":
        chcount = clist.count(ch)
        if chcount > maxcount:
            maxcount = chcount
            maxchar = ch
        if chcount < mincount and chcount >= 1:
            mincount = chcount
            minchar = ch
    return minchar, maxchar

first = True
charray = [[]]
chlength = 0
def process(line):
    global first
    global chlength
    if first:
        chlength = len(line)
        charr = []
        for i in range(len(line)):
            charray.append(copy.deepcopy(charr))
        first = False
    i = 0
    for a in line:
        charray[i].append(a)
        i += 1

for line in open('data.txt'):
    process(line.strip())

msg1=''
msg2=''
for i in range(chlength):
    b, a = mostchar(charray[i])
    msg1 += a
    msg2 += b
    
print("Part 1: message is: ", msg1)
    
print("Part 2: message is: ", msg2)
