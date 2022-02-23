#include <stdarg.h> // Used for var-args
#include <stdio.h>
#include <string.h>
#include <vector>
#include <math.h>
#include <stdlib.h>
#include <time.h>
/*        11
 12345678901
#############
#...........#
###D#A#A#D###
  #C#C#B#B#
  #########
 
*/

// location:  this is a number that describes either a room or a space (hallway)
//    if location <= 7, it is a room
//    if location >= 10, then location - 10 is the index into the space (hallway)

//
//
/*
   2 2   2   2   2   2 2 
   0 1   2   3   4   5 6 
 # # # # # # # # # # # # #
 # . .   .   .   .   . . #
 # # # 0 # 4 # 8 #12 # # # 
     # 1 # 5 # 9 #13 #
     # 2 # 6 #10 #14 #
     # 3 # 7 #11 #15 #
     # # # # # # # # #
 
*/

bool move(int f, int t);		// this function will move amphipod from position f to pos. t
								// it returns true if that is a possible move, false otherwise

typedef enum {
	Z_amph = -1, A_amph = 0, B_amph = 1, C_amph = 2, D_amph = 3 } amph_t;

amph_t	g_home[] = {A_amph, A_amph, A_amph, A_amph, B_amph, B_amph, B_amph, B_amph, 
					C_amph, C_amph, C_amph, C_amph, D_amph, D_amph, D_amph, D_amph};

char ACHR(amph_t a)
{
	switch (a)
	{
		case A_amph: return 'A';
		case B_amph: return 'B';
		case C_amph: return 'C';
		case D_amph: return 'D';
		case Z_amph: return '.';
	}
	return '?';
}

amph_t AMPH(char a)
{
	switch (a)
	{
		case 'A': return A_amph;
		case 'B': return B_amph;
		case 'C': return C_amph;
		case 'D': return D_amph;
	}
	return Z_amph;
}



amph_t AMP_TYPE(int n)
{
	if (n >= 100) n -= 100;
	switch (n)
	{
		case 0:
		case 1: 
		case 2:
		case 3: return A_amph;
		case 4: 
		case 5: 
		case 6: 
		case 7: return B_amph;
		case 8: 
		case 9: 
		case 10: 
		case 11: return C_amph;
		case 12: 
		case 13: 
		case 14: 
		case 15: return D_amph;
	}
	return Z_amph;
}


typedef struct _space {
	int		occupied;		// if <0, unoccupied, if >= 0, index into amphipod, but if >= 100 - amphipod is home
} space;	


typedef struct _amphipod {
	int		location; // if 0 <= location <= 7, room index, >= 20, space index is -20
	int		energy;
} amphipod;

typedef struct _move_s {
	int	from;
	int	to;
} move_t;

typedef std::vector<move_t> vm_t;
typedef std::vector<move_t>::iterator vm_t_i;

typedef struct burrow_s {
	amphipod	a[16];
	space		s[27];
	vm_t		v;
}burrow;

#define IX(r,c)	(4 * c + r)

class moves {
	public:
		moves(burrow &b);
		void clear() { vm.clear(); it = vm.begin(); };
		int	number() { return vm.size(); };
		int add(int f, int t) { move_t v; v.from = f; v.to = t; vm.push_back(v); it = vm.begin(); return number(); };
		bool first(move_t &m) { reset(); if (it != vm.end()) { m = *it; it++; return true; } return false; }
		bool next(move_t &m) { if (it == vm.end()) return false; m = *it; it++; return true; };
		bool reset() {it = vm.begin(); if (it != vm.end()) return true; else return false; };
		void out() { reset(); while (it != vm.end()) { printf("MOVES:: From: %2d  to  %2d\n", (*it).from, (*it).to); it++; }};

	private:
		vm_t vm;
		vm_t::iterator it;
};

typedef std::vector<move_t> vm_t;

#define TOP(n) (n  % 2 == 0)
#define TF(b)	((b)?"TRUE":"FALSE")


