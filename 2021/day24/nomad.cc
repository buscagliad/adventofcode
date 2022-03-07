#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

//   inp a - Read an input value and write it to variable a.
//   add a b - Add the value of a to the value of b, then store the result in variable a.
//   mul a b - Multiply the value of a by the value of b, then store the result in variable a.
//   div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. 
//            (Here, "truncate" means to round the value toward zero.)
//   mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
//   eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.

typedef enum { ERROR, INP, ADD, MUL, DIV, MOD, EQL} op_t;

bool debug = false;
#define DEB(n)	if (0) printf("--- VAR: %c  OP: %s :: in-value: %ld   final-value: %ld\n", nm, __FUNCTION__, n, value);
#define DEBUG	DEB(v)
#define DEBUGC	DEB(v.value)


int64_t	get_input();
void	set_value(const char *n);


class var {
	public:
		var(char _nm) {nm = _nm; value = 0; };
		void op(op_t ot, int64_t v);
		void op(op_t ot, var *wv);
		void inp()			{int64_t v = get_input(); value = v; DEBUG; };
		void add(int64_t v)	{value += v; DEBUG; };
		void add(var v)		{value += v.value; DEBUGC; };
		void mul(int64_t v)	{value *= v; DEBUG; };
		void mul(var v)		{value *= v.value; DEBUGC; };
		void div(int64_t v)	{value /= v; DEBUG; };
		void div(var v)		{value /= v.value; DEBUGC; };
		void mod(int64_t v)	{value %= v; DEBUG; };
		void mod(var v)		{value %= v.value; DEBUGC; };
		void eql(int64_t v)	{value = (value == v) ? 1 : 0; DEBUG; };
		void eql(var v)		{value = (value == v.value) ? 1 : 0; DEBUGC; };
		void set(int64_t v)	{value = v;};
		int64_t get()		{return value;};
		void out()			{printf("VAR: %c  value: %ld\n", nm, value); };
	private:
		int64_t value;
		char	nm;
};

void var::op(op_t ot, int64_t v)
{
	switch (ot)
	{
		case INP: inp(); break;
		case ADD: add(v); break;
		case MUL: mul(v); break;
		case DIV: div(v); break;
		case MOD: mod(v); break;
		case EQL: eql(v); break;
		default:
			printf("ERROR - cannot perform this operation\n");
	}
}
		
void var::op(op_t ot, var *wv)
{
	op(ot, wv->get());
}


var	x('x');
var y('y');
var w('w');
var z('z');

#define	MAX_DIGS 15
char	digs[MAX_DIGS];
int		dig_index = 0;
void	set_value(const char *n)
{
	strncpy(digs, n, MAX_DIGS);
	dig_index = 0;
	w.set(0);
	x.set(0);
	y.set(0);
	z.set(0);
}
int64_t	get_input()
{
	if (dig_index >= MAX_DIGS) return 0;
	return digs[dig_index++]-'0';
}

op_t	get_op(char *op)
{
	if (strncmp(op, "inp", 3) == 0) return INP;
	if (strncmp(op, "add", 3) == 0) return ADD;
	if (strncmp(op, "mul", 3) == 0) return MUL;
	if (strncmp(op, "div", 3) == 0) return DIV;
	if (strncmp(op, "mod", 3) == 0) return MOD;
	if (strncmp(op, "eql", 3) == 0) return EQL;
	return ERROR;
}

var	*get_var(char c)
{
	switch(c)
	{
		case 'w': return &w;
		case 'x': return &x;
		case 'y': return &y;
		case 'z': return &z;
		default: return NULL;
	}
	return NULL;
}

int64_t	get_val(char *s)
{
	var	*v = get_var(*s);
	if (v) return v->get();
	return atoll(s);
}


bool	parse_line(char	*inl)
{
	op_t	op = get_op(inl);
	var		*vr = get_var(inl[4]);
	int64_t	vl = get_val(inl+6);
	if (debug) printf("INLINE: %s :: ", inl);
	vr->op(op, vl);
	if (debug) printf("w: %ld  x: %ld  y: %ld  z: %ld\n", w.get(), x.get(), y.get(), z.get());
	if (op == INP) return true;
	return false;
}

void	parse_file(const char *fn)
{
	FILE *f = fopen(fn, "r");
	char	inl[100];
	fgets(inl, 100, f);
	while (!feof(f))
	{
		inl[strlen(inl)-1] = 0;
		//parse_line(inl);
		if(parse_line(inl))
		{
			printf("Current state:  %s  digits: %d  w:%ld  x: %ld  y: %ld  z: %ld\n", digs, dig_index-1,
				w.get(), x.get(), y.get(), z.get());
			//x.set(0);
			//w.set(0);
			//z.set(0);
			//y.set(0);
		}
		fgets(inl, 100, f);
	}
	if (1)
	{
		printf("Final state:  %s  digits: %d  w:%ld  x: %ld  y: %ld  z: %ld\n", digs, dig_index,
				w.get(), x.get(), y.get(), z.get());
	}
	fclose(f);
}

char	randig()
{
	double	r = rand() / (double) RAND_MAX * 9;
	int     ir = r;
	return '1' + ir;
}
	

void	ran_value()
{
	char	rv[15];
	rv[14] = 0;
	for (int i = 0; i < 14; i++)
		rv[i] = randig();
	set_value(rv);
}

