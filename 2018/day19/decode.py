R=[0,0,0,0,0,0]



def update(R):
    # OP 17:: addi 2 2 2
    R[2] = R[2] + 2
    # OP 18:: mulr 2 2 2
    R[2] = R[2] * R[2]
    # OP 19:: mulr 3 2 2
    R[2] = R[2] * 19
    # OP 20:: muli 2 11 2
    R[2] = 11 * R[2]
    # OP 21:: addi 1 5 1
    R[1] = 5 + R[1]
    # OP 22:: mulr 1 3 1
    R[1] = 22 * R[1]
    # OP 23:: addi 1 8 1
    R[1] = 8 + R[1]
    # OP 24:: addr 2 1 2
    R[2] = R[1] + R[2]
    # OP 25:: addr 3 0 3
    if R[0] == 0: 
        R[3] = 0
        return
    R[3] = R[3] + R[0]
    # OP 26:: seti 0 5 3
    # This returns IP back to 0 - or instruction #1
    # OP 27:: setr 3 9 1
    R[1] = 27
    # OP 28:: mulr 1 3 1
    R[1] = 28 * R[1]
    # OP 29:: addr 3 1 1
    R[1] = 29 + R[1]
    # OP 30:: mulr 3 1 1
    R[1] = 30 * R[1]
    # OP 31:: muli 1 14 1
    R[1] = 14 * R[1]
    # OP 32:: mulr 1 3 1
    R[1] = 32 * R[1]
    # OP 33:: addr 2 1 2
    R[2] = R[2] + R[1]
    # OP 34:: seti 0 9 0
    R[0] = 0
    # OP 35:: seti 0 9 3
    # This returns IP back to 0 - or instruction #1
    R[3] = 0

update(R)
print(R)
#exit(1)
# ip = 3 [1, 10550400, 10551354, 33, 0, 0]
# OP  0:: addi 3 16 3
#Goto 17
Done = False
# OP  1:: seti 1 3 4
R[3] = 0
R[4] = 1

while not Done:
    # OP  2:: seti 1 8 5
    R[5] = 1
    if (R[1]): print(R)
    # OP  3:: mulr 4 5 1
    R[1] = R[5] * R[4]
# OP  4:: eqrr 1 2 1
    if R[1] == R[2]: 
        R[1] = 1
    else:
        R[1] = 0
# OP  5:: addr 1 3 3
    R[3] = R[1] + 4  # current program pointer
# OP  6:: addi 3 1 3
    R[3] = 6
# OP  7:: addr 4 0 0
    if R[1] == 0:
        R[0] = R[4] + R[0]
# OP  8:: addi 5 1 5
    R[5] = R[5] + 1
# OP  9:: gtrr 5 2 1
    if R[5] > R[2]: 
        R[1] = 1 
    else:
        R[1] = 0
# OP 10:: addr 3 1 3
    #R[3] = R[1] + R[3]
# OP 11:: seti 2 6 3
    if R[1] == 0:
        R[3] = 1
        continue
# OP 12:: addi 4 1 4
    R[4] = 1 + R[4]
# OP 13:: gtrr 4 2 1
    if R[4] > R[2]:
        R[1] = 1
    else:
        R[1] = 0
# OP 14:: addr 1 3 3
    R[3] = R[3] + 1
# OP 15:: seti 1 1 3
    R[3] = 1
# OP 16:: mulr 3 3 3
    done = True

# ADDR: R[C] = R[A] + R[B]
# ADDI: R[C] = R[A] + B

# MULR: R[C] = R[A] * R[B]
# MULI: R[C] = R[A] * B

# SETR: R[C] = R[A]
# SETI: R[C] = A

# GTRR: if R[A] > R[B]: R[C] = 1 else: R[C] = 0
# EQRR: if R[A] == R[B]: R[C] = 1 else: R[C] = 0