void dump(space *sp)
{
	printf("SPACES:\n");
	space *s = sp + 10;
	for (int i = 20; i < 27; i++, s++)
	{
		printf("  Index: %d   occupied: %d\n", i, s->occupied);
	}
	printf("ROOMS:\n");
	s = sp;
	for (int i = 0; i < 16; i++, s++)
	{
		printf("  Index: %d  type: %c   occupied: %d  TOP: %s\n", 
			i, ACHR(AMP_TYPE(i)), s->occupied, TF(TOP(i)));
	}
}

void dump(amphipod *a, int n)
{
	printf("AMPHIPODS:\n");
	for (int i = 0; i < n; i++, a++)
	{
		printf("  Index: %d  type: %c   location: %d   Energy: %d\n", 
			i, ACHR(AMP_TYPE(i)), a->location, a->energy);
	}
}

void dump_b(burrow &b)
{
	dump(b.a, 16);
	dump(b.s);
}
	

void init_space(space *s, int *ix)
{
	for (int i = 0; i <  16; i++) s[i].occupied = *ix++;
	for (int i = 16; i < 27; i++) s[i].occupied = -1;
}

int	UNITS(amph_t a)
{
	switch (a)
	{
		case A_amph: return 1;
		case B_amph: return 10;
		case C_amph: return 100;
		case D_amph: return 1000;
		case Z_amph: return -1;
	}
	return -1;
}


void	i_amph(amphipod &a, int location)
{
	a.location = location;
	a.energy = 0;
}

//
// c[] is an array of amphipod types, but, it is not indexec
// the same as the rooms:
//     0 1 2 3  \     0 2 4 6 
//     4 5 6 7	/  	  1 3 5 7
//
//     if (2 * n <= 6 then 2 * n is the index
//     else index is 2 * n - 7
//
//  order[k] means room k contains this amphipod (an index int amphipod array)
//
void	init_amph(amphipod *a, char *chrs, int *order)
{
	int abcd[] = {0, 4, 8, 12};
	for (int i = 0; i < 16; i++)
	{
		int j = (int) AMPH(chrs[i]);	// this is a number 0 thru 3
		int o_index = abcd[j];	// a number from 0 thru 15 (A's are 0-3, B's 4-7, etc.)
		abcd[j]++;
		order[i] = o_index;  	// order is an array that will be used to set the 
								// rooms to point to their initial amphipod
		//printf("i=%d j=%d o_index=%d\n", i, j, o_index);
		i_amph(a[o_index], i);
	}

}

int	count_home(burrow &b)
{
	space *s = b.s;
	int	cnt = 0;
	// check to see if they are initially 'home'
	for (int i = 0; i < 16; i++)
	{
		int	at = s[i].occupied;
		if (at > 99) cnt++;
	}
	return cnt;
}


//char	room_char(space &r, amphipod *a)
//{
//	if (r.occupied < 0) return '.';
//	return ACHR(AMP_TYPE(r.occupied));
//}


char	occ_char(burrow &b, int n)
{
	int nv = b.s[n].occupied;
	if (nv < 0) return '.';
	int lc = 0;	// if the amphipod is 'home' we'll make his letter lower case
	if (nv > 99){
		 lc = 32;
		 nv -= 100;
	 }
	//printf("lc: %d   %c\n", lc, (int)'B' + lc);
	return ACHR(AMP_TYPE(nv)) + lc;
}

int		amph_energy(amphipod *a)
{
	int i;
	int	en = 0;
	for (i = 0; i <= 15; i++)
	    en += a[i].energy;
	return en;
}

int		energy(burrow &b)
{
	return amph_energy(b.a);
}

void	out_burrow(burrow &b)
{
	int cnt;
/*
#############
#...........#
###D#A#A#D###
  #C#C#B#B#
  #########
*/
	time_t t = time(0);
	printf("Time: %s\n", ctime(&t));
#define CH(n)		occ_char(b, n)
	printf("#############\n");
	printf("#%c%c.%c.%c.%c.%c%c#\n",
		CH(20), CH(21), CH(22), CH(23), CH(24), CH(25), CH(26));

#define RM(n, m)	occ_char(b, 4 * m + n)
	printf("###%c#%c#%c#%c###\n",
		RM(0,0), RM(0,1), RM(0,2), RM(0,3));
	printf("###%c#%c#%c#%c###\n",
		RM(1,0), RM(1,1), RM(1,2), RM(1,3));
	printf("###%c#%c#%c#%c###\n",
		RM(2,0), RM(2,1), RM(2,2), RM(2,3));
	printf("###%c#%c#%c#%c###\n",
		RM(3,0), RM(3,1), RM(3,2), RM(3,3));
	printf("  #########\n");
	printf("Energy: %d\n", amph_energy(b.a));
	cnt = count_home(b);
	printf("Count in Correct room: %d\n\n", cnt);
	for (vm_t_i it = b.v.begin(); it != b.v.end(); it++)
	{
		printf("do_move(%d, %d);\n", it->from, it->to);
	}
}


