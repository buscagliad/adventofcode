#include <vector>
#include <string>
#include <iostream>
#include <string.h>
#include "hist.hh"	
#include "point.hh"
#include "rotmat.hh"

using namespace std;

#define DEBUG 0


class Pairs;

typedef struct {
	point	p;
	int		matched;
} beacon_t;

class scanner  {
	friend class Pairs;
	public:
		scanner(FILE *f);	// reads --- scanner N ---, and all triplets until blank line
	    string  name() const { return _name; };
		void	analyze(scanner &s);
		void	analyze(const scanner &s, rotmat &rm, point &left_vec, point &right_vec);
		void	out(bool out_beacons = false) const;
		void	adjust(rmobj_t  &rm);
		point   get_location() { return location; };
		void	set_location(point rotvec, point offset, point from_loc, point from_rot) {
			rot_to_zero = rotvec;
// previous  location = offset - location;
			////from_loc.out("From Location - relative to s[0]");
			////from_rot.out("From Rotation - relative to s[0]");
			offset.out  ("Delta Offset");
			rotvec.out("Delta Rotation");
			point t = rotate(offset, rotvec);
			//t = rotate(t, from_rot);
			t.out("Rotated offset");
			location = t + from_loc; //  - location;
			////location.out("t + from_loc");
			//location = rotate(location, rotvec);
			//location.out("After rotation");
			location = rotate(location, rotvec);
			//for (size_t i = 0; i < 0 && i < zero_beacon.size(); i++)
			//{
			//	zero_beacon[i] = offset - zero_beacon[i];
			//	zero_beacon[i] = rotate(zero_beacon[i], rotvec);
			//	beacon[i].p = rotate(beacon[i].p, rotvec);
			//}
			location.out(_name + "DEBUG 4");
		};
		point	translate_to_frame  (point t) const
		{
			location.out("From Location");
			rot_to_zero.out("From Rotation");
			t.out("Tanslation point");
			
			return rotate(t, rot_to_zero) + location;
		};
	private:
		string _name;
		point	location;	// relative to 0 - for 0 - (0,0,0)
		point	rot_to_zero;	// rotate to 0
		vector<beacon_t> beacon;
		vector<point> zero_beacon;	// beacons - relative to 0
		//rotmat	rm;			// rotation matix to orient with 0
};

void scanner::adjust(rmobj_t &rmo)
{
	point	t;

	printf("ADJUST for %s\n", _name.c_str());
	printf("ADJUST:  From: %d to %d\n", rmo.from, rmo.to);

	for (uint32_t i = 0; i < beacon.size(); i++)
	{
		t = rmo.rm * beacon[i].p + rmo.translate;
		beacon[i].p = t;
	}
}

