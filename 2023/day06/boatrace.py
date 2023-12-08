import math

Time=     [   56,     97,     78 ,    75]
Distance=[   546,   1927,   1131,   1139]


def race(t, d):
	ways = 0
	for i in range(t+1):
		speed = i
		remtime = t - i
		dist = speed * remtime
		if dist > d: ways += 1
	return ways

def f(T, D, t):
	return t * (T - t) - D

def p2race(T, D):
	nl = T/2 - math.sqrt(T*T - 4*D) / 2
	nr = T/2 + math.sqrt(T*T - 4*D) / 2
	nl = math.trunc(nl) + 1
	nr = math.trunc(nr)
	return nr - nl + 1

m = 1
for i in range (len(Time)):
	x = race(Time[i], Distance[i])
	m *= x

print("Part 1: race multiplier is: ", m)

print("Part 2: race wins are: ", p2race(56977875, 546192711311139))