int	count(burrow &b)
{
	int cnt = 0;
	for (int i = 0; i < 16; i++) if (b.s[i].occupied > 99) cnt++;
	return cnt;
}

void	reset(burrow &b, char *ch)
{
	int	order[16];
	init_amph(b.a, ch, order);
	// check if 'order' has elements in the correct place
	int lix = 0;
	int hix = 3;
	for (int col = 0; col < 4; col++)
	{
		int	ix = 4 * col;
		for (int row = 3; row >= 0; row--)
		{
			if ( (lix <= order[ix + row]  &&  (order[ix + row]) <= hix) )
			    order[ix + row] += 100;
			else
			    break;
		}
		lix += 4;
		hix += 4;
	}
	//for (int i = 0; i < 16; i++) printf("order[%d] = %d\n", i, order[i]);
	init_space(b.s, order);
}


#define OK(t) ((t)?"OK":"FAIL")					


/*
# # # # # # # # # # # # #
# 0 1 - 2 - 3 - 4 - 5 6 #
# # # 0 # 2 # 4 # 6 # # #
    # 1 # 3 # 5 # 7 #
    # # # # # # # # #
#define RFALSE	{ printf("Returnning false at line %d\n", __LINE__); return false; }
*/
#define RFALSE return false

// this function will check the path from hallway position "from_h" to hallway position
// "to_h"   
bool hall_path(burrow &b, int from_h, int to_h)
{
	//printf("...hall_path  from_h: %d   to_h: %d\n", from_h, to_h);
	bool	hallpath = true;

	for (int i = from_h; i <= to_h; i++)
	{
		int	gsio = b.s[i].occupied;
		hallpath = hallpath && (gsio < 0);
		//if (gsio >= 0) printf("gsio = %d (i: %d)\n", gsio, i);
	}
	//if (!hallpath) printf("ERROR - hallpath %d - %d\n", from_h, to_h);
	return hallpath;
}
//
// room_path includes hallway traverses
//
bool room_path(burrow &b, int from_room, int to_room)
{
	int		fcol = from_room / 4;
	int		frow = from_room % 4;
	int		tcol = to_room / 4;
	int		trow = to_room % 4;
	
	if (frow == 0)	// nothing to worry about
	{
	}
	if (frow >= 1) // 0 needs to be empty
	{
		if (b.s[fcol * 4 + 0].occupied > 0) RFALSE;
	}
	if (frow >= 2) // 0, 1 needs to be empty
	{
		if (b.s[fcol * 4 + 1].occupied > 0) RFALSE;
	}
	if (frow >= 3)	// 0, 1, 2 needs to be empty
	{
		if (b.s[fcol * 4 + 2].occupied > 0) RFALSE;
	}
	
	// if we get here - the from rooms are clear
	// now we check the to rooms

	if (trow == 0)	// nothing to worry about
	{
	}
	if (trow >= 1) // 0 needs to be empty
	{
		if (b.s[tcol * 4 + 0].occupied > 0) RFALSE;
	}
	if (trow >= 2) // 0, 1 needs to be empty
	{
		if (b.s[tcol * 4 + 1].occupied > 0) RFALSE;
	}
	if (trow >= 3)	// 0, 1, 2 needs to be empty
	{
		if (b.s[tcol * 4 + 2].occupied > 0) RFALSE;
	}
	
	//
	// if we get here, the room paths for from and to are 
	// clear - we just need to make sure the hall paths are opened
	int	hs = (fcol > tcol) ? tcol : fcol;
	int he = (fcol < tcol) ? tcol : fcol;
	// return false is the hallway is blocked
	for (int i = hs; i < he; i++)
	{
		//printf("From: %d (%d,%d)   To: %d (%d,%d)   hs: %d  he: %d\n", from_room, frow, fcol, to_room, trow, tcol, hs, he);
	    if (b.s[i + 22].occupied >= 0) RFALSE;
	}
	
	return true;	// if we get here - we are clear
}


