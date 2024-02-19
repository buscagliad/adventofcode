import copy
from itertools import combinations
import numpy as np
from collections import deque

DEBUG = False
##                0         1            2             3               4
## Floors[0]:   steps, current floor, prev floor, just moved obj1, just moved obj2 

STEPS=(0,0)
CUR_FLOOR=(0,1)
PREV_FLOOR=(0,2)
LAST_OBJ1=(0,3)
LAST_OBJ2=(0,4)

PART2 = True

# The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
# The second floor contains a hydrogen generator.
# The third floor contains a lithium generator.
# The fourth floor contains nothing relevant.
TEST = False
USE_DEQUE = True
if TEST:
    HydGen  =  1
    HydChip =  2
    LitGen  =  3
    LitChip =  4
    Gens = [HydGen, LitGen]
    Chips = [HydChip, LitChip]
    minSteps = 100
    maxSteps = 0
    NumObjs = len(Gens) + len(Chips)
    Floors = np.zeros([5,15], dtype=int)
    Floors[CUR_FLOOR] = 1
    Floors[1][HydChip] = 1
    Floors[1][LitChip] = 1
    Floors[2][HydGen] = 1
    Floors[3][LitGen] = 1

else:

    # The first floor contains a promethium generator and a promethium-compatible microchip.
    # The second floor contains a cobalt generator, a curium generator, a ruthenium generator, and a plutonium generator.
    # The third floor contains a cobalt-compatible microchip, a curium-compatible microchip, a ruthenium-compatible microchip, and a plutonium-compatible microchip.
    # The fourth floor contains nothing relevant.
    # Gen % 2 == 1
    # Chip % 2 == 0
    ProGen  =  1
    ProChip =  2
    CobGen  =  3
    CobChip =  4
    CurGen  =  5
    CurChip =  6
    RutGen  =  7
    RutChip =  8
    PluGen  =  9
    PluChip =  10

    Gens = [ProGen, CobGen, CurGen, RutGen, PluGen]
    Chips = [ProChip, CobChip, CurChip, RutChip, PluChip]
    minSteps = 50
    maxSteps = 0
    NumObjs = 10

    Floors = np.zeros([5,15], dtype=int)
    Floors[CUR_FLOOR] = 1
    Floors[1][ProGen] = 1
    Floors[1][ProChip] = 1
    Floors[2][CobGen] = 1
    Floors[2][CurGen] = 1
    Floors[2][RutGen] = 1
    Floors[2][PluGen] = 1
    Floors[3][CobChip] = 1
    Floors[3][CurChip] = 1
    Floors[3][RutChip] = 1
    Floors[3][PluChip] = 1
    if PART2:
        minSteps = 600
        maxSteps = 0
        NumObjs = 14
        EleGen  = 11
        EleChip = 12
        DilGen  = 13
        DilChip = 14
        Floors[1][EleGen] = 1
        Floors[1][EleChip] = 1
        Floors[1][DilGen] = 1
        Floors[1][DilChip] = 1
  



def compatible(obj1, obj2): # two objects are compatible if they are both generators, both chips, or if they 'balance each other'
    if obj2 == 0 or obj1 == 0: return True
    if obj1 == obj2 : 
        #print(obj1, obj2, "  MATCH")
        #exit(1)
        return True
    if obj1 % 2 == 0 and obj2 % 2 == 0: return True
    if obj1 % 2 == 1 and obj2 % 2 == 1: return True
    #
    # are objects pairs
    if abs(obj1 - obj2) == 1 and (obj1 + obj2) % 4 == 3: return True
    return False

validFloors = []

def goodFloorX(f):
    for c in range(2, len(f), 2):
        if not f[c]: continue
        if f[c-1]: continue
        else: 
            for g in range(2, len(f), 2):
                if f[g-1]: return False
    return True

def makeFloor(n):
    floor = np.zeros(11, dtype = int)
    binary_representation = bin(n)[2:]  # Get the binary representation, removing the '0b' prefix
    # print(binary_representation)
    bl = len(binary_representation)
    for i in range(bl):
        if binary_representation[i] == '1':
            floor[bl-i] = 1
    return floor

def testthis():
    count = 0
    for k in range(2**10):
        f = makeFloor(k)
        #print(f)
        if goodFloorX(f):
            #print(k, "Good ", f)
            validFloors.append(f)
            count += 1
        #else:
            #print(k, "Bad  ", f)
        
    for v in validFloors:
        print(v)
    print("Total good floors: ", count)

    exit(1) 

#testthis()
# for g in range(NumObjs+1):
    # for c in range(NumObjs+1):
        # print(g, " with ", c, " --> ", compatible(g, c))
# exit(1)

# print(Floors)
##                0         1            2             3               4
## Floors[0]:   steps, current floor, prev floor, just moved obj1, just moved obj2 

