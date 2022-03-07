#include <stdint.h>
#include <vector>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <bits/stdc++.h>

static bool debug = false;

using namespace std;

bool	linsect(int l1, int r1, int l2, int r2)
{
	if ( (r1 < l2) || (r2 < r1) ) return false;
	return true;
}

void	swap(int *a, int i, int j)
{
	if (a[i] < a[j])
	{
		int ha = a[i];
		a[i] = a[j];
		a[j] = ha;
	}
}

class side;
void make_sides(int a, int b, int c, int d, vector<side> &sp);



class side {
	public:
		side (int64_t _l, int64_t _r) { l = _l; r = _r;
			//if (_l < _r){ l = _l;  r = _r;}
			// else l = _r;  r = _l;
			if (l > r) printf("ERROR left: %ld  greater than  right: %ld\n", l, r);
			};
		
			//NOT INTERSECTING IS the following two cases - all others are intersecting
			//    s:   |-----|
			// this:           |-------------|
			//
			//  **OR**
			//
			//    s:                             |-----|
			// this:           |-------------|
		bool intersect(side s) { 
			if ( (this->l > s.r) || (this->r < s.l) ) return false; 
			return true; 
		};
		bool contains(side s)
		{
			if ( (this->l <= s.l) && (this->r >= s.r) ) return true;
			return false;
		}

		bool split(side s, vector<side> &sp);
		void out(const char *str = ""){ printf("%s (%ld,%ld) ", str, l, r); };
		int64_t length() { return r - l + 1; };
		
	private:
		int64_t	l;  // left side
		int64_t r;  // right side
};

bool side::split(side s, vector<side> &sp)
{
	sp.clear();
	//
	//    s:   |-----|
	// this:           |-------------|
	//
	//  **OR**
	//
	//    s:                             |-----|
	// this:           |-------------|
	if (!intersect(s)) return false;

	int a = s.l;
	int b = s.r;
	int c = this->l;
	int d = this->r;
	//
	// if segments are identical, return s
	//
	if ( (a == c) && (b == d) ) { sp.push_back(s); return true; }
	
	//
	// if left sides are equal, split into two segments
	if (a == c)	// b == d was handled above
	{
		if (d < b)
		{
			//          a                      b
			//    s:    |----------------------|
			// this:    |--------------|
			//          c              d
			//  [a,b] ^ [c,d]  --> [a, d] + [d + 1, b]
			//
			side one(a, d);
			side two(d+1, b);
			sp.push_back(one);
			sp.push_back(two);
			return true;
		}
		else // (d > b)
		{
			//          a                      b
			//    s:    |----------------------|
			// this:    |-------------------------|
			//          c                         d
			//  [a,b] ^ [c,d]  --> [a, b] + [b + 1, d]
			side one(a, b);
			side two(b+1, d);
			sp.push_back(one);
			sp.push_back(two);
			return true;
		}
	}
	//
	// if right sides are equal, split into two segments
	if (b == d)	// a == c was handled above
	{
		if (a < c)
		{
			//          a                      b
			//    s:    |----------------------|
			// this:            |--------------|
			//                  c              d
			//  [a,b] ^ [c,d]  --> [a, c-1] + [c, b]
			//
			side one(a, c-1);
			side two(c, b);
			sp.push_back(one);
			sp.push_back(two);
			return true;
		}
		else // (a > c)
		{
			//             a                      b
			//    s:       |----------------------|
			// this:    |-------------------------|
			//          c                         d
			//  [a,b] ^ [c,d]  --> [c, a-1] + [a, b]
			side one(c, a-1);
			side two(a, b);
			sp.push_back(one);
			sp.push_back(two);
			return true;
		}
	}
	//
	// if we get here, we need to return three splits...
	//
	//          a                      b
	//    s:    |----------------------|
	// this:        |--------------|
	//              c              d
	//  [a,b] ^ [c,d]  --> [a, c-1] + [c, d] + [d + 1, b]
	//
	if ( (a < c) && (d < b) )
	{
		side one(a, c-1);
		side two(c, d);
		side three(d+1, b);
		sp.push_back(one);
		sp.push_back(two);
		sp.push_back(three);
		return true;
	}
	//                      a           b
	//    s:                |-----------|
	// this:        |--------------|
	//              c              d
	//  [a,b] ^ [c,d]  --> [c, a-1] + [a, d] + [d + 1, b]
	if ( (c < a) && (d < b) )
	{
		side one(c, a-1);
		side two(a, d);
		side three(d+1, b);
		sp.push_back(one);
		sp.push_back(two);
		sp.push_back(three);
		return true;
	}
	//
	//          a             b
	//    s:    |-------------|
	// this:        |--------------|
	//              c              d
	//  [a,b] ^ [c,d]  --> [a, c-1] + [c, b] + [b + 1, d]
	if ( (a < c) && (b < d) )
	{
		side one(a, c-1);
		side two(c, b);
		side three(b+1, d);
		sp.push_back(one);
		sp.push_back(two);
		sp.push_back(three);
		return true;
	}
	//
	//                 a       b
	//    s:           |-------|
	// this:        |--------------|
	//              c              d
	//  [a,b] ^ [c,d]  --> [c, a-1] + [a, b] + [b + 1, d]
	if ( (c < a) && (b < d) )
	{
		side one(c, a-1);
		side two(a, b);
		side three(b+1, d);
		sp.push_back(one);
		sp.push_back(two);
		sp.push_back(three);
		return true;
	}

	printf("INVALID case - not possible to get here.\n");
	s.out("S: ");
	this->out("THIS*: ");
	return false;
};


