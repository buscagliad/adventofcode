'''
--- Day 23: Safe Cracking ---

This is one of the top floors of the nicest tower in EBHQ. The Easter Bunny's private office is here, complete with a safe hidden behind a painting, and who wouldn't hide a star in a safe behind a painting?

The safe has a digital screen and keypad for code entry. A sticky note attached to the safe has a password hint on it: "eggs". The painting is of a large rabbit coloring some eggs. You see 7.

When you go to type the code, though, nothing appears on the display; instead, the keypad comes apart in your hands, apparently having been smashed. Behind it is some kind of socket - one that matches a connector in your prototype computer! You pull apart the smashed keypad and extract the logic circuit, plug it into your computer, and plug your computer into the safe.

Now, you just need to figure out what output the keypad would have sent to the safe. You extract the assembunny code from the logic chip (your puzzle input).

The code looks like it uses almost the same architecture and instruction set that the monorail computer used! You should be able to use the same assembunny interpreter for this as you did there, but with one new instruction:

tgl x toggles the instruction x away (pointing at instructions like jnz does: positive means forward; negative means backward):

    For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
    For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
    The arguments of a toggled instruction are not affected.
    If an attempt is made to toggle an instruction outside the program, nothing happens.
    If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later made to execute that instruction, skip it instead.
    If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a), the resulting instruction is not executed until the next time it is reached.

For example, given this program:

cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a

    cpy 2 a initializes register a to 2.
    The first tgl a toggles an instruction a (2) away from it, which changes the third tgl a into inc a.
    The second tgl a also modifies an instruction 2 away from it, which changes the cpy 1 a into jnz 1 a.
    The fourth line, which is now inc a, increments a to 3.
    Finally, the fifth line, which is now jnz 1 a, jumps a (3) instructions ahead, skipping the dec a instructions.

In this example, the final value in register a is 3.

The rest of the electronics seem to place the keypad entry (the number of eggs, 7) in register a, run the code, and then send the value left in register a to the safe.

What value should be sent to the safe?

Your puzzle answer was 13685.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

The safe doesn't open, but it does make several angry noises to express its frustration.

You're quite sure your logic is working correctly, so the only other thing is... you check the painting again. As it turns out, colored eggs are still eggs. Now you count 12.

As you run the program with this new input, the prototype computer begins to overheat. You wonder what's taking so long, and whether the lack of any instruction more powerful than "add one" has anything to do with it. Don't bunnies usually multiply?

Anyway, what value should actually be sent to the safe?



Your puzzle answer was 479010245.

Both parts of this puzzle are complete! They provide two gold stars: **

'''
# cpy x y copies x (either an integer or the value of a register) into register y.
# inc x increases the value of register x by one.
# dec x decreases the value of register x by one.
# jnz x y jumps to an instruction y away (positive means forward; negative means 
#        backward), but only if x is not zero.

import math

pgm = []
reg = {}

def process(line):
    global pgm
    w = line.strip().split()
    if (len(line) < 3): return
    ins = w[0]
    reg = w[1]
    if len(w) == 3:
        pline = [ins, reg, w[2]]
    else:
        pline = [ins, reg]
        
    #print(pline)
    pgm.append(pline)


def getval(s):
    if s in ['a','b','c','d']:
        return reg[s]
    return int(s)

def runpgm(pgm, rega, regb, regc, regd):
    global reg
    pgm.clear()
    for line in open('data.txt', 'r'):
        process(line)

    done = False
    pc = 0
    reg['a'] = rega
    reg['b'] = regb
    reg['c'] = regc
    reg['d'] = regd
    while not done:
        ins = pgm[pc][0]
        from_reg = pgm[pc][1]
        val = 0
        #print(pc, pgm[pc], " a: ", reg['a'], " b: ", reg['b'], " c: ", reg['c'], " d: ", reg['d'])
        if len(pgm[pc]) == 3:
            to_reg = pgm[pc][2]
                
        match ins:
            case 'cpy':
                reg[to_reg] = getval(from_reg)
                pc += 1
            case 'dec':
                reg[from_reg] -= 1
                pc += 1
            case 'inc':
                reg[from_reg] += 1
                pc += 1
            case 'jnz':
                if not getval(from_reg) == 0:
                    pc += getval(to_reg)
                else:
                    pc += 1
            case 'tgl':
                i = getval(from_reg) + pc
                if i < 0 or i >= len(pgm):
                    pass
                    #print("ERROR - ", i, " is outside prorgram space")
                else:
                    match pgm[i][0]:
                        case 'inc':  
                            pgm[i][0] = 'dec'
                        case 'dec':  
                            pgm[i][0] = 'inc'
                            print(i, " inc ")
                        case 'cpy':  
                            pgm[i][0] = 'jnz'
                        case 'jnz':  
                            pgm[i][0] = 'cpy'
                        case 'tgl':  
                            pgm[i][0] = 'jnz'
                pc += 1
        if pc >= len(pgm) : done = True

runpgm(pgm, 7, 0, 0, 0)
print ("Part 1: Register a value is: ", getval('a'))

#for s in range(7,10):
#    runpgm(pgm, s, 0, 0, 0)
#    print("s: ", s, "  reg a: ", getval('a'))
#
#s:  7   reg a:  13685
#s:  8   reg a:  48965
#s:  9   reg a:  371525
#
# if f(x) = register a value after running: runpgm(pgm, x, 0, 0, 0)
#  we notice that f(7) = 13685  (part 1 answer)  Also: f(7) - 7! = 8645
#                 f(8) = 48965  Also: f(8) - 8! = 8645
#                 f(9) = 371525  Also: f(9) - 9! = 8645
#
# We are concluding that f(x) = 8645 + x! (for x >= 7)
#
print("Part 2: when number of eggs are 12, reg a: ", 8645 + math.factorial(12))