//
// it is assumed that there is an amphipod at 'f' and we are trying to move
// it to 't'
bool valid(burrow &b, int f, int t, bool debug = false)
{
	// check for invalid from/to requests 16 thru 19 are invalid locations
	if ( ( (f >= 16) && (f <= 19) ) ||
	     ( (t >= 16) && (t <= 19) ) ) RFALSE;
	// make sure that there is an amphipod at f and NOT at t
	if (b.s[t].occupied >= 0) RFALSE;
	if (b.s[f].occupied < 0) RFALSE;
	int	trow = t % 4;
	int tcol = t / 4;
	int	frow = f % 4;
	int fcol = f / 4;
	
	// check that the to is valid - from type 
	// and that the cells below are 'done'
	if (t < 19)
	{
		amph_t ft = AMP_TYPE(b.s[f].occupied);
		if (ft != AMP_TYPE(t)) RFALSE;	// if destination type is not the from type - return false

		// it trow is NOT 3, we need to make sure the cells below are 'done'
		
		if (trow == 3)	// nothing to be done
		{
			
		}
		if (trow <= 2) // 3 needs to be 'done'
		{
			if (b.s[tcol * 4 + 3].occupied < 100) RFALSE; 
		}
		if (trow <= 1) // 2, 3 needs to be 'done'
		{
			if (b.s[tcol * 4 + 2].occupied < 100) RFALSE;
		}
		if (trow == 0)	// 1, 2, 3 needs to be 'done'
		{
			if (b.s[tcol * 4 + 1].occupied < 100) RFALSE;
		}

	}
	




	     
	// going from one romm to another room
	if ( f < 19  &&  t < 19 ) return room_path(b, f, t);

	// we are leaving a room for the hallway
	if ( f < 19  &&  t > 19 ) 
	{
		// if room is not a top room (frow > 0), make sure the above rooms are not occupied
		for (int j = 0; j < frow; j++)
			if (b.s[fcol * 4 + j].occupied >= 0) RFALSE; // return false if above room occupied

		if ( (fcol == 0) )
		{
			if (t > 21) return hall_path(b, 22, t);
			else return hall_path(b, t, 21);
		}
		else if ( fcol == 1 )
		{
			if (t > 22) return hall_path(b, 23, t);
			else return hall_path(b, t, 22);
		}
		else if ( fcol == 2 )
		{
			if (t > 23) return hall_path(b, 24, t);
			else return hall_path(b, t, 23);
		}
		else if ( fcol == 3 )
		{
			if (t > 24) return hall_path(b, 25, t);
			else return hall_path(b, t, 24);
		}
	}
	// return to a room
	if (f > 19 && t < 19)
	{
		// if to trow > 0, make sure all of the rooms are vacant
		if (trow > 0)	// above room must be vacant
		{
			for (int j = 0; j < trow; j++)
				if (b.s[tcol * 4 + j].occupied >= 0) RFALSE; // return false if above room occupied
		}


		if ( tcol == 0) 
		{
			if (f > 21) return hall_path(b, 22, f - 1);
			else return hall_path(b, f + 1, 21);
		}
		else if ( tcol == 1) 
		{
			if (f > 22) return hall_path(b, 23, f - 1);
			else return hall_path(b, f + 1, 22);
		}
		else if ( tcol == 2) 
		{
			if (f > 23) return hall_path(b, 24, f - 1);
			else return hall_path(b, f + 1, 23);
		}
		else if ( tcol == 3) 
		{
			if (f > 24) return hall_path(b, 25, f - 1);
			else return hall_path(b, f + 1, 24);
		}	
	}
	//printf("ERROR - CANNOT GET HERE!!\n");
	RFALSE;
}

