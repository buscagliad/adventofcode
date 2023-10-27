import copy
import sys

sys.setrecursionlimit(15000)

game_number = 1

class Player:
	def __init__(self, name, pt = True):
		global game_number
		self.cards = []
		self.name = name
		self.empty = True
		self.primary = pt
		self.hashlist = []
		self.game = game_number
		self.round = 0
		
	def add(self, c):
		self.cards.append(c)
		self.empty = False
		
	def next(self):
		if len(self.cards) == 0: return -1
		c = self.cards[0]
		self.last_card = c
		self.cards.remove(c)
		return c
		
	def sample(self):
		if len(self.cards) == 0: return -1
		c = self.cards[0]
		return c

	def hash(self, other):
		s = self.name + str(self.cards) + other.name + str(other.cards)
		tf = s in self.hashlist
		if not tf : self.hashlist.append(s)
		return tf, s
		
	def won(self, c):
		self.cards.append(self.last_card)
		self.cards.append(c)
		
	def display(self):
		print (self.name, " Cards: ", self.cards)
		
	def score(self):
		sc = 0
		numcards = len(self.cards)
		for n in range(numcards):
			multiplier = numcards - n
			# print(n, self.cards[n], " * ", multiplier)
			sc += self.cards[n] * multiplier
		return sc
		
	def subgame (self):
		p = Player(self.name + ".sg", False)
		for n in range(self.last_card):
			p.add(self.cards[n])
		p.game = game_number
		return p
		
		


def playround(p1, p2):
	c1 = p1.sample()
	c2 = p2.sample()
	if c1 < 0 or c2 < 0: return False
	c1 = p1.next()
	c2 = p2.next()

	if (c2 > c1):
		p2.won(c1)
	else:
		p1.won(c2)
	return True

reccount = 0
master_sum = 0

def check(p1, p2):
	global master_sum
	nums = []
	for c in p1.cards:
		nums.append(c)
	for c in p2.cards:
		nums.append(c)
	if sum(nums) == master_sum:
		return True
	return False

def playrecround(p1, p2, deb=False):
	global recmap
	global game_number
	global reccount
	#if not check(p1,p2) and p1.game == 1:
	#	p1.display()
	#	p2.display()
	#	exit(1)
	c1 = p1.sample()
	c2 = p2.sample()
	if c1 < 0 : 
		if deb: print("The winner of game", p1.game, "is player 2")
		return True, 2
	if c2 < 0 : 
		if deb: print("The winner of game", p1.game, "is player 1")
		return True, 1
	p1.round += 1
	p2.round += 1
	if deb: 
		print("\n-- Round:", p1.round, "(Game", p1.game,") --")
		print("player 1's deck: ", p1.cards)
		print("player 2's deck: ", p2.cards)
	reccount += 1
	dup, deckstate = p1.hash(p2)
	if dup:
		# print(reccount, " BOTH repeated")
		return True, 1
	c1 = p1.next()
	c2 = p2.next()
	who = 0
	#print (c1, len(p1.cards), c2, len(p2.cards))
	if (c1 <= len(p1.cards)) and (c2 <= len(p2.cards)):
		if deb:
			print("Player 1 plays: ", c1)
			print("Player 2 plays: ", c2)
			print("Playing a sub-game to determine the winner ...")
		game_number += 1
		p1sg = p1.subgame()
		p2sg = p2.subgame()
		#p1sg.display()
		#p2sg.display()
		done = False
		normalPlay = False
		while not done:
			done, who = playrecround(p1sg, p2sg)
	else:
		normalPlay = True
		if (c2 > c1):
			who = 2
		else:
			who = 1
	if deb and normalPlay:
		print("Player 1 plays: ", c1)
		print("Player 2 plays: ", c2)
	if who == 2:
		if deb: print("Player 2 wins round", p1.round, "of game", p1.game)
		p2.won(c1)
	elif who == 1:
		p1.won(c2)
		if deb: print("Player 1 wins round", p1.round, "of game", p1.game)
	return playrecround(p1, p2)


p1 = Player("Player 1")
p2 = Player("Player 2")

def init(fname):
	player1 = True
	for line in open(fname, "r"):
		if line == "Player 1:\n":
			player1 = True
			continue
		if line == "Player 2:\n":
			player1 = False
			continue
		if line == "\n" : continue
		if player1:
			p1.add(int(line))
		else:
			p2.add(int(line))
	return sum(p1.cards) + sum(p2.cards)

master_sum = init("data.txt")

p2_1 = copy.deepcopy(p1)
p2_2 = copy.deepcopy(p2)
r = 0

while playround(p1, p2):
	r += 1

p1s = p1.score()
p2s = p2.score()
if p1s > 0:
	print("Part 1: Player 1 wins with a score: ", p1s)
else:
	print("Part 1: Player 2 wins with a score: ", p2s)


playrecround(p2_1, p2_2)

p1s = p2_1.score()
p2s = p2_2.score()
if p1s > 0:
	print("Part 2: Player 1 wins with a score: ", p1s)
else:
	print("Part 2: Player 2 wins with a score: ", p2s)
