'''

--- Day 16: Chronal Classification ---

As you see the Elves defend their hot chocolate successfully, you go back to falling through time. This is going to become a problem.

If you're ever going to return to your own time, you need to understand how this device on your wrist works. You have a little while before you reach your next destination, and with a bit of trial and error, you manage to pull up a programming manual on the device's tiny screen.

According to the manual, the device has four registers (numbered 0 through 3) that can be manipulated by instructions containing one of 16 opcodes. The registers start with the value 0.

Every instruction consists of four values: an opcode, two inputs (named A and B), and an output (named C), in that order. The opcode specifies the behavior of the instruction and how the inputs are interpreted. The output, C, is always treated as a register.

In the opcode descriptions below, if something says "value A", it means to take the number given as A literally. (This is also called an "immediate" value.) If something says "register A", it means to use the number given as A to read from (or write to) the register with that number. So, if the opcode addi adds register A and value B, storing the result in register C, and the instruction addi 0 7 3 is encountered, it would add 7 to the value contained by register 0 and store the sum in register 3, never modifying registers 0, 1, or 2 in the process.

Many opcodes are similar except for how they interpret their arguments. The opcodes fall into seven general categories:

Addition:

    addr (add register) stores into register C the result of adding register A and register B.
    addi (add immediate) stores into register C the result of adding register A and value B.

Multiplication:

    mulr (multiply register) stores into register C the result of multiplying register A and register B.
    muli (multiply immediate) stores into register C the result of multiplying register A and value B.

Bitwise AND:

    banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.

Bitwise OR:

    borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.

Assignment:

    setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    seti (set immediate) stores value A into register C. (Input B is ignored.)

Greater-than testing:

    gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.

Equality testing:

    eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.

Unfortunately, while the manual gives the name of each opcode, it doesn't seem to indicate the number. However, you can monitor the CPU to see the contents of the registers before and after instructions are executed to try to work them out. Each opcode has a number from 0 through 15, but the manual doesn't say which is which. For example, suppose you capture the following sample:

Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

This sample shows the effect of the instruction 9 2 1 2 on the registers. Before the instruction is executed, register 0 has value 3, register 1 has value 2, and registers 2 and 3 have value 1. After the instruction is executed, register 2's value becomes 2.

The instruction itself, 9 2 1 2, means that opcode 9 was executed with A=2, B=1, and C=2. Opcode 9 could be any of the 16 opcodes listed above, but only three of them behave in a way that would cause the result shown in the sample:

    Opcode 9 could be mulr: register 2 (which has a value of 1) times register 1 (which has a value of 2) produces 2, which matches the value stored in the output register, register 2.
    Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1 produces 2, which matches the value stored in the output register, register 2.
    Opcode 9 could be seti: value 2 matches the value stored in the output register, register 2; the number given for B is irrelevant.

None of the other opcodes produce the result captured in the sample. Because of this, the sample above behaves like three opcodes.

You collect many of these samples (the first section of your puzzle input). The manual also includes a small test program (the second section of your puzzle input) - you can ignore it for now.

Ignoring the opcode numbers, how many samples in your puzzle input behave like three or more opcodes?

'''

'''
0000000000111111111
0123456789012345678
Before: [2, 0, 3, 3]
7 2 0 2
After:  [2, 0, 2, 3]
'''
import numpy as np


DEBUG = False
DEBUG1 = False

class RegSet:
    def __init__(self, st):
        self.reg = [int(st[9]), int(st[12]), int(st[15]), int(st[18])]
    def out(self, txt):
        print(txt, self.reg)

class Ops:
    def __init__(self, st):
        oc = st.strip().split()
        self.op = int(oc[0])
        self.A = int(oc[1])
        self.B = int(oc[2])
        self.C = int(oc[3])
    def out(self):
        print(self.op, self.A, self.B, self.C)


