
genA = 679
genB = 771

#genA = 65
#genB = 8921

factorA = 16807
factorB = 48271

modnum = 2147483647

def gnext(last, mult):
    return (last * mult) % modnum

cnt = 0
for i in range(40000000):
    genA = gnext(genA, factorA)
    genB = gnext(genB, factorB)
    if genA & 0xffff == genB & 0xffff: 
        cnt += 1

print("Part 1: number of pairs: ", cnt)

def gnext2(last, mult, div):
    rv = 15
    last = (last * mult) % modnum
    while last & div > 0:
        last = (last * mult) % modnum
    return last

cnt = 0
genA = 679
genB = 771
for i in range(5000000):
    genA = gnext2(genA, factorA, 3)
    genB = gnext2(genB, factorB, 7)
    if genA & 0xffff == genB & 0xffff: 
        cnt += 1
print("Part 2: number of judges pairs: ", cnt)
