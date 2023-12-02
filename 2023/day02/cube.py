
def process(line):
# Game 6: 5 blue, 2 green; 6 red, 3 green; 4 green, 4 blue, 2 red; 14 blue, 2 red
	w = line.split()
	num = 1
	idx = int(w[1][:len(w[1])-1])
	for i in range(len(w)):
		if i < 2: continue
		if i % 2 == 0: num = int(w[i])
		if i % 2 == 1: 
			color = w[i]
			#print(num, color)
			if color[:4] == "blue" and num > 14: return -idx
			if color[:5] == "green" and num > 13: return -idx
			if color[:3] == "red" and num > 12: return -idx
	return idx


def process2(line):
# Game 6: 5 blue, 2 green; 6 red, 3 green; 4 green, 4 blue, 2 red; 14 blue, 2 red
	w = line.split()
	num = 1
	greennum = bluenum = rednum = 0
	idx = int(w[1][:len(w[1])-1])
	for i in range(len(w)):
		if i < 2: continue
		if i % 2 == 0: num = int(w[i])
		if i % 2 == 1: 
			color = w[i]
			#print(num, color)
			if color[:4] == "blue" and num > bluenum: bluenum = num
			if color[:5] == "green" and num > greennum: greennum = num
			if color[:3] == "red" and num > rednum: rednum = num
	return rednum * bluenum * greennum

s = 0
for line in open("data.txt", "r"):
	n = process(line)
	#print (line, n)
	if n > 0: s += n

print("Part 1: sum of games is: ", s)

s = 0
for line in open("data.txt", "r"):
	n = process2(line)
	#print (line, n)
	s += n

print("Part 2: sum of power games is: ", s)
