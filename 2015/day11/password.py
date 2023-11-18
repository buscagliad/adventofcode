
bad=[ord('i')-ord('a'), ord('o')-ord('a'), ord('l')-ord('a')]

def haspairs(v):
	c = 0
	skip = False
	for i in range(len(v)-1):
		if skip: 
			skip = False
			continue
		if v[i] == v[i+1] : 
			c += 1
			skip = True
	return c >= 2

def haslst(v):
	c = 0
	mc = 0
	for i in range(len(v)-1):
		if v[i] == v[i+1] + 1 : 
			c += 1
			if c > mc: mc = c
		else:
			c = 0
	return mc >= 2	

def toint(s):
	rv = []
	for a in reversed(s):
		rv.append(ord(a) - ord('a'))
	return rv

def tostr(v):
	rv = ""
	for a in reversed(v):
		rv += chr(a + ord('a'))
	return rv

def inc(v):
	v[0] += 1
	if v[0] in bad: v[0] += 1
	if v[0] > 25:
		v[0] = 0
		v[1] += 1
		if v[1] in bad: 
			v[1] += 1
		else:
			for i in range(1, len(v)):
				if v[i] > 25:
					v[i] = 0
					v[i+1] += 1
					if v[i+1] in bad: 
						v[i+1] += 1
						break
				else:
					break
				
		

'''
    Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
    Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
    Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.


print("convert: ", x)
y = tostr(x)
print("convert: ", y)

t="abbceffg"
print("Has straight", t, " ", haslst(toint(t)))
t="abbcefgg"
print("Has straight", t, " ", haslst(toint(t)))
t="abbceffg"
print("Has double", t, " ", haspairs(toint(t)))
t="ababcedg"
print("Has double", t, " ", haspairs(toint(t)))
t="abbbcedg"
print("Has double", t, " ", haspairs(toint(t)))
'''
x = toint("cqjxjnds")

done = False
while not done:
	inc(x)
	if not haslst(x): continue
	if not haspairs(x): continue
	print("Part 1: Valid password: ", tostr(x))
	done = True
	
done = False
while not done:
	inc(x)
	if not haslst(x): continue
	if not haspairs(x): continue
	print("Part 2: Valid password: ", tostr(x))
	done = True
