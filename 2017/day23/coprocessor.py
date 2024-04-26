'''

--- Day 23: Coprocessor Conflagration ---

You decide to head directly to the CPU and fix the printer from there. As you get close, you find an experimental coprocessor doing so much work that the local programs are afraid it will halt and catch fire. This would cause serious issues for the rest of the computer, so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on that tablet. The general functionality seems very similar, but some of the instructions are different:

    set X Y sets register X to the value of Y.
    sub X Y decreases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

    Only the instructions listed above are used. The eight registers here, named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for testing, but prevents it from doing any meaningful work.

If you run the program (your puzzle input), how many times is the mul instruction invoked?

Your puzzle answer was 3025.
--- Part Two ---

Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the switch, which makes register a now start at 1 when the program is executed.

Immediately, the coprocessor begins to overheat. Whoever wrote this program obviously didn't choose a very efficient implementation. You'll need to optimize the program if it has any hope of completing before Santa needs that printer working.

The coprocessor's ultimate goal is to determine the final value left in register h once the program completes. Technically, if it had that... it wouldn't even need to run the program.

After setting register a to 1, if the program were to run to completion, what value would be left in register h?

Your puzzle answer was 915.

Both parts of this puzzle are complete! They provide two gold stars: **


'''

import math

LOWER_CASE_ALPHABET = "abcdefghijklmnopqrstuvwxyz"

mul_count = 0

class Duet:
    def __init__(self, fname, inst):
        self.pgm = []
        self.reg = {}
        self.load(fname)
        self.pc = 0
        self.name = inst
        self.reg['a'] = inst
        self.num_mults = 0
        self.debug = True
    
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

    def out(self, t):
        print(t, 
            " a: ", self.reg['a'],
            " b: ", self.reg['b'],
            " c: ", self.reg['c'],
            " d: ", self.reg['d'],
            " e: ", self.reg['e'],
            " f: ", self.reg['f'],
            " g: ", self.reg['g'],
            " h: ", self.reg['h'])

    #
    # returns state
    #   state  0 - executed next step
    #         -2 - recv encountered
    #         -3 - end of program
    #
    def run(self):
        global mul_count
        if self.pc >= len(self.pgm) : return -3
        ins = self.pgm[self.pc][0]
        from_reg = self.pgm[self.pc][1]
        val = 0
       
        if len(self.pgm[self.pc]) == 3:
            to_reg = self.pgm[self.pc][2]

        match ins:
            case 'set':
                self.reg[from_reg] = self.getval(to_reg)
                self.pc += 1
            case 'sub':
                self.reg[from_reg] -= self.getval(to_reg)
                self.pc += 1
            case 'add':
                self.reg[from_reg] += self.getval(to_reg)
                self.pc += 1
            case 'mul':
                self.reg[from_reg] *= self.getval(to_reg)
                self.num_mults += 1
                self.pc += 1
            case 'mod':
                self.reg[from_reg] %= self.getval(to_reg)
                self.pc += 1
            case 'jgz':
                if self.getval(from_reg) > 0:
                    self.pc += self.getval(to_reg)
                else:
                    self.pc += 1
            case 'jnz':
                if self.getval(from_reg) != 0:
                    self.pc += self.getval(to_reg)
                else:
                    self.pc += 1
        return 0

pgm1 = Duet('data.txt', 0)


#
# Part 1:
#
def part1():
    rv = pgm1.run()

    while rv >= 0:
        rv = pgm1.run()
        if rv < 0:
            break

    print("Part 1: num mul instructions: ", pgm1.num_mults)

'''
a = 1
b = 0
c = 0
d = 0
e = 0
f = 0
g = 0
h = 0

def out(t):
    global a,b,c,d,e,f,g,h
    print(t, " a: ", a, " b: ", b, " c : ", c, " d: ", d, " e: ", e, " f: ", f, " g: ", g, " h: ", h)

b = 57  # line 1
c = b  # line 2
if a != 0:
    b = 105700
    c = b + 17000


while True:
    f = 1 # line 9
    d = 2 # line 10
    while d != b:
        e = 2 # line 11
        out("A: ")
        while e != b:
            
            print("d: ", d, " e: ", e, " d*e: ", d*e, " b: ", b)
            if (d * e) == b: # line 15
                #out("SETTING f to zero")
                # if is set to 0 if d and e multiply to give you b
                # only case this can't happen is if b is prime
                f = 0 # line 16
            e += 1 # line 17
            # out("B: ")
        out("C: ")
        d += 1 # line 21
    
    out("D: ")
    # if 
    if f == 0: # line 25 only increments h if b is NOT a prime
        h += 1 # line 26
    if b != c:
        break;  # program is done
    b += 17
'''
import math

def is_prime(n):
    """
    Checks if an integer is a prime number.

    Args:
    n: The integer to check.

    Returns:
    True if n is a prime number, False otherwise.
    """

    if n <= 1:
        return False

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True

part1()

c = 122700
h = 0
# c + 1 so b will take on the value c
for b in range(105700, c + 1, 17):
    if  not is_prime(b): h += 1

print("Part 2: final value for h is: ", h)

