
floor = 0
position = 0
neg1position = 0
for line in open("data.txt"):
	for p in line:
		if p == '(': 
			position += 1
			floor += 1
		if p == ')': 
			position += 1
			floor -= 1
		if floor == -1 and neg1position == 0: 
			neg1position = position

print("Part 1::  final floor is", floor)

print("Part 2::  -1 floor occured at position", neg1position)
