# cpy x y copies x (either an integer or the value of a register) into register y.
# inc x increases the value of register x by one.
# dec x decreases the value of register x by one.
# jnz x y jumps to an instruction y away (positive means forward; negative means 
#        backward), but only if x is not zero.


pgm = []

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

for line in open('data.txt', 'r'):
    process(line)

reg = {}

def getval(s):
    if s in ['a','b','c','d']:
        return reg[s]
    return int(s)

def runpgm(pgm, rega, regb, regc, regd):
    global reg
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
        # print(pc, pgm[pc], reg['a'])
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
        if pc >= len(pgm) : done = True

runpgm(pgm, 0, 0, 0, 0)
print ("Part 1: Register a value is: ", getval('a'))

runpgm(pgm, 0, 0, 1, 0)
print ("Part 2: Register a value is: ", getval('a'))