class State:
    def __init__(self, line1, line2, line3):
        self.before = RegSet(line1)
        self.after  = RegSet(line3)
        self.ops    = Ops(line2)
    def out(self):
        self.before.out("Before: ")
        self.ops.out()
        self.after.out("After:  ")

states = []
ops = []
line1 = ""
line2 = ""
line3 = ""
n = 0
start = True
for l in open('data.txt'):
    if start:
        if n == 0:
            if len(l) < 4:
                start = False
                continue
            line1 = l
        elif n == 1:
            line2 = l
        elif n == 2:
            line3 = l
        elif n == 3:
            n = -1
            states.append(State(line1, line2, line3))
        n += 1
    else:
        if len(l) < 4: continue
        ops.append(Ops(l))

if DEBUG:
    for s in states:
        s.out()
        
    for o in ops:
        o.out()


Regs = [0, 0, 0, 0]
Maps = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
ADDR = 0
ADDI = 1
MULR = 2
MULI = 3
BANR = 4
BANI = 5
BORR = 6
BORI = 7
SETR = 8
SETI = 9
GTIR = 10
GTRI = 11
GTRR = 12
EQIR = 13
EQRI = 14
EQRR = 15


def doop(oc, A, B, C):
    global Regs, Maps
    if DEBUG: print(opcode, A, B, C, " :: Regs: ", Regs)
        
        
        # Addition:
        # 
        #    addr (add register) stores into register C the result of adding register A and register B.
        #    addi (add immediate) stores into register C the result of adding register A and value B.
    if oc == ADDR:
        Regs[C] = Regs[A] + Regs[B]
        if DEBUG1: print("ADDR: ", Regs[C], " = ", Regs[A], " + ", Regs[B])
    elif oc == ADDI:
        Regs[C] = Regs[A] + B
        if DEBUG1: print("ADDI: ", Regs[C], " = ", Regs[A], " + ", B)


        # Multiplication:
        # 
        #     mulr (multiply register) stores into register C the result of multiplying register A and register B.
        #     muli (multiply immediate) stores into register C the result of multiplying register A and value B.


    elif oc == MULR:
        Regs[C] = Regs[A] * Regs[B]
        if DEBUG1: print("MULR: ", Regs[C], " = ", Regs[A], " * ", Regs[B])
    elif oc == MULI:
        Regs[C] = Regs[A] * B
        if DEBUG1: print("MULI: ", Regs[C], " = ", Regs[A], " * ", B)



        # Bitwise AND:
        # 
        #     banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
        #     bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.


    elif oc == BANR:
        Regs[C] = Regs[A] & Regs[B]
        if DEBUG1: print("BANR: ", Regs[C], " = ", Regs[A], " & ", Regs[B])
    elif oc == BANI:
        Regs[C] = Regs[A] & B
        if DEBUG1: print("BANI: ", Regs[C], " = ", Regs[A], " & ", B)


        # Bitwise OR:
        # 
        #     borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
        #     bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.


    elif oc == BORR:
        Regs[C] = Regs[A] | Regs[B]
        if DEBUG1: print("BORR: ", Regs[C], " = ", Regs[A], " | ", Regs[B])
    elif oc == BORI:
        Regs[C] = Regs[A] | B
        if DEBUG1: print("BORI: ", Regs[C], " = ", Regs[A], " | ", B)


        # Assignment:
        # 
        #     setr (set register) copies the contents of register A into register C. (Input B is ignored.)
        #     seti (set immediate) stores value A into register C. (Input B is ignored.)

    elif oc == SETR:
        Regs[C] = Regs[A]
        if DEBUG1: print("SETR: ", Regs[C], " = ", Regs[A])
    elif oc == SETI:
        Regs[C] = A
        if DEBUG1: print("SETI: ", Regs[C], " = ", A)

        # Greater-than testing:
        # 
        #     gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
        #     gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
        #     gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.

    elif oc == GTIR:
        if A > Regs[B]: Regs[C] = 1
        else: Regs[C] = 0
        if DEBUG1: print("GTIR: ", Regs[C], " = ", A, " > ", Regs[B])
    elif oc == GTRI:
        if Regs[A] > B: Regs[C] = 1
        else: Regs[C] = 0
        if DEBUG1: print("GTRI: ", Regs[C], " = ", Regs[A], " > ", B)
    elif oc == GTRR:
        if Regs[A] > Regs[B]: Regs[C] = 1
        else: Regs[C] = 0
        if DEBUG1: print("GTRR: ", Regs[C], " = ", Regs[A], " > ", Regs[B])

        # Equality testing:
        # 
        #     eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        #     eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        #     eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.


    elif oc == EQIR:
        if A == Regs[B]: Regs[C] = 1
        else: Regs[C] = 0
        if DEBUG1: print("EQIR: ", Regs[C], " = ", A, " == ", Regs[B])
    elif oc == EQRI:
        if Regs[A] == B: Regs[C] = 1
        else: Regs[C] = 0
        if DEBUG1: print("EQRI: ", Regs[C], " = ", Regs[A], " == ", B)
    elif oc == EQRR:
        if Regs[A] == Regs[B]: Regs[C] = 1
        else: Regs[C] = 0
        if DEBUG1: print("EQRR: ", Regs[C], " = ", Regs[A], " == ", Regs[B])
    if DEBUG: print(opcode, A, B, C, " :: Regs: ", Regs)

