#include <stdarg.h> // Used for var-args
#include <stdio.h>
#include <string.h>
#include <vector>
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
   1 1   1   1   1   1 1 
   0 1   2   3   4   5 6 
 # # # # # # # # # # # # #
 # . .   .   .   .   . . #
 # # # 0 # 2 # 4 # 6 # # # 
     # 1 # 3 # 5 # 7 #
     # # # # # # # # #
 
*/

bool move(int f, int t);		// this function will move amphipod from position f to pos. t
								// it returns true if that is a possible move, false otherwise
bool back(int f);				// this function will return an amphipod to its 'home' room
								// it returns true if it can return home, or false if it can't

typedef enum {
	Z_amph = -1, A_amph = 0, B_amph = 1, C_amph = 2, D_amph = 3 } amph_t;

amph_t	g_home[] = {A_amph, A_amph, B_amph, B_amph, C_amph, C_amph, D_amph, D_amph};

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
		case 1: return A_amph;
		case 2:
		case 3: return B_amph;
		case 4: 
		case 5: return C_amph;
		case 6: 
		case 7: return D_amph;
	}
	return Z_amph;
}


typedef struct _space {
	int		occupied;		// if <0, unoccupied, if >= 0, index into amphipod, but if >= 100 - amphipod is home
} space;	


typedef struct _amphipod {
	int		location; // if 0 <= location <= 7, room index, >= 10, space index is -10
	int		energy;
} amphipod;

typedef struct _move_s {
	int	from;
	int	to;
} move_t;

typedef std::vector<move_t> vm_t;
typedef std::vector<move_t>::iterator vm_t_i;

typedef struct burrow_s {
	amphipod	a[8];
	space		s[17];
	vm_t		v;
}burrow;


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
	for (int i = 10; i < 17; i++, s++)
	{
		printf("  Index: %d   occupied: %d\n", i, s->occupied);
	}
	printf("ROOMS:\n");
	s = sp;
	for (int i = 0; i < 8; i++, s++)
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

void init_space(space *s, int *ix)
{
	for (int i = 0; i <  8; i++) s[i].occupied = *ix++;
	for (int i = 8; i < 17; i++) s[i].occupied = -1;
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


void	i_amph(amphipod &a, int location, amph_t at)
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
	bool abcd[] = {false, false, false, false};
	for (int i = 0; i <= 7; i++)
	{
		int j = (int) AMPH(chrs[i]);	// this is a number 0 thru 3
		int o_index = 2 * j + (abcd[j] ? 1 : 0);
		abcd[j] = true;
		order[i] = o_index;  	// order is an array that will be used to set the 
								// rooms to point to their initial amphipod
		//printf("i=%d j=%d o_index=%d\n", i, j, o_index);
		i_amph(a[o_index], i, AMPH(chrs[i]));
	}
}

bool	i_check(amphipod *a, space *r, int &cnt)
{
	int i;
	cnt = 0;
	bool done[8] = {false, false, false, false, false, false, false, false};
	for (i = 1; i <= 7; i+=2) // check lower rooms first
	{
		int ri = r[i].occupied;
		if (AMP_TYPE(ri) == AMP_TYPE(i)) done[i] = true;
		//printf("i: %d  ri: %d   type(i): %c   type(ri): %c   STATE: %s\n",
		//	i, ri, ACHR(AMP_TYPE(i)), ACHR(AMP_TYPE(ri)), TF(done[i]));
	}
	for (i = 0; i <= 7; i+=2) // check upper rooms next
	{
		int rt = r[i].occupied;	// upper room
		//int rb = r[i+1].occupied;	// lower room
		if ( (AMP_TYPE(rt) == AMP_TYPE(i)) && done[i+1]) done[i] = true;
		//printf("i: %d  rt: %d    rb: %d   type(i): %c   type(rt): %c   STATE: %s\n",
		//	i, rt, rb, ACHR(AMP_TYPE(i)), ACHR(AMP_TYPE(rt)), TF(done[i]));
	}
	bool rv = true;

	for (i = 0; i <= 7; i++) { rv = rv && done[i]; cnt += (done[i]?1:0); }
	return rv;
}

