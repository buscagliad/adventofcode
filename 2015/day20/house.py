#
# factor(N) - returns list of factors of N
# sumext(N, V) - returns sum of elements of V whose index satisfies: 1 << i & N
# prodext(N, V) - returns product of elements of V whose index satisfies: 1 << i & N
# primefactor(N, full=False) - returns [p, e] list of prime factors and their exponents such that
#     N = sum(p ^ e)
#
import primefac as pf
from itertools import chain, combinations
import numpy as np

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def prime_factors(n):
	factors = []
	for g in pf.primefac(n):
		factors.append(g)
	return factors



def numpresents(N):	# compute number of presents at house N
	g = prime_factors(N)
	s = 0
	p = set()
	for pf in powerset(g):
		#print(pf)
		pc = np.prod(pf)
		if pc <= N: 
			p.add(pc)
			#print(p)
	return int(sum(p)) * 10
	

def numpresents2(N):	# compute number of presents at house N part 2
	s = 0
	for n in range(1, 51):
		if N % n == 0 : s += N/n
	return 11 * s

n = 1
house = 1
MAX_PRESENTS = 29000000
xp = 1

####################### PART 1 ######################
	
for house in range(2*3*4*5*6*7*8*9,2*3*4*5*6*7*8*9*10):
	xp = numpresents(house)
	#print (n, xp)
	if xp > MAX_PRESENTS:
		break

print("Part 1: first house to exceed ", MAX_PRESENTS, " with ", xp, "prestents is house ", house)

####################### PART 2 ######################
for house in range(2*3*4*5*6*7*8*9,2*3*4*5*6*7*8*9*10*11):
	xp = numpresents2(house)
	if xp > MAX_PRESENTS:
		break

print("Part 2: first house to exceed ", MAX_PRESENTS, " with ", xp, "prestents is house ", house)


