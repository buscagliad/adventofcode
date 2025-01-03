
'''
--- Day 17: Chronospatial Computer ---

The Historians push the button on their strange device, but this time, you all just feel like you're falling.

"Situation critical", the device announces in a familiar voice. "Bootstrapping process failed. Initializing debugger...."

The small handheld device suddenly unfolds into an entire computer! The Historians look around nervously before one of them tosses it to you.

This seems to be a 3-bit computer: its program is a list of 3-bit numbers (0 through 7), like 0,1,2,3. The computer also has three registers named A, B, and C, but these registers aren't limited to 3 bits and can instead hold any integer.

The computer knows eight instructions, each identified by a 3-bit number (called the instruction's opcode). Each instruction also reads the 3-bit number after it as an input; this is called its operand.

A number called the instruction pointer identifies the position in the program from which the next opcode will be read; it starts at 0, pointing at the first 3-bit number in the program. Except for jump instructions, the instruction pointer increases by 2 after each instruction is processed (to move past the instruction's opcode and its operand). If the computer tries to read an opcode past the end of the program, it instead halts.

So, the program 0,1,2,3 would run the instruction whose opcode is 0 and pass it the operand 1, then run the instruction having opcode 2 and pass it the operand 3, then halt.

There are two types of operands; each instruction specifies the type of its operand. The value of a literal operand is the operand itself. For example, the value of the literal operand 7 is the number 7. The value of a combo operand can be found as follows:

    Combo operands 0 through 3 represent literal values 0 through 3.
    Combo operand 4 represents the value of register A.
    Combo operand 5 represents the value of register B.
    Combo operand 6 represents the value of register C.
    Combo operand 7 is reserved and will not appear in valid programs.

The eight instructions are as follows:

The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.

The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)

The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)

Here are some examples of instruction operation:

    If register C contains 9, the program 2,6 would set register B to 1.
    If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    If register B contains 29, the program 1,7 would set register B to 26.
    If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.

The Historians' strange device has finished initializing its debugger and is displaying some information about the program it is trying to run (your puzzle input). For example:

Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0

Your first task is to determine what the program is trying to output. To do this, initialize the registers to the given values, then run the given program, collecting any output produced by out instructions. (Always join the values produced by out instructions with commas.) After the above program halts, its final output will be 4,6,3,5,6,3,5,2,1,0.

Using the information provided by the debugger, initialize the registers to the given values, then run the program. Once it halts, what do you get if you use commas to join the values it output into a single string?

Your puzzle answer was 2,7,4,7,2,1,7,5,1.
--- Part Two ---

Digging deeper in the device's manual, you discover the problem: this program is supposed to output another copy of the program! Unfortunately, the value in register A seems to have been corrupted. You'll need to find a new value to which you can initialize register A so that the program's output instructions produce an exact copy of the program itself.

For example:

Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0

This program outputs a copy of itself if register A is instead initialized to 117440. (The original initial value of register A, 2024, is ignored.)

What is the lowest positive initial value for register A that causes the program to output a copy of itself?

Your puzzle answer was 37221274271220.

Both parts of this puzzle are complete! They provide two gold stars: **

'''


RA = 0
RA = 0
RB = 0
RC = 0

Program = []
RESULT = []
pc = 0
anyoutput = False

def testA():
    global RA, RB, RC, pc, Program, anyoutput
    #If register C contains 9, the program 2,6 would set register B to 1.
    RC = 9
    RA = 0
    RB = 0
    pc = 0
    Program = [2,6]
    run()
    print()
    print("Expect: RB = 1")
    print("RB ", RB)

    RA = 10
    RB = 0
    RC = 0
    pc = 0
    Program = [5,0,5,1,5,4]
    print("Expect: 0,1,2")
    run()
    print()
    
    # If register B contains 29, the program 1,7 would set register B to 26.
    RB = 29
    RA = 0
    RC = 0
    pc = 0
    Program = [1,7]
    print("Expect:  RB = 26")
    run()
    print("RB: ", RB)
    
    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    RB = 2024
    RC = 43690
    RA = 0
    pc = 0
    Program = [4,0]
    print("Expect:  RB = 44354")
    run()
    print("RB: ", RB)
    
    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    RB = 2024
    RC = 43690
    RA = 0
    pc = 0
    Program = [4,0]
    print("Expect:  RB = 44354")
    run()
    print("RB: ", RB)

def test1():
    global RA, RB, RC, pc, Program, anyoutput
    RA = 729
    RB = 0
    RC = 0

    Program = [0,1,5,4,3,0]
    pc = 0
    anyoutput = False