void out_vside(vector<side> &s, const char *str = "")
{
	printf("%s", str);
	for (unsigned int i = 0; i < s.size(); i++)
	    s[i].out();
}

void make_sides(int a, int b, int c, int d, vector<side> &sp)
{
	sp.clear();
	vector<int> x;
	x.push_back(a);
	x.push_back(b);
	x.push_back(c);
	x.push_back(d);
	sort(x.begin(), x.end());
	x.erase( unique( x.begin(), x.end() ), x.end() );
	
	if (x.size() == 1) {	// all of the values are equal
		sp.push_back(side(a, b)); 
		return;
	}
	else {
		if (x.size() == 2) { sp.push_back(side(x[0], x[1])); return; }
		if (x.size() == 3) { sp.push_back(side(x[0], x[1] - 1)); 
							 sp.push_back(side(x[1], x[2])); return; }
		sp.push_back(side(x[0], x[1] - 1)); 
		sp.push_back(side(x[1], x[2]));
		sp.push_back(side(x[2] + 1, x[3]));
		return;
	}
}


class cube;

static int g_cube_id = 0;

class cube {
	public:
		friend bool add_unique(vector<cube>	&ilist, cube c);

		typedef enum {NEW, ACTIVE, ERASED} cube_state;
		void out(vector<cube> &c);
		cube() : x(0,0), y(0,0), z(0,0), state(NEW) { id = ++g_cube_id; };
		cube(int64_t lx, int64_t rx, int64_t ly, 
			 int64_t ry, int64_t lz, int64_t rz) : x(lx, rx), y(ly, ry), z(lz, rz), state(NEW)
			 { id = ++g_cube_id; } ;
		cube(side _x, side _y, side _z) : x(_x), y(_y), z(_z), state(NEW)  {id = ++g_cube_id;  };
		int64_t	size() { return x.length() * y.length() * z.length(); }
		#define BOOL(b) ((b)?"true":"false")
		bool intersect(cube c) {
			bool xi = x.intersect(c.x);
			bool yi = y.intersect(c.y);
			bool zi = z.intersect(c.z);
			//x.out("X "); c.x.out("C.X"); printf("  xi: %s\n", BOOL(xi));
			//y.out("Y "); c.y.out("C.Y"); printf("  yi: %s\n", BOOL(yi));
			//z.out("Z "); c.z.out("C.Z"); printf("  zi: %s\n", BOOL(zi));
			return 	xi && yi && zi; };

