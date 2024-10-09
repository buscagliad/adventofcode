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
R=[1,0,0,0,0,0]
update(R)
print(R)
