#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>

//   inp a - Read an input value and write it to variable a.
//   add a b - Add the value of a to the value of b, then store the result in variable a.
//   mul a b - Multiply the value of a by the value of b, then store the result in variable a.
//   div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. 
//            (Here, "truncate" means to round the value toward zero.)
//   mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
//   eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
//
// the input has only three commands that are different between steps, these are:
// inp w		This will be the n'th digit - obtained via recursion and for loops
// mul x 0		ALWAYS zeroes X
// add x z		ALWAYS sets X to z (z persists across steps)
// mod x 26		ALWAYS mod x by 26
// div z 1		--> div z by either 1 or 26 (this will determine max_z
// add x 10		--> add_x: number changes at each step
// eql x w		ALWAYS sets x to 1 if it's equal to w, 0 otherwise
// eql x 0		ALWAYS sets x to 1 if it's equal to 0, 0 otherwise
// mul y 0		ALWAYS sets y to 0
// add y 25		ALWAYS sets y to 25
// mul y x		ALWAYS sets y = y * x
// add y 1		ALWAYS increments y by 1
// mul z y		ALWAYS set z = z * y
// mul y 0		ALWAYS set y = 0
// add y w		ALWAYS set y = y + w
// add y 2		--> add_y: y = y + this value
// mul y x		ALWAYS set y = y * x
// add z y		ALWAYS set z = z + y

// These values shown below are 'hardcoded' for my specific data.txt input file
// I (for no good reason) wanted to genericize this based on the input file
#define T7 8031810176 // 26 ^ 7
#define T6 308915776  // 26 ^ 6
#define T5 11881376   // 26 ^ 5
#define T4 456976     // 26 ^ 4
#define T3 17576      // 26 ^ 3
#define T2 676        // 26 ^ 2
#define T1 26         // 26 ^ 1
		        //  1   2   3   4   5   6   7   8   9  10  11  12   13  14
int64_t add_x[] = {10, 10, 14, 11, 14,-14, 0, 10, -10, 13,-12, -3, -11, -2};
int64_t add_y[] = { 2,  4,  8,  7, 12, 7, 10, 14,   2,  6,  8, 11,  5,  11};
int64_t div_z[] = { 1,  1,  1,  1,  1, 26, 26,  1, 26,  1, 26, 26,  26, 26};
int64_t max_z[] = {T7, T7, T7, T7, T7, T7, T6, T5, T5, T4, T4, T3,  T2, T1};

int		step = -1;	// "inp w" indicates start of a step - will increment then
int		step_line = 0;
void	update_add_z(int64_t divz)
{
	div_z[step] = divz;
}
void	update_add_y(int64_t addy)
{
	add_y[step] = addy;
}
void	update_add_x(int64_t addx)
{
	add_x[step] = addx;
}

void	update_max_z()
{
	max_z[13] = div_z[13];
	for (int i = 12; i >= 0; i--)
	{
		max_z[i] = div_z[i] * max_z[i+1];
	}
}

typedef enum { ERROR, INP, ADD, MUL, DIV, MOD, EQL} op_t;

bool debug = false;
#define DEB(n)	if (0) printf("--- VAR: %c  OP: %s :: in-value: %ld   final-value: %ld\n", nm, __FUNCTION__, n, value);
#define DEBUG	DEB(v)
#define DEBUGC	DEB(v.value)


int64_t	get_input();
void	set_value(const char *n);


#define	MAX_DIGS 15
char	digs[MAX_DIGS];
int		dig_index = 0;
void	set_value(const char *n)
{
	strncpy(digs, n, MAX_DIGS);
	dig_index = 0;
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

bool	get_val(char *s, int64_t &v)
{
	if (isalpha(*s)) return false;
	v = atoll(s);
	return true;
}


void	parse_line(char	*inl)
{
	op_t	op = get_op(inl);
	char	var = inl[4];
	int64_t	v;
	bool	is_a_value = get_val(inl+6, v);
	if (op == INP) { step++; step_line = 1;  return;} else step_line++;
	if ( (op == DIV) && (var == 'z') && (step_line == 5) && (is_a_value) ) update_add_z(v);
	if ( (op == ADD) && (var == 'x') && (step_line == 6) && (is_a_value) ) update_add_x(v);
	if ( (op == ADD) && (var == 'y') && (step_line == 16) && (is_a_value) ) update_add_y(v);
	return;
}

#define PVEC(s, v, n)		printf("%s: %ld", s, v[0]); for (int i = 1; i < n; i++)\
							{printf(", %ld", v[i]); } printf("\n");


void	parse_file(const char *fn)
{
	FILE *f = fopen(fn, "r");
	char	inl[100];
	fgets(inl, 100, f);
	if (0)
	{		printf("Hard coded values\n");
		PVEC("div_z", div_z, 14);
		PVEC("max_z", max_z, 14);
		PVEC("add_x", add_x, 14);
		PVEC("add_y", add_y, 14);
	}
	while (!feof(f))
	{
		inl[strlen(inl)-1] = 0;
		parse_line(inl);
		fgets(inl, 100, f);
	}
	update_max_z();
	if (0)
	{
		printf("Input from file: %s\n", fn);
		PVEC("div_z", div_z, 14);
		PVEC("max_z", max_z, 14);
		PVEC("add_x", add_x, 14);
		PVEC("add_y", add_y, 14);
			
	}
	fclose(f);
}

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
	parse_file("data.txt");
	solution();

	return 1;
}
	