		void out(const char *text = NULL)
		{
			if (!text) text = "Cube: ";
			printf("[%6.6d] %s", id, text);
			x.out("X: "); y.out("Y: "); z.out("Z: ");
			printf("   [%s]  Size: %ld\n", state == NEW ? "NEW" : state == ACTIVE ? "ACTIVE" : "ERASED", size());
		}
		bool	split(cube s, vector<cube> &clist, bool clear = true)
		{
			bool  rv = false;
			if (clear) clist.clear();
			if (!intersect(s)) return false;
			vector<side> nx, ny, nz;
			x.split(s.x, nx);
			y.split(s.y, ny);
			z.split(s.z, nz);
			if (debug) {
				printf("IN SPLIT:  S: %d   *this: %d\n", s.id, this->id);
				printf("x-list: "); out_vside(nx);
				printf(" y-list: "); out_vside(ny);
				printf(" z-list: "); out_vside(nz);
			}
			for (size_t i = 0; i < nx.size(); i++)
			{
				for (size_t j = 0; j < ny.size(); j++)
				{
					for (size_t k = 0; k < nz.size(); k++)
					{
						cube c(nx[i], ny[j], nz[k]);
						if (this->contains(c)) continue;
						if (s.contains(c)) clist.push_back(c);
						//add_unique(clist, c);
					}
				}
			}
			return rv;
		}
		int		contains(cube c);	// returns 1 if *this contains c, -1 vice versa, 0 otherwise
		bool	is_new() { return state == NEW; };
		bool	is_active() { return state == ACTIVE; };
		bool    is_erased() { return state == ERASED; };
		void	set_erased() { state = ERASED; };
		void	set_active() { if (state != ERASED) state = ACTIVE; };
	private:
		side x, y, z;
		cube_state state;
		int	id;
};

int	cube::contains(cube c)
{
	if ( (x.contains(c.x) &&  y.contains(c.y) && z.contains(c.z) ) ) return 1;
	if ( (c.x.contains(x) &&  c.y.contains(y) && c.z.contains(z) ) ) return -1;
	return 0;
}

void cube::out(vector<cube> &c)
{
	int64_t ncs = 0;
	for (vector<cube>::iterator it = c.begin(); it != c.end(); it++)
	{
		(*it).out();
		ncs += (*it).size();
	}
	printf("Number of lights: %ld\n", ncs);
}
	

class vcube {
	public:
		bool add(cube c);
		bool remove(cube c);
		bool fix();	// look for intersecting cubes in reboot - fix them
					// returns false if not 'fixed'
		void out();
		int64_t	size();
		const cube *reset() { it = reboot.begin(); return &(*it); };
		const cube *next() { it++; if (it == reboot.end()) return NULL; else return &(*it);};
		void list_unique();
		void clean();
	private:
		void append(vector<cube> &a);
		bool handle(cube c, bool on);
		bool rhandle(cube c, bool on, vector<cube> &vc);
		vector<cube>	reboot;
		vector<cube>::iterator it;
		
};

void vcube::clean()
{
	bool is_clean = false;
	while (!is_clean)
	{
		for (it = reboot.begin(); it != reboot.end(); it++)
		{
			if ((*it).is_erased())
			{
				reboot.erase(it);
				break;
			}
		}
		if (it == reboot.end()) is_clean = true;
	}
}

void vcube::append(vector<cube> &a)
{
	for (vector<cube>::iterator t = a.begin(); t != a.end(); t++)
		reboot.push_back(*t);
}

