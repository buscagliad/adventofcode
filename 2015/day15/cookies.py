#Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
from operator import add
import numpy as np


ingredient=[]
ingredient.append(np.array([3, 0, 0, -3, 2]))
ingredient.append(np.array([-3,  3,  0,  0,  9]))
ingredient.append(np.array([-1,  0,  4,  0,  1]))
ingredient.append(np.array([0,  0,  -2,  2,  8]))

#Butterscotch: 
#ingredient.append(np.array([ -1,  -2,  6,  3,  8]))
#Cinnamon: 
#ingredient.append(np.array([ 2,  3,  -2,  -1,  3]))

def score(a, b, c, d):
	global ingredient
	rt = -1
	sc = a*ingredient[0] + b*ingredient[1] + c*ingredient[2] + d*ingredient[3]
	for s in sc: 
		if s < 0: rt = 0
	if rt == -1: rt = sc[0]*sc[1]*sc[2]*sc[3]
	#print (a, b, c, d, sc, rt)
	return rt

maxs = 0
maxi = [0,0,0,0]
p2max = 0
p2maxi = [0,0,0,0]

for a in range(101):
	for b in range(101-a):
		for c in range(101-a-b):
			x = score(a,b,c,100-a-b-c)
			if (6*a - b + 7*c) == 300:
				if x > p2max:
					p2max = x
					p2maxi = [a, b, c, 100-a-b-c]
			if x > maxs: 
				maxs = x
				maxi = [a, b, c, 100-a-b-c]

print("Part 1:  ratios: ", maxi, " Score is ", maxs)	
	
print("Part 2:  ratios: ", p2maxi, " Score is ", p2max)	
