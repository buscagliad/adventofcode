

def getNumber(line):
	firstDigit = -1
	lastDigit = 0
	for a in line:
		if a.isdigit():
			if firstDigit < 0:
				firstDigit = int(a)
			lastDigit = int(a)
	return 10 * firstDigit + lastDigit

def isNumber(s):
	if s[0].isdigit(): return int(s[0])
	if s[:3] == "one": return 1
	if s[:3] == "two": return 2
	if s[:5] == "three": return 3
	if s[:4] == "four": return 4
	if s[:4] == "five": return 5
	if s[:3] == "six": return 6
	if s[:5] == "seven": return 7
	if s[:5] == "eight": return 8
	if s[:4] == "nine": return 9
	return -1

def getNumber2(line):
	firstDigit = -1
	lastDigit = 0
	for i in range(len(line)):
		n = isNumber(line[i:])
		if (n < 0):  continue
		if firstDigit < 0:
			firstDigit = n
		lastDigit = n
	return 10 * firstDigit + lastDigit

s = 0
for line in open("data.txt", "r"):
	s += getNumber(line)

print("Part 1: sum is: ", s)

		
s = 0
for line in open("data.txt", "r"):
	s += getNumber2(line)

print("Part 2: sum is: ", s)