bool	is_valid(const char *s)
{
	for (int i = 0; i < 14; i++)
	{
		if (s[i] < '1') return false;
		if (s[i] > '9') return false;
	}
	return true;
}

void	make_valid(char *s)
{
	for (int i = 0; i < 14; i++)
	{
		if (s[i] < '1') s[i] = '1';
		if (s[i] > '9') s[i] = '9';
	}
}
	

void	set_int_value(int64_t v)
{
	char	sv[20];
	sprintf(sv, "%ld", v);
	make_valid(sv);
	set_value(sv);
}
	
int	max_search = 0;
#define MAX_SEARCH 1000

int64_t	binary_step(int64_t start, int64_t end)
{
	if (max_search > MAX_SEARCH) return 0;
	max_search++;
	set_int_value(start);
	parse_file("data.txt");
	int64_t start_z = z.get();
	set_int_value(end);
	parse_file("data.txt");
	int64_t end_z = z.get();
	if (end_z * start_z > 0) {
		printf("Same side of zero\n");
	}
	//int64_t mid = start + (start-end)/2;
	int64_t mid_z = z.get();
	if ( (mid_z > start_z) ||
	     (mid_z > end_z) )
	     { printf("No Convergence\n");
		return 0;
	}

	return mid_z;
}

void test1()
{
	int64_t sv = 11111111111111;
	int64_t cv = 11111111111111;
	int64_t k = 1;
	set_int_value(sv);
	for (k = 1; k < 100000000000000; k = k*10)
	{
		sv = cv;
		for (int i = 1; i <= 9; i++)
		{
			set_int_value(sv);
			parse_file("data.txt");
			printf("[%d] - serial number: %s   z = %ld\n", i, digs, z.get());
			sv += k;
		}
	}
}

void test2()
{
	for (int64_t k = 1; k < 1000000; k++)
	{

		ran_value();
		parse_file("data.txt");
		if (z.get() == 0) printf("[%ld] - serial number: %s   z = %ld\n", k, digs, z.get());
	}
}
void test3()
{
	for (int64_t k = 11111111111111; k < 100000000000000; k+=11111111111111)
	{

		set_int_value(k);
		parse_file("data.txt");
		if (z.get() == 0) printf("[%ld] - serial number: %s   z = %ld\n", k, digs, z.get());
	}
}

#define T7 8031810176 // 26 ^ 7
#define T6 308915776  // 26 ^ 6
#define T5 11881376   // 26 ^ 5
#define T4 456976     // 26 ^ 4
#define T3 17576      // 26 ^ 3
#define T2 676        // 26 ^ 2
#define T1 26         // 26 ^ 1
					  //  1   2   3   4   5   6   7   8   9  10  11  12   13  14
const int64_t div_z[] = { 1,  1,  1,  1,  1, 26, 26,  1, 26,  1, 26, 26,  26, 26};
const int64_t max_z[] = {T7, T7, T7, T7, T7, T7, T6, T5, T5, T4, T4, T3,  T2, T1};
const int64_t add_x[] = {10, 10, 14, 11, 14,-14, 0, 10, -10, 13,-12, -3, -11, -2};
const int64_t add_y[] = { 2,  4,  8,  7, 12, 7, 10, 14,   2,  6,  8, 11,  5,  11};

bool try_digit(int dig_index, int dig_value, int64_t z, int64_t serial_number, bool largest)
{
	//printf("digit: %d   w: %d  z: %ld  sn: %ld\n",  dig_index, dig_value, z, serial_number);
	int64_t w = dig_value; // step 1
	int64_t x = z; // step 2/3
	x = x % 26;	// step 4
	serial_number = 10 * serial_number + w; // need to do before if (dig_index == 13)

	z = z / div_z[dig_index]; // step 5
	x += add_x[dig_index]; // step 6
	if (x == w) x = 0; else x = 1; // step 7
	if (x == 0) x = 0; else x = 1; // step 8
	int64_t y = 25; // steps 9 & 10
	y *= x; // step 11
	y++; // step 12
	z *= y; // step 13
	y = w + add_y[dig_index]; // steps 14, 15, and 16
	y *= x; // step 17
	z += y; // step 18
	if (z > max_z[dig_index]) return false;
	if (dig_index == 13)
	{
		if (z == 0)	// solution!!!
		{
			if (largest)
				printf("LARGEST Serial number %ld\n", serial_number);
			else
				printf("SMALLEST Serial number %ld\n", serial_number);
			return true;
		}
		return false;
	}
	dig_index++;
	for (int k = 9; largest && k >= 1; k--)
	   if (try_digit(dig_index, k, z, serial_number, largest)) return true;
	for (int k = 1; !largest && k <= 9; k++)
	   if (try_digit(dig_index, k, z, serial_number, largest)) return true;
	return false;
}

void	solution()
{
	for (int k = 9; k >= 1; k--)
	{
		if (try_digit(0, k, 0, 0, true)) break;
	}
	for (int k = 1; k <= 9; k++)
	{
		if (try_digit(0, k, 0, 0, false)) break;
	}
}
				


int	main(int argc, char **argv)
{
	srand(time(0));
	if (1) {
		solution();
		return 1;
	}
	if (1) {
		set_int_value(99429795993929);		// largest
		parse_file("data.txt");
		return 1;
	}
	set_int_value(61191516111321);
	parse_file("data.txt");
	set_int_value(18113181571611);		// smallest
	parse_file("data.txt");
	return 1;
	test3();
	//parse_file("ex.txt");
	return 1;
}
	