int R2R_VIA_HALLWAY(int n)
{
	switch(n)
	{
		case 1: return 3;
		case 2: return 5;
		case 3: return 7;
	}
	return 99999;
}

int C2H(int c, int h)
{
	static int hw[4][7] = { 
		{3, 2, 2, 4, 6, 8, 9},
		{5, 4, 2, 2, 4, 6, 7},
		{7, 6, 4, 2, 2, 4, 5},
		{9, 8, 6, 4, 2, 2, 3}
		};
	//printf("c: %d   h: %d   hw: %d\n", c, h, hw[c][h-20]);

	return hw[c][h-20];
}
	

int	steps(int f, int t)
{
	int	fcol = f / 4;
	int frow = f % 4;
	int	tcol = t / 4;
	int trow = t % 4;

	int n = 0;	// step counter
	
	if ( t < 16 && f < 16)
	{
		n = frow + trow + 1;
		n += R2R_VIA_HALLWAY(fabs(tcol - fcol));
	}
	
	else if (t > 16 )
	{
		n = frow;
		n += C2H(fcol, t);
	}
	else // f < 16
	{
		n = trow;
		n += C2H(tcol, f);
	}

	return n;
}


// this function will move amphipod from position f to pos. t
// it returns false if the move requested is not possible
bool move(burrow &b, int f, int t)	
{
	//printf("\nMOVING from %d to %d\n", f, t);
	if (!valid(b, f, t))
	{
		//printf("^MOVE: %d to %d - ERROR\n", f, t);
		//out_burrow(b);
		return false;
	}
	if (t < 19)	// we're moving the amphipod home
	{
		if (f < 19)  // room-to-room amphipod move
		{
			int ri = b.s[f].occupied;	// ri is the index of the amphipod
			
			// check if this is the correct room type for the amphipod
			// 
			if (AMP_TYPE(ri) != g_home[t])
			{
				//printf("Cannot move amphipod into room %d\n", t);
				RFALSE;	// cannot move to this room - it's not his home
			}
			b.s[f].occupied = -1; // now unoccupied
			b.s[t].occupied = ri + 100; // [to] now occupied
			b.a[ri].location = t;	// add 100 to location to indicate it is HOME!
			int num_steps = steps(f, t); // number of steps from f to t
			//printf("f = %d   t: %d  ri:: %d  dist: %d units: %d\n", 
			//	f, t, ri, num_steps, UNITS((amph_t)(ri/4)));
			b.a[ri].energy += UNITS((amph_t)(ri/4)) * num_steps;
			//printf("[room-to-room] MOVE: %c at %d to %d\n", ACHR(ga[ri].type), f, t);
			//out_burrow(gb);
			return true;
		}
		else   // move from hallway to room
		{
			int ri = b.s[f].occupied;	// ri is the index of the amphipod
			if (ri < 0)
			{
				printf("ERROR - no amphiod at hallway location: %d\n", ri);
				return false;
			}
			b.s[f].occupied = -1; // now unoccupied
			b.s[t].occupied = ri + 100; // to now occupied and HOME
			b.a[ri].location = t; // set amphipod location
			int num_steps = steps(f, t); // gr[f].dist[t-10];
			//printf("f = %d   t: %d   ri: %d  dist: %d units: %d\n", 
			//	f, t, ri, num_steps, UNITS((amph_t)(ri/4)));
			b.a[ri].energy += UNITS((amph_t)(ri/4)) * num_steps;
			//printf("-MOVE: %c at %d to %d\n", ACHR(ga[ri].type), f, t);
			//out_burrow(gb);
			return true;
		}
	}
	else  // t > 9, f must be < 9
	{
		int ri = b.s[f].occupied;
		b.s[f].occupied = -1; // now unoccupied
		b.s[t].occupied = ri;
		b.a[ri].location = t;
		int num_steps = steps(f, t); // gr[f].dist[t-10];
		//printf("f = %d   t-10: %d   dist: %d\n", f, t-10, num_steps);
		b.a[ri].energy += UNITS((amph_t)(ri/4)) * num_steps;
		//printf("f = %d   t: %d   ri: %d  dist: %d units: %d\n", 
		//		f, t, ri, num_steps, UNITS((amph_t)(ri/4)));
		//printf("+MOVE: %c at %d to %d\n", ACHR(ga[ri].type), f, t);
		//out_burrow(gb);
		return true;
	}
	printf("XMOVE: %d to %d - ERROR\n", f, t);
	return false;
}


