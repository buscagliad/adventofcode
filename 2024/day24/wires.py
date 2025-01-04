'''

--- Day 24: Crossed Wires ---

You and The Historians arrive at the edge of a large grove somewhere in the jungle. After the last incident, the Elves installed a small device that monitors the fruit. While The Historians search the grove, one of them asks if you can take a look at the monitoring device; apparently, it's been malfunctioning recently.

The device seems to be trying to produce a number through some boolean logic gates. Each gate has two inputs and one output. The gates all operate on values that are either true (1) or false (0).

    AND gates output 1 if both inputs are 1; if either input is 0, these gates output 0.
    OR gates output 1 if one or both inputs is 1; if both inputs are 0, these gates output 0.
    XOR gates output 1 if the inputs are different; if the inputs are the same, these gates output 0.

Gates wait until both inputs are received before producing output; wires can carry 0, 1 or no value at all. There are no loops; once a gate has determined its output, the output will not change until the whole system is reset. Each wire is connected to at most one gate output, but can be connected to many gate inputs.

Rather than risk getting shocked while tinkering with the live system, you write down all of the gate connections and initial wire values (your puzzle input) so you can consider them in relative safety. For example:

x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02

Because gates wait for input, some wires need to start with a value (as inputs to the entire system). The first section specifies these values. For example, x00: 1 means that the wire named x00 starts with the value 1 (as if a gate is already outputting that value onto that wire).

The second section lists all of the gates and the wires connected to them. For example, x00 AND y00 -> z00 describes an instance of an AND gate which has wires x00 and y00 connected to its inputs and which will write its output to wire z00.

In this example, simulating these gates eventually causes 0 to appear on wire z00, 0 to appear on wire z01, and 1 to appear on wire z02.

Ultimately, the system is trying to produce a number by combining the bits on all wires starting with z. z00 is the least significant bit, then z01, then z02, and so on.

In this example, the three output bits form the binary number 100 which is equal to the decimal number 4.

Here's a larger example:

x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj

After waiting for values on all wires starting with z, the wires in this system have the following values:

bfw: 1
bqk: 1
djm: 1
ffh: 0
fgs: 1
frj: 1
fst: 1
gnj: 1
hwm: 1
kjc: 0
kpj: 1
kwq: 0
mjb: 1
nrd: 1
ntg: 0
pbm: 1
psh: 1
qhw: 1
rvg: 0
tgd: 0
tnw: 1
vdt: 1
wpb: 0
z00: 0
z01: 0
z02: 0
z03: 1
z04: 0
z05: 1
z06: 1
z07: 1
z08: 1
z09: 1
z10: 1
z11: 0
z12: 0

Combining the bits from all wires starting with z produces the binary number 0011111101000. Converting this number to decimal produces 2024.

Simulate the system of gates and wires. What decimal number does it output on the wires starting with z?

Your puzzle answer was 56729630917616.
--- Part Two ---

After inspecting the monitoring device more closely, you determine that the system you're simulating is trying to add two binary numbers.

Specifically, it is treating the bits on wires starting with x as one binary number, treating the bits on wires starting with y as a second binary number, and then attempting to add those two numbers together. The output of this operation is produced as a binary number on the wires starting with z. (In all three cases, wire 00 is the least significant bit, then 01, then 02, and so on.)

The initial values for the wires in your puzzle input represent just one instance of a pair of numbers that sum to the wrong value. Ultimately, any two binary numbers provided as input should be handled correctly. That is, for any combination of bits on wires starting with x and wires starting with y, the sum of the two numbers those bits represent should be produced as a binary number on the wires starting with z.

For example, if you have an addition system with four x wires, four y wires, and five z wires, you should be able to supply any four-bit number on the x wires, any four-bit number on the y numbers, and eventually find the sum of those two numbers as a five-bit number on the z wires. One of the many ways you could provide numbers to such a system would be to pass 11 on the x wires (1011 in binary) and 13 on the y wires (1101 in binary):

x00: 1
x01: 1
x02: 0
x03: 1
y00: 1
y01: 0
y02: 1
y03: 1

If the system were working correctly, then after all gates are finished processing, you should find 24 (11+13) on the z wires as the five-bit binary number 11000:

z00: 0
z01: 0
z02: 0
z03: 1
z04: 1

Unfortunately, your actual system needs to add numbers with many more bits and therefore has many more wires.

Based on forensic analysis of scuff marks and scratches on the device, you can tell that there are exactly four pairs of gates whose output wires have been swapped. (A gate can only be in at most one such pair; no gate's output was swapped multiple times.)

For example, the system below is supposed to find the bitwise AND of the six-bit number on x00 through x05 and the six-bit number on y00 through y05 and then write the result as a six-bit number on z00 through z05:

x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00

However, in this example, two pairs of gates have had their output wires swapped, causing the system to produce wrong answers. The first pair of gates with swapped outputs is x00 AND y00 -> z05 and x05 AND y05 -> z00; the second pair of gates is x01 AND y01 -> z02 and x02 AND y02 -> z01. Correcting these two swaps results in this system that works as intended for any set of initial values on wires that start with x or y:

x00 AND y00 -> z00
x01 AND y01 -> z01
x02 AND y02 -> z02
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z05

In this example, two pairs of gates have outputs that are involved in a swap. By sorting their output wires' names and joining them with commas, the list of wires involved in swaps is z00,z01,z02,z05.

Of course, your actual system is much more complex than this, and the gates that need their outputs swapped could be anywhere, not just attached to a wire starting with z. If you were to determine that you need to swap output wires aaa with eee, ooo with z99, bbb with ccc, and aoc with z24, your answer would be aaa,aoc,bbb,ccc,eee,ooo,z24,z99.

Your system of gates and wires has four pairs of gates which need their output wires swapped - eight wires in total. Determine which four pairs of gates need their outputs swapped so that your system correctly performs addition; what do you get if you sort the names of the eight wires involved in a swap and then join those names with commas?

Your puzzle answer was bjm,hsw,nvr,skf,wkr,z07,z13,z18.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

OR = 1
AND = 2
XOR = 3

OP = ["ERROR", " | ", " & ", " ^ "]

swaps = {}
values = {}
valops = {} # valops[target] = (val1 op val2)

def process(fn):
    global swaps, values, valops
    valSection = True
    for l in open(fn):
        if len(l) < 3:
            valSection = False
            continue
        if valSection:
            values[l[:3]] = int(l[5])
        else:
            val1 = l[:3]
            if l[4] == 'O':
                op = OR
                n = 7
            elif l[4] == 'X':
                op = XOR
                n = 8
            elif l[4] == 'A':
                op = AND
                n = 8
            else:
                print("ERROR: ", l)
            val2 = l[n:n+3]
            if not val1 in values:
                values[val1] = -1
            if not val2 in values:
                values[val2] = -1
            target = l[n+7:n+10]
            if not target in values:
                values[target] = -1
            if target in swaps:
                #print("TGT changing ", target, " to ", swaps[target])
                target = swaps[target]
            #if val1 in swaps:
                #print("VAL1 changing ", val1, " to ", swaps[val1])
                #val1 = swaps[val1]
            #if val2 in swaps:
                #print("VAL2 changing ", val2, " to ", swaps[val2])
                #val2 = swaps[val2]
            valops[target] = (val1, op, val2)


def dump():
    for v in values:
        if values[v] < 0:
            print("Value ", v, " not defined")
        else:
            print("Value ", v, " = ", values[v])

    for t in valops:
        (v1,op,v2) = valops[t]
        print(v1, OP[op], v2, " -> ", t)


def opval(a, b, op):
    if op == OR: return a | b
    if op == AND: return a & b
    if op == XOR: return a ^ b
    print("ERROR - bad op: ", op)
    exit(1)

def getvalue(v):
    global valops, values
    if not v in values:
        print(v, " not a valid value")
    if values[v] >= 0: return values[v]
    (v1, op, v2) = valops[v]
    values[v] = opval(getvalue(v1), getvalue(v2), op)
    return values[v]


def xyzname(xyz, n):
    if n < 10:
        vstr = xyz +'0'+str(n)
    else:
        vstr = xyz + str(n)
    return vstr

def getresult():
    p2 = 1
    rvalue = 0
    for z in range(63):
        zstr = xyzname('z', z)
        if zstr in values: 
            v = getvalue(zstr)
            rvalue += v * p2
        p2 *= 2
    return rvalue
    

process('data.txt')
print("Part 1: wire output to the Z array is: ", getresult())


def setv(vname, value):
    for i in range(63):
        vstr = xyzname(vname, i)
        values[vstr] = value & 1
        value >>= 1

def setswaps(a, b):
    global swaps
    swaps[a]=b
    swaps[b]=a
    #print("Swapping ", a, " and ", b)

def addem(x, y):
    global values, valops
    values.clear()
    valops.clear()
    process('data.txt')
    setv('x', x)
    setv('y', y)
    return getresult()

#
# find where error occured
#
def findxy(n):
    zstr = xyzname('z', n)
    done = False
    q = [zstr]
    xdone = False
    ydone = False
    while q:
        vstr = q.pop()
        (astr, op, bstr) = valops[vstr]

        if astr[0] == 'x':
            xdone = True
        elif astr[0] == 'y':
            ydone = True
        else:
            q.append(astr)

        if bstr[0] == 'x':
            xdone = True
        elif bstr[0] == 'y':
            ydone = True
        else:
            q.append(bstr)
            
        print(astr, " -- ", values[astr], "  ",
              bstr, " -- ", values[bstr])

def getop(var):
    for vstr, vop in valops.items():
        v1 = vop[0]
        v2 = vop[1]
        if v1 == var or v2 == var: return vstr, vop
    return '   ', ('   ', 1, '   ')
#
# find where error occured
#
def findz(n):
    used = []
    xstr = xyzname('x', n)
    ystr = xyzname('y', n)
    done = False
    q = [xstr, ystr]
    used.append(xstr)
    used.append(ystr)
    while q:
        vstr = q.pop()
        ostr, (v1,op,v2) = getop(vstr)
        used.append(vstr)
        if ostr == '   ': continue
        print(v1, OP[op], v2, " -> ", ostr)
        if ostr[0] != 'z':

            if not ostr in used:
                #used.append(ostr)
                q.append(ostr)
            if not v1 in used:
               # used.append(v1)
                q.append(v1)
            if not v2 in used:
               # used.append(v2)
                q.append(v2)

def swap(a, b):
    global swaps
    swaps[a]=b
    swaps[b]=a
    

x = 0
y = 1
b=[-1]*4
n = 0
'''
NOTE: I used trial and error to determine which of the z digits
7, 13, 18 and 26 needed wires swapped.  I knew these were the
problematic wires by looking at the error computed and noticed
the errors were always a sum of 2^7, 2^13, 2^18 and 2^26
'''
setswaps('bjm', 'z07')
setswaps('z13','hsw')
setswaps('z18','skf')
setswaps('nvr','wkr')
'''
set A, B, C, D, E and F the wire names of the z bit in question
Setting N below will select one of the wire swaps
Coninue to increase N until that bit error is removed

