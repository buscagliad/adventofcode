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

Your puzzle answer was 26914.
--- Part Two ---

Things aren't looking good for the reindeer. The man asks whether more milk and cookies would help you think.

If only you could give the reindeer's immune system a boost, you might be able to change the outcome of the combat.

A boost is an integer increase in immune system units' attack damage. For example, if you were to boost the above example's immune system's units by 1570, the armies would instead look like this:

Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with
 an attack that does 6077 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning,
 slashing) with an attack that does 1595 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack
 that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire,
 cold) with an attack that does 12 slashing damage at initiative 4

With this boost, the combat proceeds differently:

Immune System:
Group 2 contains 989 units
Group 1 contains 17 units
Infection:
Group 1 contains 801 units
Group 2 contains 4485 units

Infection group 1 would deal defending group 2 185832 damage
Infection group 1 would deal defending group 1 185832 damage
Infection group 2 would deal defending group 1 53820 damage
Immune System group 2 would deal defending group 1 1577455 damage
Immune System group 2 would deal defending group 2 1577455 damage
Immune System group 1 would deal defending group 2 206618 damage

Infection group 2 attacks defending group 1, killing 9 units
Immune System group 2 attacks defending group 1, killing 335 units
Immune System group 1 attacks defending group 2, killing 32 units
Infection group 1 attacks defending group 2, killing 84 units

Immune System:
Group 2 contains 905 units
Group 1 contains 8 units
Infection:
Group 1 contains 466 units
Group 2 contains 4453 units

Infection group 1 would deal defending group 2 108112 damage
Infection group 1 would deal defending group 1 108112 damage
Infection group 2 would deal defending group 1 53436 damage
Immune System group 2 would deal defending group 1 1443475 damage
Immune System group 2 would deal defending group 2 1443475 damage
Immune System group 1 would deal defending group 2 97232 damage

Infection group 2 attacks defending group 1, killing 8 units
Immune System group 2 attacks defending group 1, killing 306 units
Infection group 1 attacks defending group 2, killing 29 units

Immune System:
Group 2 contains 876 units
Infection:
Group 2 contains 4453 units
Group 1 contains 160 units

Infection group 2 would deal defending group 2 106872 damage
Immune System group 2 would deal defending group 2 1397220 damage
Immune System group 2 would deal defending group 1 1397220 damage

Infection group 2 attacks defending group 2, killing 83 units
Immune System group 2 attacks defending group 2, killing 427 units

After a few fights...

Immune System:
Group 2 contains 64 units
Infection:
Group 2 contains 214 units
Group 1 contains 19 units

Infection group 2 would deal defending group 2 5136 damage
Immune System group 2 would deal defending group 2 102080 damage
Immune System group 2 would deal defending group 1 102080 damage

Infection group 2 attacks defending group 2, killing 4 units
Immune System group 2 attacks defending group 2, killing 32 units

Immune System:
Group 2 contains 60 units
Infection:
Group 1 contains 19 units
Group 2 contains 182 units

Infection group 1 would deal defending group 2 4408 damage
Immune System group 2 would deal defending group 1 95700 damage
Immune System group 2 would deal defending group 2 95700 damage

Immune System group 2 attacks defending group 1, killing 19 units

Immune System:
Group 2 contains 60 units
Infection:
Group 2 contains 182 units

Infection group 2 would deal defending group 2 4368 damage
Immune System group 2 would deal defending group 2 95700 damage

Infection group 2 attacks defending group 2, killing 3 units
Immune System group 2 attacks defending group 2, killing 30 units

After a few more fights...

Immune System:
Group 2 contains 51 units
Infection:
Group 2 contains 40 units

Infection group 2 would deal defending group 2 960 damage
Immune System group 2 would deal defending group 2 81345 damage

Infection group 2 attacks defending group 2, killing 0 units
Immune System group 2 attacks defending group 2, killing 27 units

Immune System:
Group 2 contains 51 units
Infection:
Group 2 contains 13 units

Infection group 2 would deal defending group 2 312 damage
Immune System group 2 would deal defending group 2 81345 damage

Infection group 2 attacks defending group 2, killing 0 units
Immune System group 2 attacks defending group 2, killing 13 units

Immune System:
Group 2 contains 51 units
Infection:
No groups remain.

This boost would allow the immune system's armies to win! It would be left with 51 units.

You don't even know how you could boost the reindeer's immune system or what effect it might have, so you need to be cautious and find the smallest boost that would allow the immune system to win.

How many units does the immune system have left after getting the smallest boost it needs to win?

Your puzzle answer was 862.