bool vcube::fix()
{
	vector<cube>::iterator first;
	vector<cube>::iterator second;
	vector<cube> addlist;
	bool	rv = true;
	for (first  = reboot.begin(); first != reboot.end(); first++)
	{
		if (first->is_erased()) continue;
		
		for (second = reboot.begin(); second != reboot.end(); second++)
		{
			if (second->is_erased()) continue;
			if (first == second) continue;
			if (first->intersect(*second))
			{
				vector<cube>	ilist;
				first->split(*second, ilist, true);
				if (debug) {
					printf("FIX ::"); 
					first->out(); 
					printf(" intersects with "); 
					second->out(); 
					printf("\n");
				}
				second->set_erased();
				if (debug) printf("   FIX SPLIT: *it -> c  \n");
				for (vector<cube>::iterator ilt = ilist.begin(); ilt != ilist.end(); ilt++)
				{
					if (debug) { printf("FIX: Adding: \n"); ilt->out(); }
					addlist.push_back(*ilt);
					rv = false;
				}
			}
		}
	}
	append(addlist);
	if (!rv) return fix();
	return true;
}				

int64_t	vcube::size()
{	
	int64_t ncs = 0;
	for (it = reboot.begin(); it != reboot.end(); it++)
	{
		if ((*it).is_erased()) continue;
		ncs += (*it).size();
	}
	return ncs;
}


void	vcube::out()
{
//	for (vector<cube>::iterator it = reboot.begin(); it != reboot.end(); it++)
//		for (vector<cube>::iterator itn = it+1; itn != reboot.end(); itn++)
	for (size_t i = 0; i < reboot.size(); i++)
	{
		//printf("i = %lu\n", i);
		if ( reboot[i].is_erased() ) continue;
		for (size_t j = i + 1; j < reboot.size(); j++)
		{
			if ( reboot[j].is_erased() ) continue;
			int cont = reboot[i].contains(reboot[j]);
			bool intersect = reboot[i].intersect(reboot[j]);
			if (cont == 1)
			{
				reboot[i].out();
				printf("   CONTAINS    ");
				reboot[j].out();
				reboot[j].set_erased();
			}
			else if (cont == -1)
			{
				reboot[j].out();
				printf("   CONTAINS    ");
				reboot[i].out();
				reboot[i].set_erased();
			}
			else if (intersect)
			{
				reboot[j].out();
				printf("   INTERSECTS    ");
				reboot[i].out();
				//reboot[i].set_erased();
			}
		}
	}
	
	int64_t ncs = 0;
	for (it = reboot.begin(); it != reboot.end(); it++)
	{
		if ((*it).is_erased()) continue;
		(*it).out();
		ncs += (*it).size();
	}
	printf("Number of lights: %ld\n", ncs);
}

void vec_cube_out(vector<cube>	&ilist, const char *s = "VCO: ")
{
	for (size_t n = 0; n < ilist.size(); n++)
	{
		if (ilist[n].is_erased()) continue;
		printf(s); 
		ilist[n].out();
	}
}

bool vec_list_unique(vector<cube>	&ilist)
{
	bool rv = false;
	for (size_t n = 0; n < ilist.size(); n++)
	{
		if (ilist[n].is_erased()) continue;
		for (size_t k = n + 1; k < ilist.size(); k++)
		{
			if (ilist[k].is_erased()) continue;
			if (ilist[n].intersect(ilist[k]))
			{
			    printf("ERROR %lu - %lu\n", n, k);
				printf("  Cube: %lu: ", n);
				ilist[n].out();
				printf("\n  Cube: %lu: ", k);
				ilist[k].out();
				rv = true;
			}
		}
	}
	return rv;
}

void vcube::list_unique()
{
	vec_list_unique(reboot);
}

