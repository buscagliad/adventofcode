# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)
#
# STRICT rules:
#
#    byr (Birth Year) - four digits; at least 1920 and at most 2002.
#    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
#    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
#    hgt (Height) - a number followed by either cm or in:
#        If cm, the number must be at least 150 and at most 193.
#        If in, the number must be at least 59 and at most 76.
#    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
#    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
#    pid (Passport ID) - a nine-digit number, including leading zeroes.
#    cid (Country ID) - ignored, missing or not.


from string import digits, hexdigits


class passport:
    def __init__(self, inline, strict):
        self.v_byr = False
        self.v_iyr = False
        self.v_eyr = False
        self.v_hgt = False
        self.v_hcl = False
        self.v_ecl = False
        self.v_pid = False
        self.v_cid = False
        nvpl = inline.split()   # list of all name value pairs
        #print("In passport constructor  " + inline)
        for item in nvpl:
            nvp = item.partition(':')
            if nvp[0] == 'byr':
                self.byr = int(nvp[2])
                if not(strict) : self.v_byr = True
                elif strict and len(nvp[2]) == 4 and 1920 <= self.byr and self.byr <= 2002 :
                    self.v_byr = True
            elif nvp[0] == 'iyr':
                self.iyr = int(nvp[2])
                if not(strict) : self.v_iyr = True
                elif strict and 2010 <= self.iyr and self.iyr <= 2020 : 
                    self.v_iyr = True
            elif nvp[0] == 'eyr':
                self.eyr = int(nvp[2])
                if not(strict) : self.v_eyr = True
                elif strict and 2020 <= self.eyr and self.eyr <= 2030 : self.v_eyr = True
            elif nvp[0] == 'hgt':
                self.hgt = nvp[2]
                if not(strict) and len(self.hgt) > 0 : 
                    self.v_hgt = True
                    continue
                if self.hgt.find('cm') >= 0 : 
                    h = int(nvp[2].replace('cm', ''))
                    if 150 <= h and h <= 193 : self.v_hgt = True
                elif self.hgt.find('in') >= 0 : 
                    h = int(nvp[2].replace('in', ''))
                    if 59 <= h and h <= 76 : self.v_hgt = True
            elif nvp[0] == 'hcl':
                self.hcl = nvp[2]
                if not(strict) : self.v_hcl = True
                else:
                    if self.hcl[0] == '#' and len(self.hcl) == 7:
                        self.v_hcl = True
                        for c in self.hcl[1:]:
                            self.v_hcl = self.v_hcl and c in hexdigits
            elif nvp[0] == 'ecl':
                self.ecl = nvp[2]
                if not(strict) : self.v_ecl = True
                else:
                    for ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                        if ecl == self.ecl :
                            self.v_ecl = True
                            break
                    #print("Testing eye color with " + self.ecl + " : " + str(self.v_ecl))

            elif nvp[0] ==  'pid':
                self.pid = nvp[2]
                if not(strict) : self.v_pid = True
                else: 
                    if len(self.pid) == 9:
                        self.v_pid = True
                        for c in self.pid[1:]:
                            self.v_pid = self.v_pid and c in digits
            elif nvp[0] ==  'cid':
                self.cid = int(nvp[2])
                if self.cid > 0 : self.v_cid = True
        self.valid = self.v_byr and self.v_iyr and self.v_eyr and self.v_hgt and self.v_hcl and self.v_ecl and self.v_pid
    def out(self):
        print("")
        if (self.v_byr) : print("Birth Year: " + str(self.byr))
        if (self.v_iyr) : print("Issue Year: " + str(self.iyr))
        if (self.v_eyr) : print("Expiration Year: " + str(self.eyr))
        if (self.v_hgt) : print("Height: " + self.hgt)
        if (self.v_hcl) : print("Hair Color: " + self.hcl)
        if (self.v_ecl) : print("Eye Color: " + self.ecl)
        if (self.v_pid) : print("Passport ID: " + str(self.pid))
        if (self.v_cid) : print("Country ID: " + str(self.cid))
        print("PASSPORT VALID: " + str(self.valid))

def init(fname, strict):
    pps = []
    pline = ""
    with open(fname) as f:
        for line in f:
            if (line.isspace()):
                pps.append(passport(pline, strict))
                pline = ""
            else:
                pline = pline + " " + line.strip();
    if len(pline) > 0 : pps.append(passport(pline, strict))
    return pps

def count_passports(fname, strict):
    pps = init(fname, strict)
    count = 0
    for p in pps:
        if p.valid : count = count + 1
    return count

print (str(count_passports('data.txt', False)) + " valid passports - no strict controls.")
print (str(count_passports('data.txt', True)) + " valid passports - STRICT controls.")