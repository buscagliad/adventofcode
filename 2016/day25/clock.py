'''
--- Day 25: Clock Signal ---
You open the door and find yourself on the roof. The city sprawls away from you for miles and miles.

There's not much time now - it's already Christmas, but you're nowhere near the North Pole, much too far to deliver these stars to the sleigh in time.

However, maybe the huge antenna up here can offer a solution. After all, the sleigh doesn't need the stars, exactly; it needs the timing data they provide, and you happen to have a massive signal generator right here.

You connect the stars you have to your prototype computer, connect that to the antenna, and begin the transmission.

Nothing happens.

You call the service number printed on the side of the antenna and quickly explain the situation. "I'm not sure what kind of equipment you have connected over there," he says, "but you need a clock signal." You try to explain that this is a signal for a clock.

"No, no, a clock signal - timing information so the antenna computer knows how to read the data you're sending it. An endless, alternating pattern of 0, 1, 0, 1, 0, 1, 0, 1, 0, 1...." He trails off.

You ask if the antenna can handle a clock signal at the frequency you would need to use for the data from the stars. "There's no way it can! The only antenna we've installed capable of that is on top of a top-secret Easter Bunny installation, and you're definitely not-" You hang up the phone.

You've extracted the antenna's clock signal generation assembunny code (your puzzle input); it looks mostly compatible with code you worked on just recently.

This antenna code, being a signal generator, uses one extra instruction:

out x transmits x (either an integer or the value of a register) as the next value for the clock signal.
The code takes a value (via register a) that describes the signal to generate, but you're not sure how it's used. You'll have to find the input to produce the right signal through experimentation.

What is the lowest positive integer that can be used to initialize register a and cause the code to output a clock signal of 0, 1, 0, 1... repeating forever?
'''


import math

debug = False
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
    last_out = 1
    min_count = 10
    ret_val = ""
    out_count = 0
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
        if debug: print(pc+1, pgm[pc], end="")
        if len(pgm[pc]) == 3:
            to_reg = pgm[pc][2]
                
        match ins:
            case 'out':
                this_out = getval(from_reg)
                if (this_out == 1): ret_val += '1'
                elif (this_out == 0): ret_val += '0'
                else: ret_val += 'X'
                out_count += 1
                pc += 1
                # if ( (this_out == 0 and last_out == 1) or
                     # (this_out == 1 and last_out == 0) ) :
                    # last_out = this_out
                    # out_count += 1
                # else:
                    # return False
                if (out_count > min_count):
                    return ret_val
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
        if debug: print(" a: ", reg['a'], " b: ", reg['b'], " c: ", reg['c'], " d: ", reg['d'])
        if pc >= len(pgm) : done = True

# for p in range(7, 10):
    # n = 10 ** p

for n in range(10, 100000):
    tf = runpgm(pgm, n, 0, 0, 0)
    if tf == "01010101010":  
        print ("Part 1: Register a value is: ", n)
        break
    # else:
        # print(n, " ", tf, " Registers:  a: ", getval('a'), "  b: ", getval('b'), "  c: ", getval('c'),"  d: ", getval('d'))
    # print("****************************************************")

