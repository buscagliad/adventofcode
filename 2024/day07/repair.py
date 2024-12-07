'''

--- Day 7: Bridge Repair ---

The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't on this side of the bridge, though; maybe he's on the other side?

When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it breaks pretty frequently.) You won't be able to cross until it's fixed.

You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20

Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

    190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
    3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
    292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.

The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly be true. In the above example, the sum of the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?

Your puzzle answer was 8401132154762.
--- Part Two ---

The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:

    156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
    7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
    192: 17 8 14 can be made true using 17 || 8 + 14.

Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?

Your puzzle answer was 95297119227552.

Both parts of this puzzle are complete! They provide two gold stars: **
'''

import numpy as np

def mathit(w, n):
    #print("mathit: ", w, n)
    s = 0
    i = 0
    s = int(w[0])
    for k in range(1,len(w)):
        v = int(w[k])
        if n & 1<<(k-1): s = s * v
        else: s = s + v
    return s
    
def numdigits(v):
    nd = 0;
    while v:
        v = v // 10
        nd += 1
    return nd

def cat(s, v):
    k = numdigits(v)
    return 10**k * s + v

def mathit2(w, n):
    s = 0
    i = 1
    s = int(w[0])
    for k in n:
        v = int(w[i])
        if k == 0: s = s * v
        elif k == 1: s = s + v
        elif k == 2: s = cat(s, v)
        i += 1
    #print("mathit2: ", w, n, s)
    return s
    
def comp_part1(val, w):
    n = 2**(len(w)-1)
    for i in range(0,n):
        if mathit(w, i) == val: return True
    return False


def decomp(k, b, n):
    nv = np.zeros(n, dtype=int)
    for i in range(n):
        nv[i] = k % b
        k = k // b
    return nv

def comp_part2(val, w, b):
    numn = len(w)-1
    n = b**(numn)
    for i in range(0,n):
        nv = decomp(i, b, numn)
        if mathit2(w, nv) == val: return True
    return False
    

def process(line, part2 = False):
    w = line.strip().split(' ')
    val = int(w[0][:len(w[0])-1])
    base = 2
    if part2: base = 3
    if comp_part2(val, w[1:], base):
        #print("GOOD: ", val, w)
        return val
    else:
        #print("BAD: ", val, w)
        return 0

p1 = 0
for l in open('data.txt'):
    p1 += process(l)

print("Part 1: sum of all good calibrations: ", p1)

p2 = 0
for l in open('data.txt'):
    p2 += process(l, True)
print("Part 2: sum of all good calibrations: ", p2)
#print("cat: ", cat(1513, 5163))
