#include <stdint.h>
#include <vector>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

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


class side {
	public:
		side (int64_t _l, int64_t _r): l(_l), r(_r) {};
		
			//NOT INTERSECTING IS the following two cases - all others are intersecting
			//    s:   |-----|
			// this:           |-------------|
			//
			//  **OR**
			//
			//    s:                             |-----|
			// this:           |-------------|
		bool intersect(side s) { if ( (this->l > s.r) || (this->r < s.l) ) return false; return true; };
		bool split(side s, vector<side> &sp) {
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
			//
			//    s:    |----------------------|
			// this:        |--------------|
			if ( (s.l <= this->l) && (s.r >= this->r) ) { sp.push_back(s); return true; }
			//
			//    s:    |-----------|
			// this:        |--------------|
			if ( (s.r >= this->l) && (s.l < this->l) )
			{
				sp.push_back(s);
				if (s.r < this->r) sp.push_back(side(s.r + 1, this->r));
				return true;
			}
			//
			//    s:                |-----------|
			// this:        |--------------|
			if ( (s.l <= this->r) && (s.r > this->r) )
			{
				sp.push_back(s);
				if (s.l > this->l) sp.push_back(side(this->l, s.l - 1));
				return true;
			}
			//
			//    s:                |-----|
			// this:        |--------------|
			if ( (s.l >= this->l) && (s.r <= this->r) )
			{
				sp.push_back(s);
				if (s.r < this->r) sp.push_back(side(s.r + 1, this->r));
				if (s.l > this->l) sp.push_back(side(this->l, s.l - 1));
				return true;
			}
			printf("INVALID case - not possible to get here.\n");
			return false;
		}
				
		int64_t l, r;
		int64_t length() { return (r - l + 1); };
		void out(const char *text = NULL) {
			if (!text) text = "";
			printf("%s[%5ld .. %5ld] ", text, l, r); };
};

class cube;


class cube {
	public:
		typedef enum {NEW, ACTIVE, ERASED} cube_state;
		void out(vector<cube> &c);
		cube() : x(0,0), y(0,0), z(0,0), state(NEW) {};
		cube(int64_t lx, int64_t rx, int64_t ly, 
			 int64_t ry, int64_t lz, int64_t rz) : x(lx, rx), y(ly, ry), z(lz, rz) { } ;
		cube(side _x, side _y, side _z) : x(_x), y(_y), z(_z) { };
		int64_t	size() { return x.length() * y.length() * z.length(); }
		bool intersect(cube c) {
			return 	x.intersect(c.x) &&
					y.intersect(c.y) &&
					z.intersect(c.z); };


		void out(const char *text = NULL)
		{
			if (!text) text = "Cube: ";
			printf("%s", text);
			x.out("X: "); y.out("Y: "); z.out("Z: ");
			printf("   Size: %20ld\n", size());
		}
		bool	split(cube s, vector<cube> &clist)
		{
			bool  rv = false;
			clist.clear();
			vector<side> nx, ny, nz;
			x.split(s.x, nx);
			y.split(s.y, ny);
			z.split(s.z, nz);
			for (size_t i = 0; i < nx.size(); i++)
			{
				for (size_t j = 0; j < ny.size(); j++)
				{
					for (size_t k = 0; k < nz.size(); k++)
					{
					    clist.push_back(cube(nx[i], ny[j], nz[k]));
					    rv = true;
					}
				}
			}
			if (rv)
			{
				//this->out();
				//s.out();
				//out(clist);
			}
			return rv;
		}
		bool	is_new() { return state == NEW; };
		bool	is_active() { return state == ACTIVE; };
		bool    is_erased() { return state == ERASED; };
		bool	ignore() { return state == ACTIVE; };
		void	set_erased() { state = ERASED; };
		void	set_active() { if (state != ERASED) state = ACTIVE; };
	private:
		side x, y, z;
		cube_state state;
};

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
		void out();
		int64_t	size();
		const cube *reset() { it = reboot.begin(); return &(*it); };
		const cube *next() { it++; if (it == reboot.end()) return NULL; else return &(*it);};
	private:
		bool handle(cube c, bool on);
		vector<cube>	reboot;
		vector<cube>::iterator it;
};

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
	int64_t ncs = 0;
	for (it = reboot.begin(); it != reboot.end(); it++)
	{
		if ((*it).is_erased()) continue;
		(*it).out();
		ncs += (*it).size();
	}
	printf("Number of lights: %ld\n", ncs);
}

bool	vcube::handle(cube c, bool on)
{
	bool rv = false;
	for (vector<cube>::iterator it = reboot.begin(); it != reboot.end(); it++)
	{
		if ((*it).is_active() && c.intersect(*it))
		{
			//printf("Intersects with "); (*it).out(); printf("\n");
			vector<cube>	ilist;
			(*it).split(c, ilist);
			(*it).set_erased();
			for (vector<cube>::iterator ilt = ilist.begin(); ilt != ilist.end(); ilt++)
			{
                if (on || !c.intersect(*ilt))  // any cubes that do not intersect with c are
				    reboot.push_back(*ilt);
				//(*ilt).out("Adding");
			}
			rv = true;
			break;
		}
	}
	if (!rv)
	{
		reboot.push_back(c);
		rv = true;
	}
	for (vector<cube>::iterator it = reboot.begin(); it != reboot.end(); it++) (*it).set_active();
	return rv;
}

bool	vcube::add(cube c)
{
	return handle(c, true);
}

//
// this function is called when a cubeset is turned off;
// in this case, intesecting cubes are created, (split) and
// those that are NOT in the cube c, are returned to the reboot
// object
bool	vcube::remove(cube c)
{
	return handle(c, false);
}

//on x=-31..21,y=-11..42,z=-4..49
void	run_reboot(const char *fname, int64_t max_abs, int64_t expected)
{
	FILE *f = fopen(fname, "r");
#define MAX_INS 1000
	char ins[MAX_INS];
	char *ip;
	vcube reboot;
	while (!feof(f))
	{
		fgets(ins, MAX_INS, f);
		if (feof(f)) break;
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
		if (abs(lx) > max_abs) continue;
		if (abs(rx) > max_abs) continue;
		if (abs(ly) > max_abs) continue;
		if (abs(ry) > max_abs) continue;
		if (abs(lz) > max_abs) continue;
		if (abs(rz) > max_abs) continue;
		printf("%s x=%ld..%ld,y=%ld..%ld,z=%ld..%ld\n", (on_off?"on":"off"),
			lx, rx, ly, ry, lz, rz);
		cube c(lx, rx, ly, ry, lz, rz);
		if (on_off) reboot.add(c);
		else reboot.remove(c);
	}
	reboot.out();
}

int main(int argc, char **argv)
{
	run_reboot(argv[1], 50, 590784);
	//run_reboot("data.txt", 50, 10000);
	return 1;
}