bool add_unique(vector<cube>	&ilist, cube c)
{
	for (size_t n = 0; n < ilist.size(); n++)
	{
		if (c.intersect(ilist[n]))
		{
			return false;
		}
	}
	ilist.push_back(c);
	return true;
}
//
// rhandle returns true if c is added to add_list
//                 false if not
bool	vcube::rhandle(cube c, bool on, vector<cube> &add_list)
{
//	bool rv = false;
	bool isect = false;
	if (debug) { printf("In rhandle with c: [%s] ", on ? "ON" : "OFF"); (c).out(); }
	if (reboot.size() == 0)
	{
		add_list.push_back(c);
		return true;
	}

	for (vector<cube>::iterator it = reboot.begin(); it != reboot.end(); it++)
	{
		if ((*it).is_erased()) continue;	// ignore 'DELETED' cubes
		//printf("rhandle - loop - it = "); (*it).out("loop");
		// if on is true - do this
		//    contains::
		// 		if (*it) contains  c   do this:: - remove c
		//		if   c   contains *it  do this:: - remove (*it) // ignore it
		//    intersects::
		//		create cubes c.split and *it.split
		//		remove c and *it
		//
		// if on is false (i.e. OFF) - do this
		//    contains::
		// 		if (*it) contains  c   do this:: - remove (c)
		// 		if   c   contains *it  do this:: - need to split and remove *it
		//	  intersects:
		//		create cubes remove all cubes that intersect with c (c is not added)	
		int c_has_it = c.contains(*it);  // 1 c > it, -1 c < it
		if ( on )
		{
			if (c_has_it == 1)	// c contains it
			{
				(*it).set_erased();
				add_list.push_back(c);
				if (debug) {
					printf("C contains *it - deleting *it:"); 
					(*it).out();
				}
				return false;
			}
			else if (c_has_it == -1)	// it contains c
			{
				if (debug) {
					printf("it contains c:"); 
					(*it).out();
				}
				c.set_erased();
				return true;
			}
			else if (c.intersect(*it))
			{
				if (debug) {
					printf("Intersects with "); 
					(*it).out(); 
					printf("\n");
				}
				vector<cube>	ilist;
				(*it).split(c, ilist, true);
				if (debug) printf("SPLIT: *it -> c  \n");
				//(*it).set_erased();
				if (debug) vec_cube_out(ilist, "   ON:: intersect");
				for (vector<cube>::iterator ilt = ilist.begin(); ilt != ilist.end(); ilt++)
				{
					add_list.push_back(*ilt);
				}
				isect = true;
			}
		}
		// if on is false (i.e. OFF) - do this
		//    contains::
		// 		if (*it) contains  c   do this:: - remove (c)
		// 		if   c   contains *it  do this:: - need to split and remove *it
		//	  intersects:
		//		create cubes remove all cubes that intersect with c (c is not added)	
		else  // c is an OFF cube
		{
			if (c_has_it == 1)	// c contains it
			{
				(*it).set_erased();
				if (debug) 
				{
					printf("C contains *it - deleteing *it:"); 
					(*it).out();
				}
			}
			else if (c.intersect(*it))
			{
				if (debug) {
					printf("OFF Intersects with "); 
					(*it).out(); 
					printf("\n");
				}
				vector<cube>	ilist;
				(c).split(*it, ilist, true);
				(*it).split(c, ilist, false);
				if (debug) printf("  OFF-SPLIT: *it -> c  \n");
				(*it).set_erased();
				//(*it).out("*it");
				//(c).out("C");
				if (debug) vec_cube_out(ilist, "OFF - intersect");
				for (vector<cube>::iterator ilt = ilist.begin(); ilt != ilist.end(); ilt++)
				{
					if (!(c.intersect(*ilt)))
					{
						add_list.push_back(*ilt);
						isect = true;
					}
				}			
				//(*it).set_erased();
				//c.set_erased();
			}
		}
	}
	if (on && !isect) add_list.push_back(c);
		
	//c.set_active();
	//add_list.push_back(c);
	return true;
}


