'''

--- Day 24: Immune System Simulator 20XX ---

After a weird buzzing noise, you appear back at the man's cottage. He seems relieved to see his friend, but quickly notices that the little reindeer caught some kind of cold while out exploring.

The portly man explains that this reindeer's immune system isn't similar to regular reindeer immune systems:

The immune system and the infection each have an army made up of several groups; each group consists of one or more identical units. The armies repeatedly fight until only one army has units remaining.

Units within a group all have the same hit points (amount of damage a unit can take before it is destroyed), attack damage (the amount of damage each unit deals), an attack type, an initiative (higher initiative units attack first and win ties), and sometimes weaknesses or immunities. Here is an example group:

18 units each with 729 hit points (weak to fire; immune to cold, slashing)
 with an attack that does 8 radiation damage at initiative 10

Each group also has an effective power: the number of units in that group multiplied by their attack damage. The above group has an effective power of 18 * 8 = 144. Groups never have zero or negative units; instead, the group is removed from combat.

Each fight consists of two phases: target selection and attacking.

During the target selection phase, each group attempts to choose one target. In decreasing order of effective power, groups choose their targets; in a tie, the group with the higher initiative chooses first. The attacking group chooses to target the group in the enemy army to which it would deal the most damage (after accounting for weaknesses and immunities, but not accounting for whether the defending group has enough units to actually receive all of that damage).

If an attacking group is considering two defending groups to which it would deal equal damage, it chooses to target the defending group with the largest effective power; if there is still a tie, it chooses the defending group with the highest initiative. If it cannot deal any defending groups damage, it does not choose a target. Defending groups can only be chosen as a target by one attacking group.

At the end of the target selection phase, each group has selected zero or one groups to attack, and each group is being attacked by zero or one groups.

During the attacking phase, each group deals damage to the target it selected, if any. Groups attack in decreasing order of initiative, regardless of whether they are part of the infection or the immune system. (If a group contains no units, it cannot attack.)

The damage an attacking group deals to a defending group depends on the attacking group's attack type and the defending group's immunities and weaknesses. By default, an attacking group would deal damage equal to its effective power to the defending group. However, if the defending group is immune to the attacking group's attack type, the defending group instead takes no damage; if the defending group is weak to the attacking group's attack type, the defending group instead takes double damage.

The defending group only loses whole units from damage; damage is always dealt in such a way that it kills the most units possible, and any remaining damage to a unit that does not immediately kill it is ignored. For example, if a defending group contains 10 units with 10 hit points each and receives 75 damage, it loses exactly 7 units and is left with 3 units at full health.

After the fight is over, if both armies still contain units, a new fight begins; combat only ends once one army has lost all of its units.

For example, consider the following armies:

Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with
 an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
 slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack
 that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire,
 cold) with an attack that does 12 slashing damage at initiative 4

If these armies were to enter combat, the following fights, including details during the target selection and attacking phases, would take place:

Immune System:
Group 1 contains 17 units
Group 2 contains 989 units
Infection:
Group 1 contains 801 units
Group 2 contains 4485 units

Infection group 1 would deal defending group 1 185832 damage
Infection group 1 would deal defending group 2 185832 damage
Infection group 2 would deal defending group 2 107640 damage
Immune System group 1 would deal defending group 1 76619 damage
Immune System group 1 would deal defending group 2 153238 damage
Immune System group 2 would deal defending group 1 24725 damage

Infection group 2 attacks defending group 2, killing 84 units
Immune System group 2 attacks defending group 1, killing 4 units
Immune System group 1 attacks defending group 2, killing 51 units
Infection group 1 attacks defending group 1, killing 17 units

Immune System:
Group 2 contains 905 units
Infection:
Group 1 contains 797 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 184904 damage
Immune System group 2 would deal defending group 1 22625 damage
Immune System group 2 would deal defending group 2 22625 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 144 units

Immune System:
Group 2 contains 761 units
Infection:
Group 1 contains 793 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183976 damage
Immune System group 2 would deal defending group 1 19025 damage
Immune System group 2 would deal defending group 2 19025 damage

Immune System group 2 attacks defending group 1, killing 4 units
Infection group 1 attacks defending group 2, killing 143 units

Immune System:
Group 2 contains 618 units
Infection:
Group 1 contains 789 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 183048 damage
Immune System group 2 would deal defending group 1 15450 damage
Immune System group 2 would deal defending group 2 15450 damage

Immune System group 2 attacks defending group 1, killing 3 units
Infection group 1 attacks defending group 2, killing 143 units

Immune System:
Group 2 contains 475 units
Infection:
Group 1 contains 786 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 182352 damage
Immune System group 2 would deal defending group 1 11875 damage
Immune System group 2 would deal defending group 2 11875 damage

Immune System group 2 attacks defending group 1, killing 2 units
Infection group 1 attacks defending group 2, killing 142 units

Immune System:
Group 2 contains 333 units
Infection:
Group 1 contains 784 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181888 damage
Immune System group 2 would deal defending group 1 8325 damage
Immune System group 2 would deal defending group 2 8325 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units

Immune System:
Group 2 contains 191 units
Infection:
Group 1 contains 783 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181656 damage
Immune System group 2 would deal defending group 1 4775 damage
Immune System group 2 would deal defending group 2 4775 damage

Immune System group 2 attacks defending group 1, killing 1 unit
Infection group 1 attacks defending group 2, killing 142 units

Immune System:
Group 2 contains 49 units
Infection:
Group 1 contains 782 units
Group 2 contains 4434 units

Infection group 1 would deal defending group 2 181424 damage
Immune System group 2 would deal defending group 1 1225 damage
Immune System group 2 would deal defending group 2 1225 damage

Immune System group 2 attacks defending group 1, killing 0 units
Infection group 1 attacks defending group 2, killing 49 units

Immune System:
No groups remain.
Infection:
Group 1 contains 782 units
Group 2 contains 4434 units

In the example above, the winning army ends up with 782 + 4434 = 5216 units.

You scan the reindeer's condition (your puzzle input); the white-bearded man looks nervous. As it stands now, how many units would the winning army have?
'''

