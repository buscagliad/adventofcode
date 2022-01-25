#include <vector>
#include <string>
#include <set>
#include <iostream>
#include <string.h>
#include "hist.hh"	
#include "point.hh"
#include "rotmat.hh"

using namespace std;

#define DEBUG 0



typedef struct {
	point	p;
	int		num_matches;
} beacon_t;

class scanner  {
	friend bool scanner_compare(scanner &l, scanner &r, rotmat &rm, point &t);
	public:
		scanner(FILE *f);	// reads --- scanner N ---, and all triplets until blank line
	    string  name() const { return _name; };
		void	out(bool out_beacons = false) const;
		void	adjust(rotmat &rm, point offset, point from_loc);
		void	adjust(rotmat &rm, point offset, scanner *s);
		point   get_location() { return location; };
		bool    get_location(point &loc) { loc = location; return final_location; };
		void	relative_to(scanner *to, rotmat rm, point translate);
		void	set_location(point rotvec, point offset, point from_loc, point from_rot) {
			offset.out  ("Delta Offset");
			rotvec.out("Delta Rotation");
			point t = rotate(offset, rotvec);
			t.out("Rotated offset");
			location = t + from_loc; //  - location;
			location = rotate(location, rotvec);
			location.out(_name + "DEBUG 4");
		};
		point	get_beacon(size_t n) {
			return beacon[n].p + location; };
		size_t	size() { return beacon.size(); };
	private:
		void	move_to_zero(scanner *to);
		string _name;
		point	location;	// relative to 0 - for 0 - (0,0,0)
		point	translate;	// distance relative to relscan
		vector<beacon_t> beacon;
		scanner *relscan;	// location is relative to this scanner
		rotmat	rm;			// rotation matix to orient with 0
		bool	final_location;
};

void
scanner::move_to_zero(scanner *to)
{
	if (!to) return;
	adjust(to->rm, to->translate, to->get_location());
	to->rm.out();
	to->translate.out("Translate");
	move_to_zero(to->relscan);
}

void
scanner::relative_to(scanner *to, rotmat rm, point translate)
{
	if (!to) return;
	printf("Scanner %s   relative_to  %s\n", this->_name.c_str(), to->_name.c_str());
	this->rm = rm;
	this->translate = translate;
	this->relscan = to;
	this->move_to_zero(to);
}


void scanner::adjust(rotmat &rm, point translate, point from_loc)
{
	point	t;

	printf("ADJUST for %s\n", _name.c_str());

	for (uint32_t i = 0; i < beacon.size(); i++)
	{
		t = rm * beacon[i].p;
		beacon[i].p = t;
	}
	translate.out("ADJUST: translate");
	from_loc.out("ADJUST: from location");
	location.out("ADJUST: current location");
	location =  rm * location + translate + from_loc;
	location.out("ADJUST: final location");
}


void scanner::adjust(rotmat &rm, point translate, scanner *s)
{
	point	t;

	printf("ADJUST for %s\n", _name.c_str());

	for (uint32_t i = 0; i < beacon.size(); i++)
	{
		t = rm * beacon[i].p;
		beacon[i].p = t;
	}
	translate.out("ADJUST: translate");
	point from_loc = s->get_location();
	from_loc.out("ADJUST: from location");
	location.out("ADJUST: current location");
	location =  rm * location + translate + from_loc;
	location.out("ADJUST: final location");
}

#define MAX_LINE 100
scanner::scanner(FILE *f)
{
	char	line[MAX_LINE];
	fgets(line, MAX_LINE, f);
	//cout << line;
	_name = line;
	_name.erase(_name.size() - 1);
	relscan = NULL;
	int	xr, yr, zr;
	fgets(line, MAX_LINE, f);
	while (!feof(f) && strlen(line) > 2)
	{
		//cout << line;
		sscanf(line, "%d,%d,%d", &xr, &yr, &zr);
		beacon_t bc;
		bc.p = point(xr, yr, zr);
		bc.num_matches = 0;
		beacon.push_back(bc);
		fgets(line, MAX_LINE, f);
	}
}

void 
scanner::out(bool out_beacons) const
{
	cout << _name << endl;
	location.out("Location");
	for (uint32_t i = 0; out_beacons && (i < beacon.size()); i++)
	{
		point bl = location - beacon[i].p;
		cout << beacon[i].p.x << "," << beacon[i].p.y << "," << beacon[i].p.z << "        ";
		cout << bl.x << "," << bl.y << "," << bl.z << endl;
	}
}