def goodFloorNOTUSED(f, obj1, obj2):
    #return True
    if not compatible(obj1, obj2): return False
    if obj1 % 2 == 1 and obj2 % 2 == 1: return True  # can always add generators
    if obj1 > 0 and obj1 % 2 == 0 and f[obj1 - 1] == 0: return False
    if obj2 > 0 and obj2 % 2 == 0 and f[obj2 - 1] == 0: return False
    return True

def goodFloorRemove(f, obj1, obj2):
    f[obj1] = 0
    if obj2 > 0: f[obj2] = 0
    return goodFloorX(f)
    # for obj1, obj2 in combinations(getFloorObjs(f), 2):
        # if not compatible(obj1, obj2): return False
    # return True

def getState(s, destination_floor, obj1, obj2):
    current_floor = s[CUR_FLOOR]
    if not compatible(obj1, obj2): return False, None
    
    stepCount = s[STEPS] + 1
    if stepCount > minSteps: return False, None # if steps exceeded - return False, None
    #
    # at this point - we have a valid floor move
    # create a copy of the state and update parameters
    #
    ns = copy.deepcopy(s)
    # 
    # remove obj1 and obj2 from ns and see if it is a good floor
    #
    ns[current_floor][obj1] = 0
    ns[current_floor][obj2] = 0
    if not goodFloorX(ns[current_floor]): return False, None
    
    #
    # add obj1 and obj2 to destination floor
    #
    if (obj1 > 0): ns[destination_floor][obj1] = 1
    if (obj2 > 0): ns[destination_floor][obj2] = 1
    if not goodFloorX(ns[destination_floor]): return False, None
    
    ns[STEPS] = stepCount
    ns[CUR_FLOOR] = destination_floor    # set current floor to destination floor
    return True, ns

def getFloorObjs(f):
    fo = [0]
    for i, a in enumerate(f):
        if a > 0: fo.append(i)
    return fo

# for f in Floors[1:] :
    # print(f, " --> ", getFloorObjs(f))
    # for a, b in combinations(getFloorObjs(f), 2):
        # print(a,b)
# exit(1)

##
## Only move 1 floor at a time
##
def setStates(s):
    retStates = []
    current_floor = s[CUR_FLOOR]
    for destination_floor in [current_floor - 1, current_floor + 1]:
        if destination_floor < 1 or destination_floor > 4: continue                    
        for obj1, obj2 in combinations(getFloorObjs(s[current_floor]), 2):
            good, ns = getState(s, destination_floor, obj1, obj2)
            if good:
                retStates.append(ns)
                    
    return retStates

def pState(s):
    print("Step: ", s[STEPS])
    for i in range(4, 0, -1):
        print("F%1d " % i, end = "")
        if i == s[CUR_FLOOR]: print("E ", end="")
        else:  print(". ", end="")
        for obj in s[i]:
            print("%2d " % obj, end = "")
        print()
    print()

def hashState(f):
    hs = str(f[CUR_FLOOR])
    for floor in range(1,5):
        for i, d in enumerate(f[floor]):
            if (i == 0): hs += '|'
            elif d == 0: hs += '.'
            else:
                # hs += str(i)
                if i % 2 == 0: 
                    hs += chr(ord('a') + i//2 - 1)
                else: 
                    hs += chr(ord('A') + i//2)
    return hs

first = setStates(Floors)   # initial set of moves
#print(first)
mem = {}
if USE_DEQUE:
    states = deque()
    for f in first:
        states.append(f)
else:
    states = []
    for f in first:
        states.append(f)
#for f in first:
    #LIST#states.append(f)
    #states.append(f)
count = 0
while states:
    count += 1
    if USE_DEQUE:
        f = states.popleft()
    else:
        f = states.pop()
    # pState(f)
    if f[STEPS] > maxSteps : maxSteps = f[STEPS]
    if sum(f[4]) == NumObjs:
        if (DEBUG) : print("minSteps: ", minSteps)
        if f[STEPS] < minSteps:
            minSteps = f[STEPS]
            if (DEBUG) : print(h, "  ********* Steps: ", f[STEPS], "  Total: ", f[CUR_FLOOR])
    else:
        add_states = setStates(f)
        for f in add_states:
            h = hashState(f)
            if not h in mem:
                mem[h] = f[STEPS]
                if (DEBUG) : print(h, "  Steps: ", f[STEPS], "  Elevator: ", f[CUR_FLOOR])
                states.append(f)
            else:
                if mem[h] > f[STEPS]:
                    mem[h] = f[STEPS]
                    states.append(f)
                    if (DEBUG) : print(h, "  Steps: ", f[STEPS], "  Elevator: ", f[CUR_FLOOR])
    if count % 1000 == 0: print(count, maxSteps, len(states))
print("Part 1: minimum steps required: ", minSteps)
                    
