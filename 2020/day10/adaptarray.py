import numpy


def createArray(fname):
    array = [0]
    diff = []
    thisCount = 1
   # thisbag = bag("DONTUSE")
    for line in open(fname, 'r'):
        array.append(int(line))
    array.sort();
    array.append(array[len(array)-1]+3)
    last = 0
    for n in array[1:] :
        diff.append(n - last)
        last = n
    return diff

def inarow(arr, n) :
	ncount = 0
	rcount = 0
	for k in arr:
		if k == 1 : 
			ncount += 1
		else:
			if ncount == n : rcount += 1
			ncount = 0
	return rcount

df = createArray("data.txt")

print("Part 1: 1/3 product: ", df.count(1) * df.count(3))

##
## part 2, for a single 1 in a row, only 1 way to make that 
##         fortwo 1's in a row (..., 3, 1, 1, 3, ...), those numbers
##              can be arranged only 2 ways
##
##         for three 1's in a row (..., 3, 1, 1, 1, 3, ...), those numbers
##              can be arranged 4 ways last number (c) always needs to be in the list, which 
##              yields 4 different ways abc,ac bc, c 
##
##                                     X, a, b, c, d, Y
##         for four 1's in a row (..., 3, 1, 1, 1, 1, 3, ...), those numbers
##              can be arranged 7 ways - d always needs to be in the list,
##              and there are eight arrangements of a,b,c - however, at least
##              one of a,b,c must be present
## There are only caseds of at most 4 1's in a row

print("Part 2:  Adapter permutations: ", (2**inarow(df, 2)) * (4**inarow(df, 3)) * (7**inarow(df, 4)))
				
 