def part1(regA = 35200350):
    global RA, RB, RC, pc, Program, anyoutput
    RA = regA
    RB = 0
    RC = 0

    print("Part 1: program output: ", end = "")
    Program = [2,4, 1,2, 7,5, 4,7, 1,3, 5,5, 0,3, 3,0]
    pc = 0
    anyoutput = False
    run()
    print()

def part2():
    part1(35200350)
    print()
    #print(Program)
    print(RESULT)
    

def combo(n):
    global RA, RB, RC, pc
    if n <= 3: return n
    if n == 4: return RA
    if n == 5: return RB
    if n == 6: return RC
    print("ERROR - n = ", n, "  pc: ", pc)

def debug():
    global RA, RB, RC, pc, Program, anyoutput
    print("CODE: ", Program[pc], "VAL: ", Program[pc+1], pc, "   Regs: ", RA, RB, RC)
    
def pexec():
    global RA, RB, RC, pc, Program, anyoutput, RESULT
    opcode = Program[pc]
    operand = Program[pc+1]
    pc += 2
    match opcode :
        case 0: # division
            num = RA
            den = 2 ** combo(operand)
            v = RA // den
            #print("Div: ", num, " / ", den, " = ", v)
            RA = v
            #print("case ", opcode, num, " // ", den, RA)
        case 1:
            v = RB ^ operand
            #print("case ", opcode, RB, operand, v)
            RB = v
        case 2:
            RB = combo(operand) % 8
            #print("case ", opcode, combo(operand), RB)
        case 3:
            if RA > 0: # do nothing if RA == 0
                pc = operand
                #print("JUMP to ", pc)
        case 4:
            v = RC ^ RB
            RB = v
        case 5:
            v = combo(operand) % 8
            RESULT.append(v)
            if anyoutput : print(",", end = "")
            print(v, end="")
            anyoutput = True
        case 6:
            v = RA // (2 ** combo(operand))
            RB = v
        case 7:
            v = RA // (2 ** combo(operand))
            RC = v

def run():
    global RA, RB, RC, pc, Program, anyoutput, RESULT
    RESULT.clear()
    pc = 0
    while pc < len(Program):
        pexec()
        # if pc == 12:
            # print(RB, RB%8)

def testX():
    global RA, RB, RC, pc, Program, anyoutput
    # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    RA = 2024
    RB = 0
    RC = 0
    pc = 0
    Program = [0,1,5,4,3,0]
    print("Expect: 4,2,5,6,7,7,7,7,3,1,0   with RA = 0")
    run()
    print()
    print("RA: ", RA)


# Program: 2,4,1,2,7,5,4,7,1,3,5,5,0,3,3,0
def compute(value):
    RA = value
    RB = 0
    RC = 0
    n = 0
    VALS=[]
    while RA > 0:
        RB = RA % 8
        RB = RB ^ 2
        RC = RA // (2 ** RB)
        RB = RB ^ RC
        RB = RB ^ 3
        #print(RA, RB, RC)
        #if n > 0: print(",", end = "")
        n += 1
        #print(RB % 8, end = "")
        VALS.append(RB%8)
        RA = RA // 8
    return VALS

part1()

def runout(v, debug = True):
    comma = False
    res = compute(v)
    for v in res:
        if debug:
            if comma: print(',', end="")
            print(v, end="")
        comma = True
    if debug: print("      length: ", len(res))
    return res


base8=[1, 1,1,1, 1,1,1, 1,1,1, 1,1,1, 1,1,1]
def b8(b):
    s = 0
    p8 = 1
    for v in b:
        s += v * p8
        p8 *= 8
    return s

#print(base8)
#print(b8(base8))
def dodigits(start, n, m, debug):
    global Program
    pn = Program[n]
    pm = Program[m]
    for i in range(8):
        for j in range(8):
            start[n+1] = i
            start[n] = j
            v = b8(start)
            res = runout(v, False)
            if len(res) < m+1: continue
            if res[n] == pn and res[m] == pm:
                if debug: print("returning ", res)
                return res
    
#print()
#part2()
#while pc < len(Program):
#    pexec()
for e in range(14, 0, -2):
    dbg = False
    if e == 0: dbg = True
    res = dodigits(base8, e, e+1, dbg)


base8[0] = base8[1] = 0
nn = b8(base8)
#runout(nn)
for i in range(500):
    newn = nn + i 
    rr = runout(newn, False)
    if rr == Program:
        break
print("Part 2: initial value that replicates program is: ", newn)