bool	vcube::add(cube c)
{
	vector<cube> add_list;
    if (debug) printf("Calling rhandle from add\n");
	rhandle(c, true, add_list);
	if (debug) vec_cube_out(add_list, "vcube::add");
	for (vector<cube>::iterator it = add_list.begin(); it != add_list.end(); it++)
	    reboot.push_back(*it);
	for (vector<cube>::iterator it = reboot.begin(); it != reboot.end(); it++)
	{
		if (!(*it).is_erased()) (*it).set_active();
	}
	return fix();
}

//
// this function is called when a cubeset is turned off;
// in this case, intesecting cubes are created, (split) and
// those that are NOT in the cube c, are returned to the reboot
// object
bool	vcube::remove(cube c)
{
	vector<cube> add_list;
    if (debug) printf("Calling rhandle from remove\n");
	rhandle(c, false, add_list);
	if (debug) vec_cube_out(add_list, "OFF:");
	for (vector<cube>::iterator it = add_list.begin(); it != add_list.end(); it++)
	    reboot.push_back(*it);
	for (vector<cube>::iterator it = reboot.begin(); it != reboot.end(); it++)
	{
		if (!(*it).is_erased()) (*it).set_active();
	}
	return fix();
}

//on x=-31..21,y=-11..42,z=-4..49
void	run_reboot(const char *fname, int64_t max_abs, int64_t expected)
{
	FILE *f = fopen(fname, "r");
#define MAX_INS 1000
	char ins[MAX_INS];
	char *ip;
	vcube reboot;
	vcube on_list;
	vcube off_list;
	while (!feof(f))
	{
		fgets(ins, MAX_INS, f);
		if (feof(f)) break;
		if (ins[0] == '#') continue;
		if (ins[0] == '-') break;
		bool on_off = (strncmp(ins, "off", 3) == 0) ? false : true;
		ip = ins + 3;
		if (!on_off) ip++;
		ip+=2; // move past x=
		int64_t	lx, rx, ly, ry, lz, rz;
		lx = strtoll(ip, &ip, 10);
		ip+=2; // move past ..
		rx = strtoll(ip, &ip, 10);
		ip+=3; // move past ,y=
		ly = strtoll(ip, &ip, 10);
		ip+=2; // move past ..
		ry = strtoll(ip, &ip, 10);
		ip+=3; // move past ,z=
		lz = strtoll(ip, &ip, 10);
		ip+=2; // move past ..
		rz = strtoll(ip, &ip, 10);
		if (max_abs > 0)
		{
			if (abs(lx) > max_abs) continue;
			if (abs(rx) > max_abs) continue;
			if (abs(ly) > max_abs) continue;
			if (abs(ry) > max_abs) continue;
			if (abs(lz) > max_abs) continue;
			if (abs(rz) > max_abs) continue;
		}
		printf("%s x=%ld..%ld,y=%ld..%ld,z=%ld..%ld\n", (on_off?"on":"off"),
			lx, rx, ly, ry, lz, rz);
		cube c(lx, rx, ly, ry, lz, rz);
		if (on_off) {
			reboot.add(c);
			//on_list.add(c);
		}
		else
		{
			reboot.remove(c);
			//off_list.add(c);
		}
		reboot.clean();
		if (debug) printf("\n\n********** reboot.out() ********************************\n");
		if (debug) reboot.out();
		//printf("************** reboot.list_unique() ************************\n");
		//reboot.list_unique();
		if (debug) printf("************************************************************\n\n");
	}
	printf("\n\nREBOOT FINAL:\n");
	reboot.out();
	int64_t actual = reboot.size();
	if (actual == expected)
	{
		printf("\n\nSUCCESS!!!!  --  %ld is CORRECT!\n\n", actual);
	}
	else
	{
		printf("\n\nERROR - expected %ld   got %ld\n\n", expected, actual);
	}

}

int main(int argc, char **argv)
{
	run_reboot("data.txt", 50, 553201);	// part 1 test
	run_reboot("data.txt",  0, 1263946820845866);
	return 1;
}