//char	room_char(space &r, amphipod *a)
//{
//	if (r.occupied < 0) return '.';
//	return ACHR(AMP_TYPE(r.occupied));
//}


char	occ_char(burrow &b, int n)
{
	if (b.s[n].occupied < 0) return '.';
	return ACHR(AMP_TYPE(b.s[n].occupied));
}

int		amph_energy(amphipod *a)
{
	int i;
	int	en = 0;
	for (i = 0; i <= 7; i++)
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
		CH(10), CH(11), CH(12), CH(13), CH(14), CH(15), CH(16));
		
#define RM(n, m)	occ_char(b, 2 * m + n)
	printf("###%c#%c#%c#%c###\n",
		RM(0,0), RM(0,1), RM(0,2), RM(0,3));
	printf("###%c#%c#%c#%c###\n",
		RM(1,0), RM(1,1), RM(1,2), RM(1,3));
	printf("  #########\n");
	printf("Energy: %d\n", amph_energy(b.a));
	i_check(b.a, b.s, cnt);
	printf("Count in Correct room: %d\n\n", cnt);
	for (vm_t_i it = b.v.begin(); it != b.v.end(); it++)
	{
		printf("do_move(%d, %d);\n", it->from, it->to);
	}
}

int	init_check(amphipod *a, space *s)
{
	int i;
	int cnt = 0;
	for (i = 1; i <= 7; i+=2) // check lower rooms first
	{
		int ri = s[i].occupied;
		if (AMP_TYPE(ri) == AMP_TYPE(i)) {cnt++; a[ri].location += 100; s[i].occupied += 100; }// mark as in final home
	}
	for (i = 0; i <= 7; i+=2) // check upper rooms next
	{
		int rt = s[i].occupied;	// upper room
		if ( (AMP_TYPE(rt) == AMP_TYPE(i)) && s[i+1].occupied > 99) {cnt++; a[rt].location += 100; s[i].occupied += 100;}
	}
	return cnt;
}

int	count(burrow &b)
{
	int cnt = 0;
	for (int i = 0; i < 8; i++) if (b.s[i].occupied > 99) cnt++;
	return cnt;
}

void	reset(burrow &b, char *ch)
{
	int	order[8];
	init_amph(b.a, ch, order);
	init_space(b.s, order);
	init_check(b.a, b.s);
}


#define OK(t) ((t)?"OK":"FAIL")					


/*
# # # # # # # # # # # # #
# 0 1 - 2 - 3 - 4 - 5 6 #
# # # 0 # 2 # 4 # 6 # # #
    # 1 # 3 # 5 # 7 #
    # # # # # # # # #
*/

// this function will check the path from hallway position "from_h" to hallway position
// "to_h"   
bool hall_path(burrow &b, int from_h, int to_h)
{
	//printf("...hall_path  from_h: %d   to_h: %d\n", from_h, to_h);
	bool	hallpath = true;
	//if (from_h >= to_h) return true;	// special case where no spaces can be filled in the path
	//from_h -= 10;
	//to_h -= 10;


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
	bool	roompath = true;
	int		hs, he;
	if (from_room > to_room)
	{
		hs = to_room / 2;		// 0,1 -> 0  2,3 -> 1  4,5 -> 2  6,7 -> 3
		he = from_room / 2 - 1;
	}
	else
	{
		hs = from_room / 2;		// 0,1 -> 0  2,3 -> 1  4,5 -> 2  6,7 -> 3
		he = to_room / 2 - 1;
	}
	
	
	if ( (from_room < 8) && (from_room % 2 == 1) )	// above room must be vacant
	{
		if (b.s[from_room - 1].occupied >= 0) 
		{
			//printf("ERROR - previous room not vacant: f: %d  t: %d\n", from_room, to_room);
			return false; // return false if above room occupied
		}
	}
	// return false is the hallway is blocked
	bool hallpath = true;
	for (int i = hs; i <= he; i++)
	    hallpath = hallpath && b.s[i + 12].occupied < 0;

	if (!hallpath)
	{
		//printf("ERROR - hallpath occupied: hs: %d  he: %d\n", hs, he);
		//for (int i = hs; i <= he; i++)
	    //    printf("%d : %s\n", i + 2, TF(gb.s[i + 2].occupied < 0));
		return false;
	}
	
	// room path
	if (to_room <= 3)
	{
		roompath = b.s[2].occupied < 0;
		if (to_room == 3) roompath = roompath && b.s[3].occupied < 0;
	}
	else if (to_room <= 5)
	{
		roompath = b.s[4].occupied < 0;
		if (to_room == 5) roompath = b.s[5].occupied < 0;
	}
	else if (to_room <= 7)
	{
		roompath = roompath && b.s[6].occupied < 0;
		if (to_room == 7) roompath = roompath && b.s[7].occupied < 0;
	}
	//if (!roompath)
	//	printf("ERROR - roompath occupied: f: %d  t: %d\n", from_room, to_room);
	return roompath;
}

