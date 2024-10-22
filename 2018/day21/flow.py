'''

--- Day 19: Go With The Flow ---

With the Elves well on their way constructing the North Pole base, you turn your attention back to understanding the inner workings of programming the device.

You can't help but notice that the device's opcodes don't contain any flow control like jump instructions. The device's manual goes on to explain:

"In programs where flow control is required, the instruction pointer can be bound to a register so that it can be manipulated directly. This way, setr/seti can function as absolute jumps, addr/addi can function as relative jumps, and other opcodes can cause truly fascinating effects."

This mechanism is achieved through a declaration like #ip 1, which would modify register 1 so that accesses to it let the program indirectly access the instruction pointer itself. To compensate for this kind of binding, there are now six registers (numbered 0 through 5); the five not bound to the instruction pointer behave as normal. Otherwise, the same rules apply as the last time you worked with this device.

When the instruction pointer is bound to a register, its value is written to that register just before each instruction is executed, and the value of that register is written back to the instruction pointer immediately after each instruction finishes execution. Afterward, move to the next instruction by adding one to the instruction pointer, even if the value in the instruction pointer was just updated by an instruction. (Because of this, instructions must effectively set the instruction pointer to the instruction before the one they want executed next.)

The instruction pointer is 0 during the first instruction, 1 during the second, and so on. If the instruction pointer ever causes the device to attempt to load an instruction outside the instructions defined in the program, the program instead immediately halts. The instruction pointer starts at 0.

It turns out that this new information is already proving useful: the CPU in the device is not very powerful, and a background process is occupying most of its time. You dump the background process' declarations and instructions to a file (your puzzle input), making sure to use the names of the opcodes rather than the numbers.

For example, suppose you have the following program:

#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5

When executed, the following instructions are executed. Each line contains the value of the instruction pointer at the time the instruction started, the values of the six registers before executing the instructions (in square brackets), the instruction itself, and the values of the six registers after executing the instruction (also in square brackets).

ip=0 [0, 0, 0, 0, 0, 0] seti 5 0 1 [0, 5, 0, 0, 0, 0]
ip=1 [1, 5, 0, 0, 0, 0] seti 6 0 2 [1, 5, 6, 0, 0, 0]
ip=2 [2, 5, 6, 0, 0, 0] addi 0 1 0 [3, 5, 6, 0, 0, 0]
ip=4 [4, 5, 6, 0, 0, 0] setr 1 0 0 [5, 5, 6, 0, 0, 0]
ip=6 [6, 5, 6, 0, 0, 0] seti 9 0 5 [6, 5, 6, 0, 0, 9]

In detail, when running this program, the following events occur:

    The first line (#ip 0) indicates that the instruction pointer should be bound to register 0 in this program. This is not an instruction, and so the value of the instruction pointer does not change during the processing of this line.
    The instruction pointer contains 0, and so the first instruction is executed (seti 5 0 1). It updates register 0 to the current instruction pointer value (0), sets register 1 to 5, sets the instruction pointer to the value of register 0 (which has no effect, as the instruction did not modify register 0), and then adds one to the instruction pointer.
    The instruction pointer contains 1, and so the second instruction, seti 6 0 2, is executed. This is very similar to the instruction before it: 6 is stored in register 2, and the instruction pointer is left with the value 2.
    The instruction pointer is 2, which points at the instruction addi 0 1 0. This is like a relative jump: the value of the instruction pointer, 2, is loaded into register 0. Then, addi finds the result of adding the value in register 0 and the value 1, storing the result, 3, back in register 0. Register 0 is then copied back to the instruction pointer, which will cause it to end up 1 larger than it would have otherwise and skip the next instruction (addr 1 2 3) entirely. Finally, 1 is added to the instruction pointer.
    The instruction pointer is 4, so the instruction setr 1 0 0 is run. This is like an absolute jump: it copies the value contained in register 1, 5, into register 0, which causes it to end up in the instruction pointer. The instruction pointer is then incremented, leaving it at 6.
    The instruction pointer is 6, so the instruction seti 9 0 5 stores 9 into register 5. The instruction pointer is incremented, causing it to point outside the program, and so the program ends.

What value is left in register 0 when the background process halts?

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
            print(self.reg[0], end="")
            for i in range(1, len(self.reg)):
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
    global Regs
    oc_text = op.op
    oc = op.opv
    A = op.A
    B = op.B
    C = op.C
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

def run():
    ip = 0
    global ops, Regs
    while ip >=0 and ip < len(ops):
        ip = step(ip)
        if DEBUG: Regs.out(False)
        if ip == 34: return

run()
print("Part 1: register 0 contains the value: ", Regs[0])
Regs.clear()

