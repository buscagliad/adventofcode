'''
A nice string is one with all of the following properties:

    It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
'''

def numvowels(s):
	vowels = ['a','e','i','o','u']
	cv = 0
	for c in s:
		if c in vowels: cv += 1
	return cv

def numdoubles(s):
	cv = 0
	last_c = ' '
	for c in s:
		if c == last_c: cv += 1
		last_c = c
	return cv

def bad(s):
	bad_pairs = ["ab", "cd", "pq", "xy"]
	for n in range(len(s)-1):
		if s[n:n+2] in bad_pairs: return True
	return False
	
def isnice(s):
	if (bad(s)): return False;
	if numvowels(s) > 2:
		if numdoubles(s) > 0:
			return True
	return False

def dbl_overlap(s):
	for n in range(len(s) - 2):
		pair = s[n:n+2]
		for j in range(n+2, len(s) - 2):
			if pair == s[j:j+2]: return True
	return False

def rep_letter(s):
	for i in range(len(s) - 3):
		if s[i] == s[i+2]: return True
	return False

def isniceP2(s):
	return dbl_overlap(s) and rep_letter(s)
	
	
nice = 0
for line in open("data.txt", "r"):
	if isnice(line) : 
		nice += 1

print("Part 1: there are ", nice, " nice strings")

nice = 0
for line in open("data.txt", "r"):
	if isniceP2(line) : 
		nice += 1

print("Part 2: there are ", nice, " nice strings")
