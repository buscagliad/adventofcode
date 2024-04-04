
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

print(cnt)