//
// it is assumed that there is an amphipod at 'f' and we are trying to move
// it to 't'
bool valid(burrow &b, int f, int t, bool debug = false)
{
	// check for invalid from/to requests
	if ( (f == 8) || (f == 9) ||
	     (t == 8) || (t == 9) ) return false;
	// make sure that there is an amphipod at f and NOT at t
	if (b.s[t].occupied >= 0) return false;
	if (b.s[f].occupied < 0) return false;
	
	// check that the to is valid - from type 
	if (t < 9)
	{
		amph_t ft = AMP_TYPE(b.s[f].occupied);
		if (ft != AMP_TYPE(t)) return false;	// if destination type is not the from type - return false
		if (t % 2 == 0)							// if wanting to go to top room, bottom room 
		{
			if (b.s[t+1].occupied  < 9) return false;	// we can't go to the top room if the bottom room is not 'done'
		}
	}
	
	     
	// going from one romm to another room
	if ( f < 9  &&  t < 9 ) return room_path(b, f, t);

	// we are leaving a room for the hallway
	if ( f < 9  &&  t > 9 ) 
	{
		// if room is odd, make sure above room is not occupied
		if (f % 2 == 1)	// above room must be vacant
		{
			if (b.s[f - 1].occupied >= 0)
			{
				//printf("ERROR - Odd room occupied: f: %d  t: %d\n", f, t);
				return false; // return false if above room occupied
			}
		}

		if ( (f == 0) || (f == 1) )
		{
			if (t > 11) return hall_path(b, 12, t);
			else return hall_path(b, t, 11);
		}
		else if ( (f == 2) || (f == 3) )
		{
			if (t > 12) return hall_path(b, 13, t);
			else return hall_path(b, t, 12);
		}
		else if ( (f == 4) || (f == 5) )
		{
			if (t > 13) return hall_path(b, 14, t);
			else return hall_path(b, t, 13);
		}
		else if ( (f == 6) || (f == 7) )
		{
			if (t > 14) return hall_path(b, 15, t);
			else return hall_path(b, t, 14);
		}
	}
	// return to a room
	if (f > 9 && t < 9)
	{
		// if to room is odd, make sure above room is not occupied
		if (t % 2 == 1)	// above room must be vacant
		{
			if (b.s[t - 1].occupied >= 0)
			{
				//printf("ERROR - above room is occupied for RR: f: %d  t: %d\n", f, t);
				return false; // return false if above room occupied
			}
		}


		if ( (t == 0) || (t == 1) )
		{
			if (f > 11) return hall_path(b, 12, f - 1);
			else return hall_path(b, f + 1, 11);
		}
		else if ( (t == 2) || (t == 3) )
		{
			if (f > 12) return hall_path(b, 13, f - 1);
			else return hall_path(b, f + 1, 12);
		}
		else if ( (t == 4) || (t == 5) )
		{
			if (f > 13) return hall_path(b, 14, f - 1);
			else return hall_path(b, f + 1, 13);
		}
		else if ( (t == 6) || (t == 7) )
		{
			if (f > 14) return hall_path(b, 15, f - 1);
			else return hall_path(b, f + 1, 14);
		}	
	}
	//printf("ERROR - CANNOT GET HERE!!\n");
	return false;
}