A='z26'
B='nvr'
C='wkr'
D='bpb'
E='frt'
F='frt'
'''

'''
z18
qjc
skf
x26 XOR y26 -> nvr
y26 AND x26 -> wkr
frt OR nvr -> bpb
qkf AND wkr -> frt
qkf XOR wkr -> z26
'''
N = 500
if N == 0: setswaps(A,B)
elif N == 1: setswaps(A,C)
elif N == 2: setswaps(A,D)
elif N == 3: setswaps(A,E)
elif N == 4: setswaps(A,F)
elif N == 5: setswaps(B,C)
elif N == 6: setswaps(B,D)
elif N == 7: setswaps(B,E)
elif N == 8: setswaps(B,C)
elif N == 9: setswaps(C,D)
elif N == 10: setswaps(C,E)
elif N == 11: setswaps(C,F)
elif N == 12: setswaps(D,E)
elif N == 13: setswaps(D,F)
elif N == 14: setswaps(E,F)

def bin2(n):
    b=""
    i = 0
    fb = -1
    k = 0
    while n > 0:
        if n & 1:
            if fb == -1: fb = k
            b += '1'
        else:
            b += '0'
        n //= 2
        k += 1
    return fb, b

maxi = 2**42
import random
for j in range(43): 
    x = random.randint(1, maxi)
    y = random.randint(1, maxi)
    xpy = addem(x,y)
    error = abs(xpy-x-y)
    if (x+y) != xpy: 
        nb, b = bin2(error)
        print(nb, " Z error at: ", j, "  == ", x, " + ", y, " = ", xpy, (x+y)-xpy)

sw = sorted(swaps)
part2=sw[0]
for swa in sw[1:]:
    part2 += ','+swa
    
print("Part 2: swapping the following wires creates an add: ", part2)