size_t rotvec(vector<point> &z, vector<point> &p, int r1, int r2, int r3, point off)
{
	point rp;
	z.clear();
	//printf("p.size(): %lu\n", p.size());
	if (DEBUG) off.out("OFFSET");
	for (size_t i = 0; i < p.size(); i++)
	{
		//rp = rotate(off, r1, r2, r3);
		rp = off - p[i];
		if (DEBUG) rp.out("Subtract from Offset");
	    rp = rotate(rp, r1, r2, r3);
		if (DEBUG) rp.out("Apply rotation");
	    if (DEBUG) p[i].out("From");
	    if (DEBUG) printf("    r1,r2,r3: %d,%d,%d ", r1, r2,r3);
	    if (DEBUG) rp.out("To");
	    z.push_back(rp);
	}
	return z.size();
}

int count_match(vector<point> &v, vector<point> &w)
{
	int count = 0;
	for (uint32_t i = 0; i < v.size(); i++)
	{
		for (uint32_t j = 0; j < w.size(); j++)
		{
			point	c = w[j];
			if (v[i] == c) count++;
		}	
	}
	return count;
}

void rotcheck(vector<beacon_t> &v, vector<beacon_t> &w, point off, point revp)
{
	vector<point> l;
	vector<point> r;
	for (size_t i = 0; i < v.size(); i++)
	{
		point x = v[i].p;
		l.push_back(x);
	}
	for (size_t i = 0; i < w.size(); i++)
	{
		r.push_back(w[i].p);
	}
	vector<point> z;

	int r1 = revp.x; 
	int r2 = revp.y; 
	int r3 = revp.z;

	rotvec(z, l, r1, r2, r3, off);

	int cm = count_match(z, r);
	if (cm > 0)
	{
		printf("r1,r2,r3: %d,%d,%d   cm = %d\n", r1, r2, r3, cm);
	}

}

class bcn_set {
	public:
		void clear();
		int add(point bcn);
		bool get(point &bcn, int N);	// returns most popular beacon delta, and true if 
										// greater than or equal to N
		int	size() { return beacons.size(); };
		void out();
	private:
		vector<beacon_t> beacons;
};

void bcn_set::out()
{
	for (size_t i = 0; i < beacons.size(); i++)
	{
		char num[10];
		sprintf(num, "[%4d]", i + 1);
		beacons[i].p.out(num);
	}
	printf("Number of beacons: %d\n", beacons.size());
}

void bcn_set::clear()
{
	beacons.clear();
}

int bcn_set::add(point add_beacon)
{
	for (size_t i = 0; i < beacons.size(); i++)
	{
		if (add_beacon == beacons[i].p)
		{
			beacons[i].num_matches++;
			return beacons[i].num_matches;
		}
	}
	// if we get here we had no matches - add new point
	beacon_t b;
	b.p = add_beacon;
	b.num_matches = 1;
	beacons.push_back(b);
}

bool bcn_set::get(point &diff, int N)
{
	point max;
	int   maxN = 0;
	for (size_t i = 0; i < beacons.size(); i++)
	{
		if (maxN < beacons[i].num_matches)
		{
			maxN = beacons[i].num_matches;
			max = beacons[i].p;
		}
	}
	if ( DEBUG && (maxN >= N) )
	{
		printf("MaxN: %d\n", maxN);
		max.out("Max vector");
	}
	diff = max;
	return maxN >= N;
}

//
// returns true if
// rm * l has 12 or more common beacons (rm is a rotation matrix, l is the 'left' beacon
// a common beacon is one with 12 or more delta vectors in common
// when this occurs, true is returned and trans is set to this delta in the rotated
// frame
bool scanner_compare(scanner &l, scanner &r, rotmat &rm, point &trans)
{
	bcn_set	b;
	//
	// find the delta
	for (size_t i = 0; i < l.beacon.size(); i++)
	{
		point lrv = rm * l.beacon[i].p;
		for (size_t j = 0; j < r.beacon.size(); j++)
		{
			point d;
			d = r.beacon[j].p - lrv;
			b.add(d);
		}
	}
	//
	// if 12 or more common differences, return trans as the delta in the rotated frame
	//

	return b.get(trans, 12);
}		
				

//  scanner 1 must be at 68,-1246,-43
//  scanner 2 must be at 1105,-1205,1229
//  scanner 3 must be at -92,-2380,-20
//  scanner 4 must be at -20,-1133,1061


