'''
Boss:
Hit Points: 109
Damage: 8
Armor: 2

Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3

'''

class Player:
	def __init__(self, name, damage, armor, hits, gold):
		self.name = name
		self.damage = damage
		self.armor = armor
		self.hits = hits
		self.debug = False
		self.gold = gold
	def play(self, attack):
		x = attack.damage - self.armor
		if x <= 0: x = 1
		self.hits -= x
		if (self.debug) : print("The ", attack.name, "deals ", attack.damage, " - ", self.armor, " = ", x, " damage; ",
			"the ", self.name, " goes down to ", self.hits, "points.")
		if (self.hits > 0): return True
		return False

			
# me = Player("player", 5, 5, 8, 0)
# him = Player("boss", 7, 2, 12, 0)
# while (him.play(me) and me.play(him)): pass
# if him.hits > 0:
	# print(him.name, " wins")
# else:
	# print(me.name, " wins")
	
# Hit Points: 109
# Damage: 8
# Armor: 2

him = Player("boss", 8, 2, 109, 0)

weapons=[[8, 4, 0], [10, 5, 0], [25, 6, 0], [40, 7, 0], [72, 8, 0]]

armor_store=[[0, 0, 0], [13, 0, 1], [31, 0, 2], [53, 0, 3], [75, 0, 4], [102, 0, 5]]

rings=[[0, 0, 0], [0, 0, 0], [25, 1, 0], [50, 2, 0], [100, 3, 0], [20, 0, 1], [40, 0, 2], [80, 0, 3]]

mingold = -1
maxgold = -1

for w in range(len(weapons)):
	for a in range(len(armor_store)):
		for r1 in range(len(rings)):
			for r2 in range(len(rings)):
				if (r1 == r2): continue
				him = Player("boss", 8, 2, 109, 0)
				gold = weapons[w][0] + armor_store[a][0] + rings[r1][0] + rings[r2][0]
				damage = weapons[w][1] + armor_store[a][1] + rings[r1][1] + rings[r2][1]
				armor = weapons[w][2] + armor_store[a][2] + rings[r1][2] + rings[r2][2]
				me = Player("Dave", damage, armor, 100, gold)
				while (him.play(me) and me.play(him)): pass
				if me.hits > 0:
					if mingold < 0: mingold = me.gold
					if me.gold < mingold: mingold = me.gold
					#print("I win with gold: ", me.gold)
				else:
					if maxgold < me.gold:
						maxgold = me.gold

print("Part 1: minimum amount of gold for winning is: ", mingold)
print("Part 2: maximum amount of gold for losing is: ", maxgold)
