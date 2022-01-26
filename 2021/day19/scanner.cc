#include <vector>
#include <string>
#include <set>
#include <iostream>
#include <string.h>
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

	//printf("ADJUST for %s\n", _name.c_str());

	for (uint32_t i = 0; i < beacon.size(); i++)
	{
		t = rm * beacon[i].p;
		beacon[i].p = t;
	}
	//translate.out("ADJUST: translate");
	//from_loc.out("ADJUST: from location");
	//location.out("ADJUST: current location");
	location =  rm * location + translate + from_loc;
	//location.out("ADJUST: final location");
}


void scanner::adjust(rotmat &rm, point translate, scanner *s)
{
	point	t;

	//printf("ADJUST for %s\n", _name.c_str());

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
		size_t add(point bcn);
		bool getb(point &bcn, size_t N);	// returns entry N, false if N is out of bounds
		bool get(point &bcn, int N);	// returns most popular beacon delta, and true if 
										// greater than or equal to N
		size_t	size() { return beacons.size(); };
		void out();
	private:
		vector<beacon_t> beacons;
};

void bcn_set::out()
{
	for (size_t i = 0; i < beacons.size(); i++)
	{
		char num[10];
		sprintf(num, "[%4lu]", i + 1);
		beacons[i].p.out(num);
	}
	printf("Number of beacons: %lu\n", beacons.size());
}

void bcn_set::clear()
{
	beacons.clear();
}

size_t bcn_set::add(point add_beacon)
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
	
	return beacons.size();
}

bool bcn_set::getb(point &bcn, size_t N)
{
	if (N >= beacons.size()) return false;
	bcn = beacons[N].p;
	return true; 

}

bool bcn_set::get(point &maxe, int N)
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
	maxe = max;
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

// Need to create a map relationship between scanners:
//
//						s[3]
//						/
//      s[0] -> s[1] --
//						\   /* test */
//						s[4] ---- s[2]
//
//      s[1] transforms to s[0] frame via R1,0 * s[1] + T1,0
//      s[4] transforms to s[0] via R



int main(int argc, char **argv)
{
	
	scanner *s[100];
	FILE *f = fopen(argv[1], "r");
	size_t  n = 0;
	rotmat	rm;
	point translate;
	rotmat I;
	I.setrot(1,2,3);
	rMatrices	rScan;
	typedef	set<size_t> set_t;
	set_t	scanset;
	set_t	nextset;
	set_t	finalset;
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
	// .erase removes the value
	// .find(v) returns iterator to v
	//
	// first find all scanners related to 0
	//
	scanset.insert(0);	// find 0's first
	finalset.insert(0);
	while (finalset.size() < n)
	{
		for (size_t i = 1; i < n; i++)
		{
			if (finalset.count(i)) continue;
			for (set_t::iterator j = scanset.begin(); j != scanset.end(); j++)
			{
				//printf("Finding %lu related scanners ...\n", *j);
				if (finalset.count(i)) continue;
				if (scanner_search(*s[i], *s[*j], rm, translate))
				{
					s[i]-> adjust(rm, translate, s[*j]->get_location());
					nextset.insert(i);
					finalset.insert(i);
					printf("Scanner %lu related to scanner %lu\n", i, *j);
				}
			}
		}
		scanset.clear();
		scanset = nextset;
		nextset.clear();
		printf("Final set size: %lu\n", finalset.size());
	}

	//
	// count unique beacons
	// class bcn_set holds unique beacons
	//

	bcn_set	bcn_map;
	for (size_t i = 0; i < n; i++)
	{
		for (size_t j = 0; j < s[i]->size(); j++)	// grab each beacon from the sensor
		{
			point b = s[i]->get_beacon(j);
			bcn_map.add(b);	// add will increment counter if b already exists, otherwise inserts
		}
	}
	printf("Number of unique beacons: %lu\n", bcn_map.size());

	//
	// furthest sensors
	//
	point	max_s1;
	point	max_s2;
	int		max_dist = -1;
	for (size_t i = 0; i < n; i++)
	{
		point	s1 = s[i]->get_location();
		for (size_t j = 0; j < i; j++)
		{
			point	s2 = s[j]->get_location();
			if (s1.dist(s2) > max_dist)
			{
				max_s1 = s1;
				max_s2 = s2;
				max_dist = s1.dist(s2);
			}
		}
	}
	max_s1.out("Sensor max 1");
	max_s2.out("Sensor max 2");
	printf("Max sensor distance: %d\n\n", max_dist);

}