MAXOP = 16
PosMap = np.zeros([MAXOP,MAXOP], dtype = int)

for i in range(MAXOP):
    for j in range(MAXOP):
        PosMap[i][j] = j

def setregs(rs):
    global Regs
    for i in range(4):
        Regs[i] = rs[i]

def cmpregs(rs):
    global Regs
    for i in range(4):
        if Regs[i] != rs[i] : return False
    return True
    
part1_count = 0
for s in states:
    n = 0
    for opcode in range(MAXOP):
        setregs(s.before.reg)
        if DEBUG: print("Starting registers: ", s.before.reg)
        doop(opcode, s.ops.A, s.ops.B, s.ops.C)
        if not cmpregs(s.after.reg):
            if DEBUG: print("FAIL: ", s.after.reg)
            PosMap[s.ops.op][opcode] = -1
        else:
            n += 1
            if DEBUG: print("SUCCESS: ", s.after.reg)
    if n >= 3: part1_count += 1

print("Part 1: ", part1_count, " examples support 3 or more op codes")

def rowcount(pm, sz, n):
    count = 0
    r = -1
    for i in range(sz):
        if pm[i][n] > -1: 
            count += 1
            r = i
    return (count == 1), r
    
def colcount(pm, sz, n):
    count = 0
    c = -1
    for i in range(sz):
        if pm[n][i] > -1: 
            count += 1
            c = i
    return (count == 1), c

mapc = np.zeros([MAXOP], dtype = int)
mapr = np.zeros([MAXOP], dtype = int)

def findunit():
    global mapc, mapr, PosMap
    done = False
    while not done:
        #done = True
        for i in range(MAXOP):
            row = -1
            col = -1
            found, c = rowcount(PosMap, MAXOP, i)
            if found:
                row = i
                col = c
            else:
                found, r = colcount(PosMap, MAXOP, i)
                if found:
                    row = r
                    col = i
            
            if row > -1:
                mapc[row] = col
                mapr[col] = row
                for j in range(MAXOP):
                    PosMap[j][row] = -1
                    PosMap[col][j] = -1
        if sum(mapc) == 120: done = True
#
# Clean up PosMap
#
Done = False
findunit()
# 623 is too high
setregs([0,0,0,0])
for cmd in ops:
    doop(mapr[cmd.op], cmd.A, cmd.B, cmd.C)
print("Part 2: register 0 contains the value: ", Regs[0])
