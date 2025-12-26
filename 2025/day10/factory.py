import copy
from collections import deque
import pulp
import numpy as np

"""
Find the non-negative integer vector s with minimal sum such that A s = t.

Parameters:
- A: N x M matrix (list of lists) of 0s and 1s (N rows, M columns)
- t: N-element list of integers

Returns:
- List of integers representing s if a solution exists
- None if no feasible solution
"""
def find_min_sum_s(A, t):

    N = len(A)
    if N == 0:
        return [] if not t else None
    M = len(A[0])
    
    # Basic dimension checks
    if len(t) != N:
        print("t must have length: ", N, " but has length", len(t))
        exit(1)
    if any(len(row) != M for row in A):
        raise ValueError("All rows in A must have the same length M")
    
    # Create the ILP problem
    prob = pulp.LpProblem("Minimal_Sum_NonNegative_Integer_Solution", pulp.LpMinimize)
    
    # Variables: s_j >= 0, integer
    s = [pulp.LpVariable(f"s{j}", lowBound=0, cat=pulp.LpInteger) for j in range(M)]
    
    # Objective: minimize the sum of s
    prob += pulp.lpSum(s), "Total_Sum"
    
    # Constraints: each row of A dotted with s equals the corresponding entry in t
    for i in range(N):
        prob += pulp.lpSum(A[i][j] * s[j] for j in range(M)) == t[i], f"Equation_{i}"
    
    # Solve using the default solver (CBC is included with PuLP)
    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))  # msg=False suppresses solver log
    
    # Check result
    if status != pulp.LpStatusOptimal:
        return None  # Infeasible or unbounded (though unbounded shouldn't happen here)
    
    # Extract the solution
    solution = [int(pulp.value(var)) for var in s]  # Convert to int for cleaner output
    
    return solution



def min_presses(target, buttons):
    """
    target:  tuple[int]       e.g. (3,5,4,7)
    buttons: list[tuple[int]] e.g. [(0,0,0,1), (0,1,0,1), ...]

    Returns minimum number of presses to reach target exactly.
    """
    A = np.zeros([len(target),len(buttons)], dtype = int)
    for i in range(len(target)):
        for j in range(len(buttons)):
            A[i,j] = buttons[j][i]

    # for a in A:
        # print(a)
    # print(target)
    return find_min_sum_s(A, target)




p2s = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192]
def cnt2(n):
    cnt = []
    for i, p in enumerate(p2s):
        if n & p: 
            #print(n,p)
            cnt.append(i)
    return cnt


    
def twos():
    p=[]
    for i in range(15):
        p.append([])
    for n in range(1, 2**13):
        p2f = cnt2(n)
        c = len(p2f)
        p[c].append(p2f)
    #print(p)
    return p
        
def ostr(l, n):
    #print('[', end = "")
    s = ""
    for i in range(n):
        if l & 1: s = s + '#'
        else: s = s + '.'
        l //= 2
    #print(']', end = "")
    return s

        
class lights:
    def __init__(self, final):
        self.state = 0
        self.final = 0
        self.num_lights = len(final)-2
        self.larray = [0] * self.num_lights
        p2 = 1
        n = 0
        for a in final:
            if a != '.' and a != '#': continue
            if a == '#': 
                self.final += p2
                self.larray[n] = 1
            n += 1
            p2 *= 2
    def reset(self):
        self.state = 0
    def apply(self, s):
        self.state ^= s
        if self.state == self.final: return True
        return False
    def copy(self, arr):
        arr[0] = 0
        for i in range(self.num_lights):
            arr[i+1] = self.larray[i]
        
    def out(self):
        print("Light - state: ", ostr(self.state, self.num_lights), "  desired: ", ostr(self.final, self.num_lights), "  Good: ", self.final == self.state)
        

class button:
    def __init__(self, blist, sz, num):
        #print(blist)
        b = blist.replace('(','')
        b = b.replace(')','')
        n = b.split(',')
        self.actions = 0
        self.vector=[0]*sz
        self.id = num
        #print(b)
        for a in n:
            i = int(a)
            self.actions += 2 ** i
            self.vector[i] = 1
    # def apply(self, light):
        # return light.apply(self.actions)
    def update(self, arr):
        arr[0] += 1
        for i, k in enumerate(self.vector):
            arr[1][i] -= k
        arr[2][self.id]+=1
        

    def out(self):
        print("Button: ", self.vector)


class jolts:
    def __init__(self, js, nl):
        self.j = [0]*nl   # one joltage per light
        b = js.replace('{','')
        b = b.replace('}','')
        n = b.split(',')
        self.nl = nl   # nl == len(self.j)
        for i, a in enumerate(n):
            self.j[i] = int(a)
        if self.nl != len(self.j):
            print("JOLTAGE ERROR", n, self.nl,  len(self.j))
            exit(1)

#    def add(self, b):
#        self.joltage += b.vector()
        
    def cvec(self, numbuttons):
        s = [0,[],[0]*numbuttons]
        s[1] = copy.deepcopy(self.j)
        return s
        
    def out(self):
        print("Joltages: ", self.j)

def minbutton(buttons, light, p2):
    num_buttons = len(buttons)
    max_num = 2**num_buttons - 1
    #print("num: ", num_buttons, "   max: ", max_num)
#        for b in buttons:
    for i in range(1, num_buttons+1):
        for n in p2[i]:
            #print(i, n)
            #if n > max_num: continue
            light.reset()
            for k in n:
                if k >= num_buttons: break
                if light.apply(buttons[k].actions):
                    return i
                #light.out()
    return -1

#
# [cnt, b1, b2, ..., bn]
# 
minc = 0
runs = 0

buts=[]
jolt=[]
bmin=[]

        
def init(fname):
    global runs, buts, jolt
    p2 = twos()
    
    part1 = 0
    part2 = 0
    for l in open(fname):
        #print(l)
        buttons=[]
        bc = 0
        buts.clear()
        #jolt.clear()
        strs = l.strip().split()
        bcnt=[0]*15
        for s in strs:
            if s[0] == '[':
                light=lights(s)
            if s[0] == '(':
                b = button(s, light.num_lights, bc)
                buts.append(b)
                buttons.append(tuple(v for v in b.vector))
                for i  in range(len(b.vector)):
                    bcnt[i] += b.vector[i]
                bc += 1
            if s[0] == '{':
                jolt = jolts(s, light.num_lights)
                target = tuple(jolt.j[i] for i in range(len(jolt.j)))
        nb = minbutton(buts, light, p2)
        #print(j.out(), bcnt)
        part1 += nb
        # part 2 - find min button pushes
        # initialize final array
        mpv = min_presses(target, buttons)
        mp = sum(mpv)
        part2 += mp
        #print("Solution: ", mp, part2, flush=True)
        #print(target, buttons)
        #print("--------------------------------------------")
        
        

    print("Part 1: ", part1)
    print("Part 2: ", part2)


    

init('data.txt')
# Part 1 - 506 is too high
# Part 1 - 502 is correct
# Part 2 - 21467 is correct
