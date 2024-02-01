
pgm = []

def process(line):
    global pgm
    w = line.strip().split()
    ins = w[0]
    reg = w[1][0]

    if ',' in w[1]:
        jmp = int(w[2])
        pline = [ins, reg, jmp]
    elif ins == 'jmp':
        pline = [ins, 0, int(w[1])]
    else:
        pline = [ins, reg]
        
    #print(pline)
    pgm.append(pline)

for line in open('data.txt', 'r'):
    process(line)


def runpgm(pgm, rega, regb):
    done = False
    pc = 0
    while not done:
        ins = pgm[pc][0]
        reg = pgm[pc][1]
        val = 0
        # print(pc, pgm[pc], rega, regb)
        if len(pgm[pc]) == 3:
            val = pgm[pc][2]
                
        match ins:
            case 'jmp':
                pc += val - 1
            case 'inc':
                if reg == 'a':
                    rega += 1
                elif reg == 'b':
                    regb += 1
                else:
                    print("ERROR - inc - bad reg: ", reg)
                    exit(1)
            case 'tpl':
                if reg == 'a':
                    rega *= 3
                elif reg == 'b':
                    regb *= 3
                else:
                    print("ERROR - tpl - bad reg: ", reg)
                    exit(1)
            case 'hlf':
                if reg == 'a':
                    rega //= 2
                elif reg == 'b':
                    regb //= 2
                else:
                    print("ERROR - hlf - bad reg: ", reg)
                    exit(1)
            case 'jio':
                if reg == 'a':
                    if rega == 1: pc += val - 1
                elif reg == 'b':
                    if regb == 1: pc += val - 1
                else:
                    print("ERROR - jio - bad reg: ", reg)
                    exit(1)
            case 'jie':
                if reg == 'a':
                    if rega % 2 == 0: pc += val - 1
                elif reg == 'b':
                    if regb % 2 == 1: pc += val - 1
                else:
                    print("ERROR - jie - bad reg: ", reg)
                    exit(1)
        pc += 1
        if pc >= len(pgm) : done = True
    return rega, regb

ra, rb = runpgm(pgm, 0, 0)
print ("Part 1: Register b value is: ", rb)

ra, rb = runpgm(pgm, 1, 0)
print ("Part 2: Register b value is: ", rb)
