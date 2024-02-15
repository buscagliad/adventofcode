import copy
from itertools import combinations
import numpy as np

# The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
# The second floor contains a hydrogen generator.
# The third floor contains a lithium generator.
# The fourth floor contains nothing relevant.
TEST = True
if TEST:
    HydGen  =  1
    HydChip =  2
    LitGen  =  3
    LitChip =  4
    Gens = [HydGen, LitGen]
    Chips = [HydChip, LitChip]
    minSteps = 100000000000000000
    NumObjs = len(Gens) + len(Chips)
    Floors = np.zeros([5,11], dtype=int)
    Floors[0][1] = 1
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
    minSteps = 100000000000000000
    NumObjs = 10

    Floors = np.zero([5,11], dtype=int)
    Floors[0][1] = 1
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


def compatible(obj1, obj2): # two objects are compatible if they are both generators, both chips, or if they 'balance each other'
    if obj2 == None or obj1 == None: return True
    if obj1 == obj2 : return True
    if obj1 % 2 == 0 and obj2 % 2 == 0: return True
    if obj1 % 2 == 1 and obj2 % 2 == 1: return True
    if abs(obj1 - obj2) == 1 and (obj1 + obj2) % 4 == 3: return True
    return False

# for g in Gens:
    # for c in Chips:
        # print(g, " with ", c, " --> ", compatible(g, c))

# print(Floors)
# Floors = [ [0, 1, 0, 0, 0], # steps, current floor, destination floor, elev_obj1, elev_obj2

def goodFloor(f, obj1, obj2):
    for obj in f:
        if obj == 0: continue
        if not compatible(obj, obj1): return False
        if not obj2 == None:
            if not compatible(obj, obj2): return False
    return True

def getState(s, destination_floor, obj1, obj2):
    if not goodFloor(s[destination_floor], obj1, obj2): return False, None # if either obj1 or obj2 is not compatible - return False, None
    stepCount = s[0][0] + abs(destination_floor - s[0][1])
    if stepCount > minSteps: return False, None # if steps exceeded - return False, None
    #
    # at this point - we have a valid floor move
    # create a copy of the state and update parameters
    #
    ns = copy.deepcopy(s)
    ns[0][0] = stepCount
    current_floor = ns[0][1]
    ns[current_floor][obj1] = 0
    ns[0][1] = destination_floor    # set current floor to destination floor
    ns[destination_floor][obj1] = 1
    if not obj2 == None:
        ns[current_floor][obj2] = 0
        ns[destination_floor][obj2] = 1
    return True, ns

def getFloorObjs(f):
    fo = []
    for i, a in enumerate(f):
        if a > 0: fo.append(i)
    return fo

def setStates(s):
    retStates = []
    current_floor = s[0][1]
    for obj1 in getFloorObjs(s[current_floor]):
        for destination_floor in range(current_floor - 1, 0, -1):  # going down
            good, ns = getState(s, destination_floor, obj1, None)
            if good:
                retStates.append(ns)
            else:
                break   # if not a good floor, fail
                
        for destination_floor in range(current_floor + 1, 5):  # going up
            good, ns = getState(s, destination_floor, obj1, None)
            if good:
                retStates.append(ns)
            else:
                break   # if not a good floor, fail

    for obj1, obj2 in combinations(getFloorObjs(s[current_floor]), 2):
        for destination_floor in range(current_floor - 1, 0, -1):  # going down
            good, ns = getState(s, destination_floor, obj1, obj2)
            if good:
                retStates.append(ns)
            else:
                break   # if not a good floor, fail
                
        for destination_floor in range(current_floor + 1, 5):  # going up
            good, ns = getState(s, destination_floor, obj1, obj2)
            if good:
                retStates.append(ns)
            else:
                break   # if not a good floor, fail

    return retStates

def pState(s):
    print("Step: ", s[0][0])
    for i in range(4, 0, -1):
        print("F%1d " % i, end = "")
        if i == s[0][1]: print("E ", end="")
        else:  print(". ", end="")
        for obj in s[i]:
            print("%2d " % obj, end = "")
        print()
    print()

def hashState(f):
    hs = ""
    for floor in range(1,5):
        for d in f[floor]:
            if d == 0: hs += '0'
            else: hs += '1'
    return hs

first = setStates(Floors)   # initial set of moves
#print(first)
states = []
mem = {}
for f in first:
    # print(f[0])
    # print(f[1])
    # print(f[2])
    # print(f[3])
    # print(f[4])
    states.append(f)
#print (states)
count = 0
while states:
    count += 1
    f = states.pop()
    # pState(f)
    if sum(f[4]) == NumObjs:
        print("minSteps: ", minSteps)
        if f[0][0] < minSteps:
            minSteps = f[0][0]
            print(h, "  Steps: ", f[0][0], "  Total: ", sum(sum(f[1:])))
    else:
        add_states = setStates(f)
        for f in add_states:
            h = hashState(f)
            #print(h, "  Steps: ", f[0][0], "  Total: ", sum(sum(f[1:])))
            if not h in mem:
                mem[h] = f[0][0]
                states.append(f)
            else:
                if mem[h] > f[0][0]:
                    mem[h] = f[0][0]
                    states.append(f)
    #print(len(states))
print(minSteps)
                    