Both parts of this puzzle are complete! They provide two gold stars: **
'''

NONE = 0x00
FIRE = 0x01
RADIATION = 0x02
SLASHING = 0x04
COLD = 0x08
BLUDGE = 0x10


SELECT = 1
ATTACK = 2

#
# global variables:
#
GTYPE = ""

Mode = SELECT
ImmuneSystem = []
Infection = []
N = []

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
    def __init__(self, line, boost = 0):
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
        self.damage = int(w[12]) + boost
        self.damage_type = getPower(w[13])
        self.id = GTYPE
        self.power=self.damage*self.units
        self.attacks = None
        self.attackPower = 0
        self.selected = False
    def __lt__(self, other):
        global Mode
        if Mode == SELECT:
            if ((self.power) > (other.power)): return True
            if (self.power == other.power and
                self.initiative > other.initiative): return True
        if Mode == ATTACK:
            if self.initiative > other.initiative: return True
        return False
    def attackdamage(self, other):
        odmg = self.damage * self.units
        mult = 1
        if self.damage_type & other.weak: mult = 2
        if self.damage_type & other.immunity: mult = 0
        return odmg * mult
  
    def doattack(self, other):
        damage = self.attackdamage(other)
        k = (damage) // other.hitpoints
        other.units -= k
        if other.units < 0: other.units = 0
        other.power = other.units * other.damage
        #print(self.id, " attacks ", other.id, " killing ", k, " units, leaving: ", other.units)
    def unitcost(self, other):
        damage = self.attackdamage(other)
        k = damage // other.hitpoints
        return k
    def out(self):
        print(self.id, " ", self.units, " units ", self.hitpoints, " hit points ",  self.damage, dt(self.damage_type), "  power: ", self.power, "  initiative: ",self.initiative)
        print("    weak: ", dt(self.weak), "   immune: ", dt(self.immunity))
        if self.attacks:
            print("    attacks: ", self.attacks.id, "  with power: ", self.attackPower)
            kills = self.attackdamage(self.attacks)//self.attacks.hitpoints
            print("  attack: ", self.attackdamage(self.attacks), "  hp: ", self.attacks.hitpoints, "   would kill ", kills, "units")


def init(fn, boost):
    global ImmuneSystem, Infection, N, GTYPE
    ImmuneSystem.clear()
    Infection.clear()
    for l in open(fn):
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
            ImmuneSystem.append(group(l, boost))
        else:
            GTYPE = "Infect" + str(n)
            Infection.append(group(l))
    N.clear()
    for a in ImmuneSystem: N.append(a)
    for b in Infection: N.append(b)


#
# Order will contain each group in the order of the attack (after
# sorting
#

def test():
    for a in N:
        if a.units <= 0: continue
        for b in N:
            
            if b.units <= 0 : continue
            if b.selected : continue
            if a is b or a.id[0:2] == b.id[0:2]: continue
            #if a.unitcost(b) == 0: continue
            print("0: ", a.id, " would deal ", b.id, a.attackdamage(b), " damage, killing ", a.unitcost(b))
    exit(1)

def runit(fn, delta = 0):
    global ImmuneSystem, Infection, N, Mode
    init(fn, delta)
    nimm = 2
    ninf = 2
    while nimm > 0 and ninf > 0:
        #print("******************************")
        Mode = SELECT
        N.sort()
        #
        # clear out all armies so they are not selected
        for a in N:
            a.selected = False
            a.attacks = None
            #if a.units <= 0: a.selected = True

        for a in N:
            if a.units <= 0: continue
            for b in N:
                if b.units <= 0 : continue
                if b.selected : continue
                if a is b or a.id[0:2] == b.id[0:2]: continue
                if a.attacks is None:
                    if a.attackdamage(b) > 0:
                        a.attacks = b
                        a.attackPower = a.attackdamage(b)
                        #print("0: ", a.id, " would deal ", b.id, 
                        # a.attackdamage(b), " damage, killing ", a.unitcost(b))
                    continue
                if a.attackdamage(b) > a.attackPower:
                    a.attacks = b
                    a.attackPower = a.attackdamage(b)
            if a.attacks:
                a.attacks.selected = True

        Mode = ATTACK
        N.sort()
        for n in N:
            if n.units <= 0: continue
            if n.attacks:
                #print(n.id, " attacks ", n.attacks.id, " with ", n.attacks.units, "units leaving: ", end = "")
                n.doattack(n.attacks)
                #print(n.attacks.units)
        nimm = 0
        ninf = 0
        for n in N:
            if n.id[0:3] == "Imm" and n.units > 0: 
                nimm += n.units
            elif n.id[0:3] == "Inf" and n.units > 0:
                ninf += n.units
            # if n.units > 0:
                # print(n.id, " has ", n.units, " units")
    if nimm > ninf:
        return "Immune", nimm
    return "Infect", ninf

army, un = runit("data.txt")
    
print("Part 1: winning army is ", army, " with ", un, " units", flush = True)
# 26037 is not correct
# 26838 is too low

#
# Part 2:
#
p1army = army

## by the way, trial and error on the boost number
## anything lest than 47 causing a huge loop - not sure if it converged
## but 48 worked

d = 48
army, un = runit("data.txt", d)
print("Part 2: winning army: ", army, "  remain: ", un, flush = True)