//
// NOTE: we have already compared two beacons, keeping a histogram of all coordinated
// differences (x - x, x + x, x - y, etc.).  If there are 12 (or more) values that 
//
// index of left beacon (l) and index of right beacon (r)
// indices are the array entry of the beacon within the scanner
// this object keeps track of the 'left' beacon relative to the right 
// beacon.  add(l, r) is called whenever beacon[l] and beacon[r] have a common
// difference in their coordinates, for example, if beacon[l].x and beacon[r].y have
// a common difference.  If this happens three times,


bool	scanner_search(scanner &s1, scanner &s2, rotmat &rm, point &offset)
{
	for (int x = -3; x <= 3; x++)
	{ 
		if (x == 0) continue;
		for (int y = -3; y <= 3; y++)
		{
			if (abs(x) == abs(y)) continue;
			if (y == 0) continue;
			for (int z = -3; z <= 3; z++)
			{
				if ( (abs(x) == abs(z)) ||
					 (abs(y) == abs(z)) ||
					 z == 0) continue;
				rm.setrot(x, y, z);
				//printf("\nx:%d y:%d z:%d\n", x, y, z);
				//rm.out();
				if (scanner_compare(s1, s2, rm, offset)) return true;
			
			}
		}
	}
	return false;
}


#ifdef SCANNER_MAP
typedef struct {
	scan_map_t	*parent;		// if NULL - top of map
	scan_map_t	*first_child;	// if NULL - end of map
	scan_map_t	*next_sibling;	// if NULL - no sibling
	rotmat   rot_to_parent;		// "R" rotate to parent
	point	 trans_to_parent;	// "T" adjust child to parent::  C[n] = R * C[n] + T
} scan_map_t;
	
class scanner_map{
	public:
		scanner_map() { map = NULL; };
		void associate(scanner *parent, scanner *first_child, rotmat &rm, point &translate);
		scan_map_t	*find_parrent(scanner *s);	// find parrent matching s - NULL if no match
		
	private:
		scan_map_t	*map;
}

scan_map_t
* scanner_map::search_parent(scan_map_t *here, scanner *s)
{
	if (!here) return NULL;
	if (here->parent == s) return here;
	if (here->first_child) return search_parent(here->first_child, s);
	if (here->next_sibling) return search_parent(here->next_sibling, s);
	return NULL;
}

scan_map_t
* scanner_map::find_parent(scanner *s)
{
	
void
scanner_map::associate(scanner *parent, scanner *first_child, rotmat &rm, point &translate)
{
	scan_map_t	*sm = (scan_map_t *) calloc (1, sizeof(scan_map_t));
	scan_map_t	*p = find(map, parent);
	if (!p)
#endif

// Need to create a map relationship between scanners:
//
//						s[3]
//						/
//      s[0] -> s[1] --
//						\
//						s[4] ---- s[2]
//
//      s[1] transforms to s[0] frame via R1,0 * s[1] + T1,0
//      s[4] transforms to s[0] via R



int main(int argc, char **argv)
{
	
	scanner *s[100];
	FILE *f = fopen("data.txt", "r");
	int  n = 0;
	rotmat	rm;
	point translate;
	rotmat I;
	I.setrot(1,2,3);
	rMatrices	rScan;
	set<int>	scanset;
	while (!feof(f))
	{
		s[n++] = new scanner(f);
		//cout << "calling cout" << endl;
		//s[n-1]->out();
	}
	s[0]->relative_to(NULL, I, translate);


	//
	// search through all scanners
	// create mapping as follows:
	// place each scanner in map, each pointing to one or more scanners that they overlap with
	// the mapping should include the rotation and translation to 'align' the two scanners to
	// same coordiante system.   S[0] is the 'head' of the map
	//
	for (int i = 1; i < n; i++) scanset.insert(i);  // .erase removes the value
													// .find(v) returns iterator to v
	for (int i = 0; i < n; i++)
	{
	    for (set<int>::iterator j = scanset.begin(); j != scanset.end(); j++)
	    {
			if (i == *j) continue;
			if (scanner_search(*s[*j], *s[i], rm, translate))
			{
				rScan.add(rm, translate, *j, i);
				//printf("\n\nScanner %d  ---  Scanner %d\n", i, j);
				//s[i]->relative_to(s[j], rm, translate);
				s[*j]->adjust(rm, translate, s[i]->get_location()); //, s[j]->get_location());
				scanset.erase(j);
			}
		}
	}
	rScan.out();
	//
	// collect all beacon actual location
	//
	bcn_set bcn_map;
	for (int i = 0; i < n; i++)
	{
		for (size_t j = 0; j < s[i]->size(); j++)
		{
			point	b = s[i]->get_beacon(j);
			bcn_map.add(b);
		}
	}
	bcn_map.out();
}