int	steps(int f, int t)
{
	static const int from[17][17] = {
//	              0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
/*  0 */		{ 0, 1, 4, 5, 6, 7, 8, 9,-1,-1, 3, 2, 2, 4, 6, 8, 9},  // from 0 to ..
/*  1 */		{ 1, 0, 5, 6, 7, 8, 9,10,-1,-1, 4, 3, 3, 5, 7, 9,10},  // from 1 to ..
/*  2 */		{ 4, 5, 0, 1, 4, 5, 6, 7,-1,-1, 5, 4, 2, 2, 4, 6, 7},  // from 2 to ..	
/*  3 */		{ 5, 6, 1, 0, 5, 6, 7, 8,-1,-1, 6, 5, 3, 3, 5, 7, 8},  // from 3 to ..
/*  4 */		{ 6, 7, 4, 5, 0, 1, 4, 5,-1,-1, 7, 6, 4, 2, 2, 4, 5},  // from 4 to ..	
/*  5 */		{ 7, 8, 5, 6, 1, 0, 5, 6,-1,-1, 8, 7, 5, 3, 3, 5, 6},  // from 5 to ..
/*  6 */		{ 8, 9, 6, 7, 4, 5, 0, 1,-1,-1, 9, 8, 6, 4, 2, 2, 3},  // from 6 to ..
/*  7 */        { 9,10, 7, 8, 5, 6, 1, 0,-1,-1,10, 9, 7, 5, 3, 3, 4},  // from 7 to ..
/*  8 */		{-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},  // DOES NOT EXIST
/*  9 */		{-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},  // DOES NOT EXIST
/* 10 */		{ 3, 4, 5, 6, 7, 8, 9,10,-1,-1, 0, 1, 3, 5, 7, 9,10},
/* 11 */		{ 2, 3, 4, 5, 6, 7, 8, 9,-1,-1, 1, 0, 2, 4, 6, 8, 9},
/* 12 */		{ 2, 3, 2, 3, 4, 5, 6, 7,-1,-1, 3, 2, 0, 2, 4, 6, 7},
/* 13 */		{ 4, 5, 2, 3, 2, 3, 4, 5,-1,-1, 5, 4, 2, 0, 2, 4, 5},
/* 14 */		{ 6, 7, 4, 5, 2, 3, 2, 3,-1,-1, 7, 6, 4, 2, 0, 2, 3},
/* 15 */		{ 8, 9, 6, 7, 4, 5, 2, 3,-1,-1, 9, 8, 6, 4, 2, 0, 1},
/* 16 */		{ 9,10, 7, 8, 5, 6, 3, 4,-1,-1,10, 9, 7, 5, 3, 1, 0}
};
/*  TEST for symmetry
  	for (int i = 0; i < 17; i++)
	   for (int j = 0; j < 17; j++)
	   {
		   if (from[i][j] != from[j][i])
		   {
			   printf("NOT symmetric at [%d][%d]   values ar %d and %d\n", 
				i, j, from[i][j], from[j][i]);
			}
		}
*/
	return from[f][t];
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
	if (t < 10)	// we're moving the amphipod home
	{
		if (f < 10)  // room-to-room amphipod move
		{
			int ri = b.s[f].occupied;	// ri is the index of the amphipod
			
			// check if this is the correct room type for the amphipod
			// 
			if (AMP_TYPE(ri) != g_home[t])
			{
				//printf("Cannot move amphipod into room %d\n", t);
				return false;	// cannot move to this room - it's not his home
			}
			b.s[f].occupied = -1; // now unoccupied
			b.s[t].occupied = ri + 100; // [to] now occupied
			b.a[ri].location = t + 100;	// add 100 to location to indicate it is HOME!
			int num_steps = steps(f, t); // number of steps from f to t
			//printf("f = %d   t-10: %d   dist: %d\n", f, t-10, num_steps);
			b.a[ri].energy += UNITS((amph_t)(ri/2)) * num_steps;
			//printf("[room-to-room] MOVE: %c at %d to %d\n", ACHR(ga[ri].type), f, t);
			//out_burrow(gb);
			return true;
		}
		else   // move from hallway to room
		{
			int ri = b.s[f].occupied;	// ri is the index of the amphipod
			if (ri < 0)
			{
				//printf("ERROR - no amphiod at hallway location: %d\n", ri);
				return false;
			}
			b.s[f].occupied = -1; // [to] now occupied
			b.a[ri].location = t + 100;
			b.s[t].occupied = ri + 100;
			int num_steps = steps(f, t); // gr[f].dist[t-10];
			//printf("f = %d   t-10: %d   dist: %d\n", f, t-10, num_steps);
			b.a[ri].energy += UNITS((amph_t)(ri/2)) * num_steps;
			//printf("-MOVE: %c at %d to %d\n", ACHR(ga[ri].type), f, t);
			//out_burrow(gb);
			return true;
		}
	}
	else if (valid(b, f, t))  // t > 9, f must be < 9
	{
		int ri = b.s[f].occupied;
		b.s[f].occupied = -1; // now unoccupied
		b.s[t].occupied = ri;
		b.a[ri].location = t;
		int num_steps = steps(f, t); // gr[f].dist[t-10];
		//printf("f = %d   t-10: %d   dist: %d\n", f, t-10, num_steps);
		b.a[ri].energy += UNITS((amph_t)(ri/2)) * num_steps;
		//printf("+MOVE: %c at %d to %d\n", ACHR(ga[ri].type), f, t);
		//out_burrow(gb);
		return true;
	}
	//printf("XMOVE: %d to %d - ERROR\n", f, t);
	return false;
}
								
