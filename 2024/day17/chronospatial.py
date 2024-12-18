

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
            debug()
            v = combo(operand) % 8
            RESULT.append(v)
            #if anyoutput: print(",", end = "")
            #print(v, end = "")
            print("OUT: ", v)
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

RA = 35200350
RB = 0
RC = 0
print("HERE")
print("Part 1: program output: ", end = "")
n = 0
VALS=[]
while RA > 0:
    RB = RA % 8
    RB = RB ^ 2
    RC = RA // (2 ** RB)
    RB = RB ^ RC
    RB = RB ^ 3
    print(RA, RB, RC)
    #if n > 0: print(",", end = "")
    n += 1
    #print(RB % 8, end = "")
    VALS.append(RB%8)
    RA = RA // 8
print(VALS)
print()
            
#part1()
#print()
part2()
#while pc < len(Program):
#    pexec()
        