# Units within a group all have the same hit points (amount of damage a unit can 
# take before it is destroyed), attack damage (the amount of damage each unit 
# deals), an attack type, an initiative (higher initiative units attack first and 
# win ties), and sometimes weaknesses or immunities. Here is an example group:

# Immune System:
# 8233 units each with 2012 hit points (immune to radiation) with an attack that does 2 fire damage at initiative 5
# 2739 units each with 5406 hit points (immune to fire) with an attack that does 16 fire damage at initiative 3
# 229 units each with 6782 hit points (weak to slashing) with an attack that does 260 cold damage at initiative 7
# 658 units each with 12313 hit points with an attack that does 132 bludgeoning damage at initiative 4
# 3231 units each with 1872 hit points (weak to slashing, cold) with an attack that does 5 bludgeoning damage at initiative 1
# 115 units each with 10354 hit points (immune to fire, radiation, bludgeoning) with an attack that does 788 cold damage at initiative 2
# 1036 units each with 9810 hit points (weak to radiation) with an attack that does 94 bludgeoning damage at initiative 8
# 3389 units each with 6734 hit points with an attack that does 19 cold damage at initiative 18
# 2538 units each with 5597 hit points (weak to slashing, radiation) with an attack that does 15 slashing damage at initiative 16
# 6671 units each with 6629 hit points (immune to bludgeoning) with an attack that does 8 slashing damage at initiative 14

# Infection:
# 671 units each with 17509 hit points with an attack that does 52 cold damage at initiative 12
# 7194 units each with 41062 hit points (immune to cold; weak to radiation) with an attack that does 11 bludgeoning damage at initiative 20
# 1147 units each with 37194 hit points (weak to radiation, fire) with an attack that does 56 slashing damage at initiative 11
# 569 units each with 27107 hit points (weak to slashing, bludgeoning) with an attack that does 93 slashing damage at initiative 17
# 140 units each with 19231 hit points (immune to slashing; weak to bludgeoning) with an attack that does 247 slashing damage at initiative 19
# 2894 units each with 30877 hit points (immune to radiation, bludgeoning) with an attack that does 15 radiation damage at initiative 10
# 1246 units each with 8494 hit points (weak to fire) with an attack that does 12 bludgeoning damage at initiative 9
# 4165 units each with 21641 hit points (weak to radiation; immune to fire) with an attack that does 10 radiation damage at initiative 6
# 7374 units each with 24948 hit points (weak to cold) with an attack that does 5 fire damage at initiative 13
# 4821 units each with 26018 hit points with an attack that does 10 fire damage at initiative 15

NONE = 0x00
FIRE = 0x01
RADIATION = 0x02
SLASHING = 0x04
COLD = 0x08
BLUDGE = 0x10

GTYPE = ""

SELECT = 1
ATTACK = 2
mode = SELECT

def getPower(dtype):
    if dtype == "fire": return FIRE
    elif dtype == "cold": return COLD
    elif dtype == "bludgeoning": return BLUDGE
    elif dtype == "slashing": return SLASHING
    elif dtype == "radiation": return RADIATION
    else:
        print("getPower   Unknown dtype: ", dtype)
        exit(1)
def dt(dtype):
    rv = ""
    if dtype & FIRE: rv += "fire "
    if dtype & COLD: rv +=  "cold "
    if dtype & BLUDGE: rv +=  "bludgeoning "
    if dtype & SLASHING: rv +=  "slashing "
    if dtype & RADIATION: rv +=  "radiation " 
    return rv