// this function will return an amphipod to its 'home' room
// it returns true if it can return home, or false if it can't
bool back(int f)		
{
	
	return false;
}



int	can_move(burrow &b, int f, int t)
{
	if (b.s[f].occupied < 0) return -1;
	if (b.s[f].occupied > 99) return -1;
	if (valid(b, f, t)) return t;
	return -1;
}

int	get_moves(burrow &b, vm_t &t, bool debug = false)
{
	t.clear();
	for (int a = 0; a < 8; a++)
	{
		int from = b.a[a].location;
		if (from > 99) continue;
		for (int j = 0; j < 17; j++)
		{
			int to = can_move(b, from, j);
			if (debug) printf("[X} GET_MOVES:: amp: %d  loc: %d   to: %d (%d)\n",
				a, from, to, j);
			move_t m; m.from = from; m.to = to;
			if (to >= 0) t.push_back(m);
		}
	}
	return t.size();
}


int	get_moves(burrow &b, moves &t, bool debug = false)
{
	t.clear();
	for (int a = 0; a < 8; a++)
	{
		int from = b.a[a].location;
		if (from > 99) continue;
		for (int j = 0; j < 17; j++)
		{
			int to = can_move(b, from, j);
			if (debug) printf("{Y} GET_MOVES:: amp: %d  loc: %d   to: %d (%d)\n",
				a, from, to, j);
			if (to >= 0) t.add(from, to);
		}
	}
	return t.number();
}


moves::moves(burrow &b)
{
	get_moves(b, vm, false);
	reset();
}

burrow min_b;
int	   min_score = 999999999;

