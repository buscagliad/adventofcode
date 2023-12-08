
import functools

CARD_P1="23456789TJQKA"
CARD_P2="J23456789TQKA"

CARD=""

def cardcomp(cl, cr):
	global CARD
	il = CARD.index(cl)
	ir = CARD.index(cr)
	if il == ir: return 0
	if il < ir: return 1
	return -1

def pairs(hand, joker = False):
	global CARD
	p1 = 1
	i1 = 0
	c1 = 0
	p2 = 1
	i2 = 0
	c2 = 0
	
	hasJoker = 0
	if joker: hasJoker = hand.count('J')
	
	for i in range(5):
		if joker and hand[i] == 'J' : continue
		p = hand.count(hand[i])
		#print (i, p, p1, hand[i])
		if p > p1:
			p1 = p
			i1 = i
			c1 = CARD.index(hand[i])
			#print("First Pair found: ", hand[i1], p1)
	for i in range(5):
		if joker and hand[i] == 'J' : continue
		p = hand.count(hand[i])
		if p > 1 and not hand[i] == hand[i1] :
			p2 = p
			i2 = i
			c2 = CARD.index(hand[i])
			#print("Second Pair found: ", hand[i2], p2)
	p1 += hasJoker
	if p1 > 5: p1 = 5
	if p1 == 5: ht = 6
	elif p1 == 4: ht = 5
	elif p1 == 3 and p2 == 2: ht = 4
	elif p1 == 3 and p2 < 2: ht = 3
	elif p1 == 2 and p2 == 2: ht = 2
	elif p1 == 2: ht = 1
	else: ht = 0
	return [p1, c1, i1, p2, c2, i2, ht]


def comphand(h1, h2):
	global CARD
	if h1.type > h2.type : return -1
	elif h1.type < h2.type : return 1
	for i in range(5):
		if h1.rank(i) > h2.rank(i)  : return -1
		if h1.rank(i)  < h2.rank(i)  : return 1


	
HandType = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Full House",
			"Four of a Kind", "Five of a Kind"]


class Hand():
	def __init__(self, line, useJoker = False):
		self.hand = line[:5]
		self.bid = int(line[6:])
		self.p1 = 0
		self.p2 = 0
		#print(self.hand)
		self.p1, self.c1, self.i1, self.p2, self.c2, self.i2, self.type = pairs(self.hand, useJoker)
		#self.hand = sorted(self.hand,key=functools.cmp_to_key(cardcomp))

	def rank(self, i):
		global CARD
		return CARD.index(self.hand[i])
	
	def high(self):
		global CARD
		return CARD.index(self.hand[0])
		
	def out(self):
		global CARD
		global HandType
		#print("Hand: ", self.hand, "  Bid: ", self.bid, 
		#	"Pair 1: ", self.c1, " (", self.p1, ") ",
		#	"Pair 2: ", self.c2, " (", self.p2, ") ",
		#	"   ", HandType[self.type])

def rankHands(joker = False):
	global CARD
	CARD = CARD_P1
	if joker: CARD = CARD_P2
	
	hands=[]		
	for line in open("data.txt", "r"):
		#print (line)
		h = Hand(line, joker)
		hands.append(h)
		#h.out()

	newhands = sorted(hands, key=functools.cmp_to_key(comphand))

	rank = 1
	s = 0
	for n in reversed(newhands):
		n.out()
		s += rank * n.bid
		rank += 1
	return s

print ("Part 1: rank sum of hands with Jacks is: ", rankHands(False))

print("Part 2: rank sum of hands with Joker is: ", rankHands(True))
