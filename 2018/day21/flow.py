'''

--- Day 21: Chronal Conversion ---

You should have been watching where you were going, because as you wander the new North Pole base, you trip and fall into a very deep hole!

Just kidding. You're falling through time again.

If you keep up your current pace, you should have resolved all of the temporal anomalies by the next time the device activates. Since you have very little interest in browsing history in 500-year increments for the rest of your life, you need to find a way to get back to your present time.

After a little research, you discover two important facts about the behavior of the device:

First, you discover that the device is hard-wired to always send you back in time in 500-year increments. Changing this is probably not feasible.

Second, you discover the activation system (your puzzle input) for the time travel module. Currently, it appears to run forever without halting.

If you can cause the activation system to halt at a specific moment, maybe you can make the device send you so far back in time that you cause an integer underflow in time itself and wrap around back to your current time!

The device executes the program as specified in manual section one and manual section two.

Your goal is to figure out how the program works and cause it to halt. You can only control register 0; every other register begins at 0 as usual.

Because time travel is a dangerous activity, the activation system begins with a few instructions which verify that bitwise AND (via bani) does a numeric operation and not an operation as if the inputs were interpreted as strings. If the test fails, it enters an infinite loop re-running the test instead of allowing the program to execute normally. If the test passes, the program continues, and assumes that all other bitwise operations (banr, bori, and borr) also interpret their inputs as numbers. (Clearly, the Elves who wrote this system were worried that someone might introduce a bug while trying to emulate this system with a scripting language.)

What is the lowest non-negative integer value for register 0 that causes the program to halt after executing the fewest instructions? (Executing the same instruction multiple times counts as multiple instructions executed.)

Your puzzle answer was 5745418.
--- Part Two ---

In order to determine the timing window for your underflow exploit, you also need an upper bound:

What is the lowest non-negative integer value for register 0 that causes the program to halt after executing the most instructions? (The program must actually halt; running forever does not count as halting.)

Your puzzle answer was 5090905.

Both parts of this puzzle are complete! They provide two gold stars: **

'''
import numpy as np

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

DEBUG = False
DEBUG1 = False
icount = 0

class RegSet:
    def __init__(self, st):
        self.reg = [0, 0, 0, 0, 0, 0]
        self.ip = 0
        s = st.strip().split()
        self.ip = int(s[1])
    def __getitem__(self, key):
        if key < 0 or key > len(self.reg):
            print("__getitem__ error - ", key)
            return -1
        return self.reg[key]
    def __setitem__(self, key, value):
        if key < 0 or key > len(self.reg):
            print("__setitem__ error - ", key, value)
        self.reg[key] =  value
    def getip(self):
        return self.reg[self.ip]
    def setip(self, ip):
        self.reg[self.ip] = ip
    def get(self, r):
        return self.reg[r]
    def set(self, r, v):
        self.reg[r] = v
    def inc(self, r):
        self.reg[r] += 1
    def clear(self):
        for i in range(len(self.reg)):
            self.reg[i] = 0
    def out(self, full=True):
        if full:
            print("ip =", self.ip, self.reg)
        else:
            print(icount, end="")
            for i in range(len(self.reg)):
                print(",",self.reg[i], end="")
                if (i + 1 == len(self.reg)): print()

class Ops:
    def __init__(self, st):
        # mulr 2 2 2
        oc = st.strip().split()
        self.op = oc[0]
        self.A = int(oc[1])
        self.B = int(oc[2])
        self.C = int(oc[3])
        
        match self.op:
            case "addr":
                self.opv = ADDR
            case "addi":
                self.opv = ADDI
            case "mulr":
                self.opv = MULR
            case "muli":
                self.opv = MULI
            case "banr":
                self.opv = BANR
            case "bani":
                self.opv = BANI
            case "borr":
                self.opv = BORR
            case "bori":
                self.opv = BORI
            case "setr":
                self.opv = SETR
            case "seti":
                self.opv = SETI
            case "gtir":
                self.opv = GTIR
            case "gtri":
                self.opv = GTRI
            case "gtrr":
                self.opv = GTRR
            case "eqir":
                self.opv = EQIR
            case "eqri":
                self.opv = EQRI
            case "eqrr":
                self.opv = EQRR
            case _:
                print("ERROR - unkown value ", self.op)
                exit(1)

    def out(self):
        print(self.op, "(", self.opv, ") :: ", self.A, self.B, self.C)


ops = []

n = 0
start = True

for l in open('data.txt'):
    if start:
        start = False
        Regs = RegSet(l)
    else:
        ops.append(Ops(l))

if DEBUG:

    for o in ops:
        o.out()





def doop(op):
    global Regs, icount
    oc_text = op.op
    oc = op.opv
    A = op.A
    B = op.B
    C = op.C
    icount += 1
    if DEBUG: 
        print(oc_text, A, B, C, " :: Regs: ", end = "")
        Regs.out()
            
        
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


def step (ip):
    global ops, Regs
    """ Function doc """
    #ip = regs.getip()
    Regs.setip(ip)
    doop(ops[ip])
    ip = Regs.getip()
    ip += 1
    return ip
  
#
# Clean up PosMap
#
Done = False
def dumpops():
    for cmd in ops:
        cmd.out()

pairs = []
R4s = []

def run(count = 25999999):
    ip = 0
    
    global ops, Regs
    l = set()
    while ip >=0 and ip < len(ops) and count > 0:
        ip = step(ip)
        if ip == 29:
            R3 = Regs.reg[3]
            R4 = Regs.reg[4]
            #print(R3,R4,flush=True)
            if len(pairs) == 0:
                print("Part 1:  Value that takes least steps to reach: ", R4, flush=True)
            # print(R3, R4)
            addPair = True
            if R4 in R4s:
                addPair = False
            
            R4s.append(R4)
                
            if (R3,R4) in pairs:
                print("Part 2:  Value that takes most steps to reach: ", lastR4, flush=True)
                return
            else:
                if addPair:
                    pairs.append((R3,R4))
                    lastR4 = R4

        if ip == 34: return

run()