#define MAX_LINE 100
scanner::scanner(FILE *f)
{
	char	line[MAX_LINE];
	fgets(line, MAX_LINE, f);
	//cout << line;
	_name = line;
	_name.erase(_name.size() - 1);
	int	xr, yr, zr;
	fgets(line, MAX_LINE, f);
	while (!feof(f) && strlen(line) > 2)
	{
		//cout << line;
		sscanf(line, "%d,%d,%d", &xr, &yr, &zr);
		beacon_t bc;
		bc.p = point(xr, yr, zr);
		bc.matched = 0;
		beacon.push_back(bc);
		zero_beacon.push_back(bc.p);
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





void scanner::analyze(scanner &s)
{
	rotmat rm;
	point left_vec, right_vec;
	analyze(s, rm, left_vec, right_vec);
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
			//char str[100];
			//sprintf(str, "v[%d] = ", i);
			//v[i].out(str);
			//sprintf(str, "w[%d] + off = ", j);
			//c.out(str);
			
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
		


typedef struct {
	int	l;
	int r;
	int count;
} lr_t;

class Pairs {
	public:
		Pairs(scanner *l,  scanner const *r) { sl = l; sr = r; };
		void add(int l, int r);	
		void flag(point rvec, point off);		
	private:
		vector<lr_t> p;
		scanner *sl;
		scanner  const * sr;
};

static int num_matches = 0;

void Pairs::flag(point rvec, point offset)
{
	for (size_t i = 0; i < p.size(); i++)
	{
		if (p[i].count >= 3)
		{
			point l = sl->beacon[p[i].l].p;
			point r = sr->beacon[p[i].r].p;
			sl->beacon[p[i].l].matched = ++num_matches;
			//sr->beacon[p[i].r].matched = num_matches;
			/*printf("Left %d    Right: %d    Count: %d    num_matches = %d\n",
				p[i].l, p[i].r, p[i].count, num_matches); */
			
		}
		else
		{
			printf("pair: l: %d  r: %d  count: %d\n", p[i].l, p[i].r, p[i].count);
		}
	}
	for (size_t i = 0; i < sr->beacon.size(); i++)
	{
		// rotate vector
		// add offset
		//sr->beacon[i].p.out("Right Beacon");
		point l = rotate(sr->beacon[i].p, rvec.x, rvec.y, rvec.z);
		//l.out("After rotations");
		//sr->beacon[i].p = l;
		//l -= offset;
		//l = l - sl->location;

		//l.out("Right Final");
	}
	point zero(0,0,0);

	//offset = rotate(offset, rvec);
	offset.out("OFFSET");
	rvec.out("ROTATE VECTOR");
	string nm = sr->name();
	string st = nm + "INITIAL RIGHT LOCATION";
	sr->location.out(st);
	sl->location = sr->translate_to_frame(offset);
	sl->location.out(sl->name() + "LEFT LOCATION");
	
	point	sll = sl->location;
	point	newp = sll - offset;
	//newp.out("DAVE");
	//sr->location =  newp;
	//sr->location = zero - sr->location;
	//sr->location.out(sr->name() + "FINAL RIGHT LOCATION");
	//sr->location = point(0,0,0) - sl->location;
	//sr->location = offset - sr->location;
	//sr->location = rotate(sr->location, rvec);
	//sr->location.out("LOCATION");
	//sr->location = point(0,0,0) - sr->location;
	sr->out(false);
	printf("Number of matches: %d\n", num_matches);

//  scanner 1 must be at 68,-1246,-43
//  scanner 2 must be at 1105,-1205,1229
//  scanner 3 must be at -92,-2380,-20
//  scanner 4 must be at -20,-1133,1061

}

void Pairs::add(int l, int r)
{
	for (size_t i = 0; i < p.size(); i++)
	{
		if ( (p[i].l == l) && (p[i].r == r) )
		{
			p[i].count++;
			return;
		}
	}
	lr_t x;
	x.l = l;
	x.r = r;
	x.count = 1;
	p.push_back(x);
}
#define XYZ(c)	( (c == 'x' ? 0 : (c == 'y' ? 1 : (c == 'z') ? 2 : -1)))

#define INDEX(a)	( (a[0] == 'x') ? 0 : (a[0] == 'y') ? 1 : 2 )

#define HIST(v, A, B, op)		hist	v(-2000, 2000); 			\
								for (uint32_t i = 0; i < beacon.size(); i++)	\
								    for (uint32_t j = 0; j < s.beacon.size(); j++) \
										v.add(beacon[i].p.A op s.beacon[j].p.B); \
								v.most(value, count); \
								if (DEBUG) printf("%s %s %s - value: %d   count: %d\n", \
									#A, #op, #B, value, count); \
								l = #A; \
								r = #B; \
								pm = #op; \
								i = XYZ(l[0]); \
								j = XYZ(r[0]); \
								pm1 = (pm[0] == '+' ? -1 : pm[0] == '-' ? 1 : 0); \
								if (count >= 12)  { rm.set(i, j, pm1); \
									right_vec.A = value;	\
									left_vec.B = value;	\
									rvec.A = pm1 * ( 1 + (INDEX(#B)) ); \
									if (DEBUG)printf("%d:: pm1 = %d    A: %s  B: %s   INDEX: %d\n", __LINE__, \
									pm1, #A, #B, INDEX(#B));\
									for (size_t i = 0; i < beacon.size(); i++) \
										for (size_t j = 0; j < s.beacon.size(); j++) { \
											if ((beacon[i].p.A op s.beacon[j].p.B) == value) {\
												if (DEBUG) printf("%d  L[%lu]: %d  %s  %d  R[%lu]\n", \
												value, i, beacon[i].p.A, #op, s.beacon[j].p.B, j); \
											    pairs.add(i, j); \
											 }	\
										}	\
								}


static int num_matched = 0;
void scanner::analyze(const scanner &s, rotmat &rm, point &left_vec, point &right_vec)
{
	int	value, count;
	rotmat m;
	const char *l;
	const char *r;
	const char *pm;
	point	rvec;
	int i;
	int j; 
	int pm1;
	Pairs pairs(this, &s);
	left_vec.clear();
	right_vec.clear();
	rm.clear();
	cout << endl << endl << _name << " vs. " << s._name << endl;
	HIST(xpx, x, x, +);
	HIST(xmx, x, x, -);
	HIST(xpy, x, y, +); 
	HIST(xmy, x, y, -);
	HIST(xpz, x, z, +);
	HIST(xmz, x, z, -);
	HIST(ypx, y, x, +); 
	HIST(ymx, y, x, -); 
	HIST(ypy, y, y, +);
	HIST(ymy, y, y, -); 
	HIST(ypz, y, z, +);
	HIST(ymz, y, z, -);
	HIST(zpx, z, x, +); 
	HIST(zmx, z, x, -); 
	HIST(zpy, z, y, +); 
	HIST(zmy, z, y, -);
	HIST(zpz, z, z, +);
	HIST(zmz, z, z, -);
	
	rm.out("Rotation Matrix");

	if (rm.det()) // this and s have vectors in common - eliminate them
	{
		//pairs.flag(rvec, left_vec);
		if (DEBUG) printf("Comparing %s and %s \n",
					this->_name.c_str(), 
					s._name.c_str());

		//rotcheck(beacon, s.beacon, left_vec, rvec);
		set_location(rvec, right_vec, s.location, s.rot_to_zero);

		return;
		rvec = rotate(rvec, rvec.x, rvec.y, rvec.z);

		//rotcheck(beacon, s.beacon, left_vec, rvec);
		printf("\n\nLINE :%d\n", __LINE__);
		//rotcheck(s.beacon, beacon, left_vec, rvec);
		return;
		for (uint32_t i = 0; i < beacon.size(); i++)
		{
			if (beacon[i].matched) continue;
			//point	a = beacon[i].p;
			point	a =  rm * beacon[i].p + left_vec;
			for (uint32_t j = 0; j < s.beacon.size(); j++)
			{
				if (s.beacon[j].matched) continue;
				point	b = s.beacon[j].p;
				//point	b = rm * s.beacon[j].p + left_vec;
				//printf("[%d] : ", i); a.out(" Bcn");
				//printf("[%d] : ", j); b.out(" Bcn");
				if (a == b) {
					if ( (!beacon[i].matched) && (!s.beacon[j].matched) )
					{
						beacon[i].matched = ++num_matched;
						//s.beacon[j].matched = num_matched;
						printf(" *** MATCHED\n");
						break;
					}
					else if (!beacon[i].matched)	// means s.beacon is already set
					{
						beacon[i].matched = s.beacon[j].matched;
						printf(" *** X-MATCHED - %d\n", s.beacon[j].matched);
						break;
					}
					else if (!s.beacon[j].matched)
					{
						//s.beacon[j].matched = beacon[i].matched;
						printf(" *** Y-MATCHED\n");
						break;
					}
					else
					{
						printf("\nERROR - both %s @ %d and %s @ %d are already set\n",
							this->_name.c_str(), i,
							s._name.c_str(), j);
					}
				}
			}
		}
	}
					
}



int main(int argc, char **argv)
{
	
	point	left(68,-1246,-43);
	point	offset(160,1134,-23);
	point	j = left - offset;
	point	k = offset - left;

	
	
	scanner *s[100];
	FILE *f = fopen("ex.txt", "r");
	int  n = 0;
	rotmat	rm;
	point left_vec, right_vec;
	rotmat I;
	rMatrices rScan;
	//int    offidx = 1;
	//point relpos[50];
	I.set(0,0,1);
	I.set(1,1,1);
	I.set(2,2,1);
	while (!feof(f))
	{
		s[n++] = new scanner(f);
		//cout << "calling cout" << endl;
		//s[n-1]->out();
	}
	
	point zero(0,0,0);
	s[0]->set_location(point(1,2,3), zero, zero, point(1,2,3));
	s[1]->analyze(*s[0], rm, left_vec, right_vec);
	s[3]->analyze(*s[1], rm, left_vec, right_vec);
	//s[3]->analyze(*s[1], rm, left_vec, right_vec);
	//s[4]->analyze(*s[1], rm, left_vec, right_vec);
	s[4]->analyze(*s[1], rm, left_vec, right_vec);
	s[4]->analyze(*s[2], rm, left_vec, right_vec);
	fflush(stdout);
	exit(1);
	s[2]->analyze(*s[4], rm, left_vec, right_vec);
	printf("Num beacons: %d\n", num_matched);
	for (int i = 1; i < n; i++)
	{
	    for (int j = 0; j < n; j++)
	    {
			if (i == j) continue;
			s[i]->analyze(*s[j], rm, left_vec, right_vec);
			if (rm.det())
			{
				cout << s[j]->name() << " vs. " << s[i]->name() << endl;
				left_vec.out("Translation");
				rm.out();
				rScan.add(rm, left_vec, j, i);
				//s[j]->adjust(left_vec, *s[i]);
				cout << endl << endl;
				//exit(1); // QQQ
			}
			rm.clear();
		}
	}
	for (int i = 0; i < n; i++)
	{
		printf(" | ");
		for (int j = 0; j < n; j++)
		{
			rmobj_t r;
			rScan.get(r, i, j);
			if (r.rm.det()) printf(" 1 ");
			else printf("   ");
		}
		printf(" | \n");
	}

	rScan.out();
	printf("Num beacons: %d\n", num_matched);
}
