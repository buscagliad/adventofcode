'''

--- Day 18: Duet ---

You discover a tablet containing some strange assembly code labeled simply "Duet". Rather than bother the sound card with it, you decide to run the code yourself. Unfortunately, you don't see any documentation, so you're left to figure out what the instructions mean on your own.

It seems like the assembly is meant to operate on a set of registers that are each named with a single letter and that can each hold a single integer. You suppose each register should start with a value of 0.

There aren't that many instructions, so it shouldn't be hard to figure out what they do. Here's what you determine:

    snd X plays a sound with a frequency equal to the value of X.
    set X Y sets register X to the value of Y.
    add X Y increases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
    rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
    jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

Many of the instructions can take either a register (a single letter) or a number. The value of a register is the integer it contains; the value of a number is that number.

After each jump instruction, the program continues with the instruction to which the jump jumped. After any other instruction, the program continues with the next instruction. Continuing (or jumping) off either end of the program terminates it.

For example:

set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2

    The first four instructions set a to 1, add 2 to it, square it, and then set it to itself modulo 5, resulting in a value of 4.
    Then, a sound with frequency 4 (the value of a) is played.
    After that, a is set to 0, causing the subsequent rcv and jgz instructions to both be skipped (rcv because a is 0, and jgz because a is not greater than 0).
    Finally, a is set to 1, causing the next jgz instruction to activate, jumping back two instructions to another jump, which jumps again to the rcv, which ultimately triggers the recover operation.

At the time the recover operation is executed, the frequency of the last sound played is 4.

What is the value of the recovered frequency (the value of the most recently played sound) the first time a rcv instruction is executed with a non-zero value?

Your puzzle answer was 9423.
--- Part Two ---

As you congratulate yourself for a job well done, you notice that the documentation has been on the back of the tablet this entire time. While you actually got most of the instructions correct, there are a few key differences. This assembly code isn't about sound at all - it's meant to be run twice at the same time.

Each running copy of the program has its own set of registers and follows the code independently - in fact, the programs don't even necessarily run at the same speed. To coordinate, they use the send (snd) and receive (rcv) instructions:

    snd X sends the value of X to the other program. These values wait in a queue until that program is ready to receive them. Each program has its own message queue, so a program can never receive a message it sent.
    rcv X receives the next value and stores it in register X. If no values are in the queue, the program waits for a value to be sent to it. Programs do not continue to the next instruction until they have received a value. Values are received in the order they are sent.

Each program also has its own program ID (one 0 and the other 1); the register p should begin with this value.

For example:

snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d

Both programs begin by sending three values to the other. Program 0 sends 1, 2, 0; program 1 sends 1, 2, 1. Then, each program receives a value (both 1) and stores it in a, receives another value (both 2) and stores it in b, and then each receives the program ID of the other program (program 0 receives 1; program 1 receives 0) and stores it in c. Each program now sees a different value in its own copy of register c.

Finally, both programs try to rcv a fourth time, but no data is waiting for either of them, and they reach a deadlock. When this happens, both programs terminate.

It should be noted that it would be equally valid for the programs to run at different speeds; for example, program 0 might have sent all three values and then stopped at the first rcv before program 1 executed even its first instruction.

Once both of your programs have terminated (regardless of what caused them to do so), how many times did program 1 send a value?

Your puzzle answer was 7620.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

import math

LOWER_CASE_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class Duet:
    def __init__(self, fname, inst):
        self.pgm = []
        self.reg = {}
        self.load(fname)
        self.pc = 0
        self.last_freq = []
        self.name = inst
        self.reg['p'] = inst
        self.num_sends = 0
        self.num_recvs = 0
        self.debug = False
    
    def process(self, line):
        w = line.strip().split()
        if (len(line) < 3): return
        _ins = w[0]
        _reg = w[1]
        if len(w) == 3:
            pline = [_ins, _reg, w[2]]
        else:
            pline = [_ins, _reg]
            
        #print(pline)
        self.pgm.append(pline)

    def load(self, fname):
        for a in LOWER_CASE_ALPHABET:
            self.reg[a] = 0

        for line in open(fname, 'r'):
            self.process(line)
        

    def getval(self, s):
        if s in LOWER_CASE_ALPHABET:
            return self.reg[s]
        return int(s)

    #
    # returns state
    #   state  0 - executed next step
    #         -2 - recv encountered
    #         -3 - end of program
    #
    def run(self, recv_list):
        if self.pc >= len(self.pgm) : return -3
        ins = self.pgm[self.pc][0]
        from_reg = self.pgm[self.pc][1]
        val = 0
        if self.debug: print("PGM", self.name, "  PC: ", self.pc, "  INS: ", ins, "  sends: ", 
            self.num_sends, "  rcvs: ", self.num_recvs)
        if len(self.pgm[self.pc]) == 3:
            to_reg = self.pgm[self.pc][2]
                
        match ins:
            case 'snd':
                lf = self.getval(from_reg)
                if self.debug: print("PGM ", self.name, " at PC: ", self.pc, "  snd:: last_freq = ", lf)
                self.pc += 1
                self.last_freq.append(lf)
                self.num_sends += 1
            case 'set':
                self.reg[from_reg] = self.getval(to_reg)
                self.pc += 1
            case 'add':
                self.reg[from_reg] += self.getval(to_reg)
                self.pc += 1
            case 'mul':
                self.reg[from_reg] *= self.getval(to_reg)
                self.pc += 1
            case 'mod':
                self.reg[from_reg] %= self.getval(to_reg)
                self.pc += 1
            case 'rcv':
                if len(recv_list) == 0:
                    return -2
                self.num_recvs += 1
                self.pc += 1
                #if self.getval(from_reg):
                lf = recv_list.pop(0)
                if self.debug: print("PGM ", self.name, " at PC: ", self.pc, "  rcv:: last_freq = ", lf, recv_list)
                self.reg[from_reg] = lf
            case 'jgz':
                if self.getval(from_reg) > 0:
                    self.pc += self.getval(to_reg)
                else:
                    self.pc += 1
        return 0

pgm = Duet('data.txt', 0)


#
# Part 1:
#
rv = pgm.run(0)
p_lf = []

while rv >= 0:
    rv = pgm.run(p_lf)
    if rv == -2:
        print("Part 1: last frequency played is: ", pgm.last_freq.pop())
        break

#
# Part 2:
#
pgm0 = Duet('data.txt', 0)
pgm1 = Duet('data.txt', 1)
p0_lf = []
p1_lf = []

pgm1_sends = 0
done = False
rv0 = rv1 = 0
ranboth = False
count = 0
while True:
    count += 1
    #
    # run prog
    rv1 = 0
    while rv1 == 0:
        rv1 = pgm1.run(pgm0.last_freq)
    #print("PGM1: rv: ", rv1, "  len(lf): ", len(pgm1.last_freq))
    done = ((rv0 == -3) and (rv1 == -3)) or (len(pgm0.last_freq) == 0 and len(pgm1.last_freq) == 0)
    if (ranboth and done): break
    
    rv0 = 0
    while rv0 == 0:
        rv0 = pgm0.run(pgm1.last_freq)
    
    #print("PGM0: rv: ", rv0, "  len(lf): ", len(pgm0.last_freq))
    done = ((rv0 == -3) and (rv1 == -3)) or (len(pgm0.last_freq) == 0 and len(pgm1.last_freq) == 0)
    if (ranboth and done): break
    ranboth = True
    #print("PGM 0: sends: ", pgm0.num_sends, "  recvs: ", pgm0.num_recvs, "  reg 'p' ", pgm0.reg['p'])
    #print("PGM 1: sends: ", pgm1.num_sends, "  recvs: ", pgm1.num_recvs, "  reg 'p' ", pgm1.reg['p'])


print("Part 2: number of times Program 1 sent a value is: ", pgm1.num_sends)