def parse(l):
    weak = NONE
    immune = NONE
    w = l.split()
    setI = False
    for a in w:
        if a == "immune": 
            setI = True
            continue
        if a == "weak": 
            setI = False
            continue
        if 'fire' in a:
            if setI: immune |= FIRE
            else: weak |= FIRE
        elif 'radiation' in a:
            if setI: immune |= RADIATION
            else: weak |= RADIATION
        elif 'slash' in a:
            if setI: immune |= SLASHING
            else: weak |= SLASHING
        elif 'bludg' in a:
            if setI: immune |= BLUDGE
            else: weak |= BLUDGE
        elif 'cold' in a:
            if setI: immune |= COLD
            else: weak |= COLD
    return immune, weak
        

class group:
    def __init__(self, line):
        self.units = 0
        self.hitpoints = 0
        
        self.immunity = NONE
        self.damage = NONE
        self.weak = NONE
        
        popen = line.find("(")
        pclose = line.find(")")
        if popen > -1:
            imwk = line[popen+1:pclose]
            nline = line[:popen] + line[pclose+1:]
            self.immunity, self.weak = parse(imwk)
        else:
            nline = line
        
        w = nline.strip().split()
        self.units = int(w[0])
        self.hitpoints = int(w[4])
        self.initiative = int(w[17])
        
        ##
        ## damage
        ##
        self.damage = int(w[12])
        self.damage_type = getPower(w[13])
        self.id = GTYPE
        self.power=self.damage*self.damage
        self.attacks = None
        self.attackPower = 0
    def __lt__(self, other):
        if mode == SELECT:
            if ((self.power) > (other.power)): return True
            if (self.power == other.power and
                self.initiative > other.initiative): return True
        if mode == ATTACK:
            if self.initiative > other.initiative: return True
        return False
    def attackdamage(self, other):
        odmg = self.damage * self.units
        mult = 1
        if self.damage_type & other.weak: mult = 2
        if self.damage_type & other.immunity: mult = 0
        return odmg * mult
    def setattack(self, toAttack, toPower):
        self.attacks = toAttack
        self.attackPower = toPower
    def attack(self):
        damage = self.attackdamage(self.attacks)
        nu0 = self.attacks.units
        self.attacks.attacked(damage)
        nu1 = self.attacks.units
        print(self.id, " attacks ", self.attacks.id, " killing ", nu0 - nu1, " units.")
    def attacked(self, damage):
        k = damage // self.hitpoints
        self.units -= k
        if self.units < 0: self.units = 0
    def out(self):
        print(self.id, " ", self.units, " units ", self.hitpoints, " hit points ",  self.damage, dt(self.damage_type), "  power: ", self.power, "  initiative: ",self.initiative)
        print("    weak: ", dt(self.weak), "   immune: ", dt(self.immunity))
        if self.attacks:
            print("    attacks: ", self.attacks.id, "  with power: ", self.attackPower)
            kills = self.attackdamage(self.attacks)//self.attacks.hitpoints
            print("  attack: ", self.attackdamage(self.attacks), "  hp: ", self.attacks.hitpoints, "   would kill ", kills, "units")


ImmuneSystem = []
Infection = []

for l in open('test.txt'):
    if (len(l) < 2): continue
    if "Immune System" in l:
        IS = True
        n = 0
        continue
    if "Infection" in l:
        IS = False
        n = 0
        continue
    n += 1
    if IS:
        GTYPE = "ImmSys" + str(n)
        ImmuneSystem.append(group(l))
    else:
        GTYPE = "Infect" + str(n)
        Infection.append(group(l))

'''
print("Immune")
for a in ImmuneSystem:
    a.out()
print("Infection")
for a in Infection:
    a.out()
'''
#
# Order will contain each group in the order of the attack (after
# sorting
#
N = []
N.clear()
for a in ImmuneSystem: N.append(a)
for b in Infection: N.append(b)

nimm = 2
ninf = 2
while nimm > 0 and ninf > 0:
    print("******************************")
    mode = SELECT
    N.sort()
    for a in N:
        if a.units <= 0: continue
        for b in N:
            if a is b or a.id[0:2] == b.id[0:2]: continue
            if b.units <= 0 : continue
            if a.attackdamage(b) > a.attackPower:
                a.attacks = b
                a.attackPower = a.attackdamage(b)

    mode = ATTACK
    N.sort()
    for n in N:
        if n.units <= 0: continue
        n.attack()
    nimm = 0
    ninf = 0
    for n in N:
        if n.id[0:3] == "Imm" and n.units > 0: 
            nimm += n.units
        elif n.id[0:3] == "Inf" and n.units > 0: ninf += n.units
        if n.units > 0:
            print(n.id, " has ", n.units, " units")
        
print("Part 1: winning army has ", max(nimm,ninf), " units")
