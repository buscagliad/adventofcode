weights = [1,3,5,11,13,17,19,23,29,31,37,41,43,47,53,59,67,71,73,79,83,89,97,101,103,107,109,113]
lw = len(weights)
avg = sum(weights)//3

## Need at least 6 selections, as the sum has to be even, as 4 will not add up to 508


def quan(avg, part2 = False):
    prod = 1000000000000
    for i1 in range(lw-1,-1,-1):
        s1 = weights[i1]
        p1 = weights[i1]
        for i2 in range(i1-1,-1,-1):
            s2 = s1 + weights[i2]
            p2 = p1 * weights[i2]
            for i3 in range(i2-1,-1,-1):
                s3 = s2 + weights[i3]
                p3 = p2 * weights[i3]
                for i4 in range(i3-1,-1,-1):
                    s4 = s3 + weights[i4]
                    p4 = p3 * weights[i4]
                    for i5 in range(i4-1,-1,-1):
                        s5 = s4 + weights[i5]
                        p5 = p4 * weights[i5]
                        if (part2):
                            if s5 < avg: break
                            if s5 == avg:
                               if p5 < prod:
                                    prod = p5
                        for i6 in range(i5-1,-1,-1):
                            s6 = s5 + weights[i6]
                            if s6 < avg: break
                            p6 = p5 * weights[i6]
                            if s6 == avg:
                                if p6 < prod:
                                    prod = p6
    return prod
                        
print("Part 1: Quantum entanglement is ", quan(sum(weights)//3))
                        
print("Part 2: Quantum entanglement is ", quan(sum(weights)//4, True))