bool	recurse(burrow b)
{
	if (count(b) == 8) //(b.done())
	{
		if (energy(b) < min_score)
		{
			min_score = energy(b);
			min_b = b;
			out_burrow(b);
		}
		return true;
	}
//	moves m(b);
//	move_t nm;
//	m.reset();
//	bool v = m.first(nm);
//	burrow c = b;
	vm_t	mvs;
	get_moves(b, mvs, false);
	vm_t_i	it = mvs.begin();
	move_t nm;
	burrow c = b;
	
	while(it != mvs.end())
	{
		nm = *it;
		b = c;
		move(b, nm.from, nm.to);
		//printf("RECURSE: moving %d to %d  %s\n", nm.from, nm.to, TF(bm));
		//out_burrow(b);
		b.v.push_back(nm);
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
	char	ch[9];
	int		inch;
	int		chc = 0;
	int		reorder[8] = {0, 2, 4, 6, 1, 3, 5, 7};
	burrow	gb;

	while (!feof(f) && chc < 8)
	{
		inch = fgetc(f);
		if (inch == 'A' || inch == 'B' || inch == 'C' || inch == 'D')
		{
			//printf("Index: %d  Reorder: %d  Letter: %c\n", chc, reorder[chc], inch);
		    ch[reorder[chc++]] = inch;
		}
	}
	reset(gb, ch);
	out_burrow(gb);
	recurse(gb); 
}
void ixx(burrow bb)
{
#define do_move(n, m)	move(bb, n, m); out_burrow(bb);
do_move(0, 12);
do_move(4, 14);
do_move(2, 4);
do_move(3, 13);
do_move(12, 3);
do_move(14, 2);
do_move(6, 15);
do_move(7, 14);
do_move(13, 7);
do_move(14, 0);
do_move(15, 6);

}	
void	init(const char *fn, int n)
{
	FILE *f = fopen(fn, "r");
	if (!f) return;
	char	ch[9];
	int		inch;
	int		chc = 0;
	int		reorder[8] = {0, 2, 4, 6, 1, 3, 5, 7};
	burrow	gb;

	while (!feof(f) && chc < 8)
	{
		inch = fgetc(f);
		if (inch == 'A' || inch == 'B' || inch == 'C' || inch == 'D')
		{
			//printf("Index: %d  Reorder: %d  Letter: %c\n", chc, reorder[chc], inch);
		    ch[reorder[chc++]] = inch;
		}
	}
	reset(gb, ch);
	ixx(gb); exit(1);
	if (0)
	{
		for (int i = 0; i <= 16; i++)
		{
			for (int j = 0; j <= 16; j++)
			{
				printf("From %d to %d : %s\n", i, j, OK(valid(gb, i, j)));
			}
		}
	}
	out_burrow(gb);
	moves m(gb);
	get_moves(gb, m);
	m.out();
	move(gb, 4, 12);
	out_burrow(gb);
	
	get_moves(gb, m);
	m.out();
	move(gb, 2, 4);
	out_burrow(gb);
	
	get_moves(gb, m);
	m.out();
	move(gb, 3, 13);
	out_burrow(gb);
	
	get_moves(gb, m);
	m.out();
	move(gb, 12, 3);
	out_burrow(gb);
	
	get_moves(gb, m);
	m.out();
	move(gb, 0, 2);
	out_burrow(gb);
	
	get_moves(gb, m);
	m.out();
	move(gb, 6, 14);
	out_burrow(gb);
	
	get_moves(gb, m);
	m.out();
	move(gb, 7, 16);
	out_burrow(gb);
	
	get_moves(gb, m);
	m.out();
	move(gb, 14, 7);
	out_burrow(gb);
	
	get_moves(gb, m);
	m.out();
	move(gb, 13, 6);
	out_burrow(gb);
	
	get_moves(gb, m);
	m.out();
	move(gb, 16, 0);
	out_burrow(gb);
	
	dump(gb.s);
}

void ixx()
{
	burrow bb;
	moves m(bb);
#define Move_from(n, m)	move(bb, n, m); out_burrow(bb);
Move_from (0, 10);
Move_from (4, 11);
get_moves(bb, m);
m.out();
return;
Move_from (4, 12);
Move_from (4, 13);
Move_from (4, 14);
Move_from (4, 15);
Move_from (4, 16);
Move_from (2, 11);
Move_from (2, 12);
Move_from (12, 4);
Move_from (3, 13);
Move_from (11, 3);
Move_from (10, 2);
Move_from (6, 14);
Move_from (7, 15);
Move_from (13, 7);
Move_from (14, 6);
Move_from (15, 0);
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
	r_init("part1.txt", 0);
}