int	can_move(burrow &b, int f, int t)
{
	if (b.s[f].occupied < 0) return -1;
	if (b.s[f].occupied > 99) return -1;
	if (valid(b, f, t)) return t;
	return -1;
}

int get_moves(burrow &b, vm_t &v, bool debug = false)
{
	v.clear();
	for (int a = 0; a < 16; a++)
	{
		int from = b.a[a].location;
		if (from > 99) continue;
		for (int j = 0; j < 27; j++)
		{
			int to = can_move(b, from, j);
			if (debug) printf("{Y} GET_MOVES:: amp: %d  loc: %d   to: %d (%d)\n",
				a, from, to, j);
			if (to >= 0)
			{
				move_t m; m.from = from; m.to = to;
				v.push_back(m);
			}
		}
	}
	return v.size();
}

moves::moves(burrow &b)
{
	get_moves(b, b.v, false);
	reset();
}

burrow min_b;
int	   min_score = 999999999;

bool	recurse(burrow b)
{
	if (count(b) == 16) //(b.done())
	{
		if (energy(b) < min_score)
		{
			min_score = energy(b);
			min_b = b;
			out_burrow(b);
		}
		return true;
	}
	vm_t	mvs;
	get_moves(b, mvs, false);
	vm_t_i	it = mvs.begin();
	move_t nm;
	//m.reset();
	//bool v = m.first(nm);
	burrow c = b;
	while(it != mvs.end())
	{
		nm = *it;
		b = c;
		move(b, nm.from, nm.to);
		//printf("RECURSE: moving %d to %d  %s\n", nm.from, nm.to, TF(bm));
		//out_burrow(b);
		b.v.push_back(nm);
		//out_burrow(b);
		recurse(b);
		it++;
	}
	//printf("NO MOVES:\n");
	//out_burrow(b);
	return false;
}








void	r_init(const char *fn, int n)
{
	FILE *f = fopen(fn, "r");
	if (!f) return;
	char	ch[18];
	int		inch;
	burrow	gb;
	int		row = 0;
	int     col = 0;
	int     index = 0;

	while (!feof(f))
	{
		inch = fgetc(f);
		index = col * 4 + row;
		if (inch == 'A' || inch == 'B' || inch == 'C' || inch == 'D')
		{
			//printf("Index: %d  Reorder: %d  Letter: %c\n", chc, reorder[chc], inch);
		    ch[index] = inch;
		    col++;
		    if (col >= 4)
		    {
				row ++;
				col = 0;
			}
		}
	}
	reset(gb, ch);
	printf("Initial input: \n");
	out_burrow(gb);
	recurse(gb); 
	printf("After recurse\n");
}
void ixx(burrow bb)
{
#define do_move(n, m)	printf("do_move(%d,%d)\n", n,m); move(bb, n, m); out_burrow(bb);
do_move(12,26);
do_move(13,20)
do_move(8,25)
do_move(9,24)
do_move(10,21)
do_move(4,10)
do_move(5, 9)
do_move(6,23)
do_move(7,22)
do_move(23,7)
do_move(24,6)
do_move(25,5)
do_move(14,8)
do_move(15,25)
do_move(22,15)
do_move(0,4)
do_move(1, 14)
do_move(2,22)
do_move(21,2)
do_move(20,1)
do_move(22,13)
do_move(25,0)
do_move(26,12)
dump(bb.a, 16);

}	

	
/*
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
*/
int	main(int argc, char **argv)
{
	r_init("part2.txt", 1);
/*
 	for (int i = 0; i < 16; i++)
	{
		for (int j = 20; j < 27; j++)
		{
			printf("From %d  to  %d   dist: %d\n", i, j, steps(i, j));
			printf("From %d  to  %d   dist: %d\n", j, i, steps(j, i));
		}
	}
*/
}


