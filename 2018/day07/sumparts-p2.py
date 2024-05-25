import sys
def printf(format, *args):
    sys.stdout.write(format % args)


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
STATUS = False
ADDON = 61
NUMWORKERS = 5
readem('data.txt')
if STATUS: print("AFTER:", after)
if STATUS: print("STEPS:", stlbls)
if STATUS: print("STEPS AFTER:", stafter)
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
workers = [' '] * NUMWORKERS
workertimes = [0] * NUMWORKERS
n = 0
for s in steps:
    if n >= len(workers): break
    if s in stafter: continue
    workers[n] = s
    workertimes[n] = ord(s) - ord('A') + ADDON
    n += 1

#
if DEBUG: print(available)

curtime = 0


while not done:
    curtime += 1
    newstep = False
    if DEBUG: print("*****************************************************")
    #
    # determine if a worker is now available
    #
    for i in range(len(workers)):
        if 0 < workertimes[i] and workertimes[i] <= curtime:
            st = workers[i]
            stepscompleted.append(st)
            newstep = True
            if DEBUG: print(curtime, ":  XX Completed step: ", st)
            #available.remove(workers[i][0])
            workers[i] = ' '
            workertimes[i] = 0
    #
    # get available list
    #
    if newstep:
        for s in stlbls:
            if not s in after: continue
            if DEBUG: print("-- checking for ", s)
            for aft in after[s]:
                use = True
                for a in after[s]:
                    if not a in stepscompleted: 
                        use = False
                        if DEBUG: print(a, " is not in ", stepscompleted)
                        break
                if use:
                    if not s in available and not s in stepscompleted and not s in workers:
                        if DEBUG: print(curtime, ": Adding ", s, " to available, needed: ", after[s])
                        available.append(s)   
    available.sort()
    #
    # assign an available worker to an available step
    rem = []
    if DEBUG and len(available) > 0: print("AVAILABLE:", available)
    for a in available:
        if DEBUG: print(curtime, " checking ", a)
        for i in range(len(workers)):
            if workers[i] == ' ':
                st = workers[i]
                if DEBUG: print(curtime, ":  Completed step: ", st)
                #if st in available: available.remove(st)
                workers[i] = a
                workertimes[i] = curtime + ord(a) - ord('A') + ADDON
                #if DEBUG: print("After: ", after[st])
                rem.append(a)
                break
    for r in rem: available.remove(r)
    rem.clear()
    
    if len(stlbls) == len(stepscompleted): 
        if DEBUG: print("len(steps): ", len(steps),
              "  len(stepscompleted): ", len(stepscompleted))
        done = True

    if STATUS:
        printf("%4d", curtime)
        for w in workers: print("    ", w, end = "")
        part1 = ""
        for s in stepscompleted: part1 += s       
        print("   ", part1)
    if DEBUG: print(curtime, "COMPLETE: ", stepscompleted, flush = True)
    if DEBUG: print(curtime, "AVAILABLE: ", available, flush = True)
    if DEBUG: print(curtime, "WORKING ", workers, flush = True)
    if DEBUG: print(curtime, "  TIMES ", workertimes, flush = True)

if DEBUG: print("COMPLETE: ", stepscompleted, flush = True)
if DEBUG: print("  -- ordered: ", sorted(stepscompleted))

part1 = ""
for s in stepscompleted:
    part1 += s

print("Part 2: time to complete all steps is: ", curtime)

# 436 and 437 is too low
