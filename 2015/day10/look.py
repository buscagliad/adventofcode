

import copy

def say(v):
	b = []
	j = v[0]
	c = 1
	for i in v[1:]:
		if (i == j):
			c += 1
		else:
			b.append(c)
			b.append(j)
			c = 1
			j = i
	b.append(c)
	b.append(j)
	
	return b

def runsay(v,n):
	s = v.copy()
	for i in range(n):
		x = say(s)
		s.clear()
		s = x
	return len(x)

s = [1,1,1,3,2,2,2,1,1,3]
print("Part 1 running ", s, " 40 times yields a result or length ", runsay(s, 40))

print("Part 2 running ", s, " 50 times yields a result or length ", runsay(s, 50))
		
