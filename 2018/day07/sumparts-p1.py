
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

orders = []

steps = {}

stlbls = set()
stafter = set()
after = {}

def readem(f):
    global orders
    global steps
    global stlbls, stafter
    for line in open(f):
        w = line.split()
        fi = w[1]
        af = w[7]
        stlbls.add(fi)
        stlbls.add(af)
        stafter.add(af)
        if not af in after:
            after[af] = []
        after[af].append(fi)
        if fi in steps:
            steps[fi].append(af)
        else:
            steps[fi] = [af]


DEBUG = False

readem('data.txt')
if DEBUG: print("AFTER:", after)
if DEBUG: print("STEPS:", stlbls)
if DEBUG: print("STEPS AFTER:", stafter)
#exit(1)

#
# determine which step is not in after list
#
stepscompleted = []
done = False
available = []

##
# create available list based on all steps that have not precursor
##
for s in steps:
    if s in stafter: continue
    available.append(s)


#
if DEBUG: print(available)

workers = [0] * 5
curtime = 0

for i, a in enumerate(available):
    workers[i] = ord(a) - ord('A') + 61

while not done:
    if DEBUG: print("*****************************************************")
    available.sort()
    st = available[0]

    stepscompleted.append(st)
    available.remove(st)
    #
    # with st, check if it releases any new steps to be available
    #
    for st in steps:
        if DEBUG: print("Looking at step: ", st)
        #if st in stepscompleted: 
        #    print("  --- passing, already in complete")
        #    continue
        #
        # check to see if each after check is in the available or
        # completed list
        #
        use = True
        if not st in after: continue
        if DEBUG: print("After: ", after[st])
        for s in stlbls:
            use = True
            if s in after:
                for r in after[s]:
                    if not r in stepscompleted: use = False
            if use:
                if not s in available and not s in stepscompleted:
                    available.append(s)
    if len(stlbls) == len(stepscompleted): 
        if DEBUG: print("len(steps): ", len(steps),
              "  len(stepscompleted): ", len(stepscompleted))
        done = True

    if DEBUG: print("COMPLETE: ", stepscompleted, flush = True)
    if DEBUG: print("AVAILABLE: ", available, flush = True)

if DEBUG: print("COMPLETE: ", stepscompleted, flush = True)

part1 = ""
for s in stepscompleted:
    part1 += s

print("Part 1: correct order is: ", part1)

