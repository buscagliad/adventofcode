def E(T):
    rv = [0, 0]
    rv[0] = (T + 4) % 5
    rv[1] = (T + 1) % 2
    return rv

def D(T):
    rv = [0,0,0,0,0,0]
    rv[0] = (T + 12) % 13
    rv[1] = (T + 2) % 5
    rv[2] = (T + 14) % 17    
    rv[3] = (T + 1) % 3
    rv[4] = T % 7
    rv[5] = (T + 4) % 19
    return rv

SOLN = [0, 0, 0, 0, 0, 0]
MAX = 13*5*17*3*7*19

part1 = False
part2 = False
T = 0
while not part1 or not part2:
    T += 1
    a = D(T)
    if a == SOLN:
        print("Solution: ", T)
        if not part1:
            print("Part 1: time to press the button: ", T) 
            part1 = True
        if (T + 7) % 11 == 0:
            part2 = True
            print("Part 2: time to press the button: ", T)
