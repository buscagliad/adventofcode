#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>
#include <cstring>
#include <string>

using namespace std;

const	char	*zero   = "abcefg";
const	char	*one    = "cf";
const   char	*two    = "acdeg";
const   char	*three  = "acdfg";
const   char    *four   = "bcdf";
const   char    *five   = "abdfg";
const   char    *six    = "abdefg";
const   char    *seven  = "acf";
const   char    *eight  = "abcdefg";
const   char    *nine   = "abcdfg";

const	char	*digs[] = {zero, one, two, three, four, five, six, seven, eight, nine};

#define NUM_SEGMENTS 7
class cmap {
	public:
		cmap();
		void	add(char from, char to, const char *reason);
		void	swap(char *code);
		int		num_filled();
		void	out();
		bool	is_set(char c);
		int		decode(char *code);
	private:
		char	segments[NUM_SEGMENTS];
		string  reasons[NUM_SEGMENTS];
};

void    alswap(char *d, int i, int j)
{
	char s = d[i];
	d[i] = d[j];
	d[j] = s;
}

void	alsort(char *d)
{
	int	n = strlen(d);
	for (int i = 0; i < n; i++)
	    for (int j = i; j < n; j++)
	        if (d[i] > d[j]) alswap(d, j, i);
}



cmap::cmap()
{
	for (int i = 0; i < NUM_SEGMENTS; i++)
	    segments[i] = 0;
}

void	cmap::add(char from, char to, const char *reason)
{
	int	index = from - 'a';
	segments[index] = to;
	reasons[index] = reason;
	//printf("Assigning %c --> %c  %s\n", from, to, reason);
}

void	cmap::swap(char *code)
{
	char	new_code[NUM_SEGMENTS];
	for (int i = 0; i < NUM_SEGMENTS; i++)
	    new_code[i] = segments[code[i] - 'a'];
	for (int i = 0; i < NUM_SEGMENTS; i++)
	    code[i] = new_code[i];
}

int	cmap::decode(char *code)
{
	char	new_code[NUM_SEGMENTS];
	for (int i = 0; i < NUM_SEGMENTS; i++)
	{
		if (code[i])
	        new_code[i] = segments[code[i] - 'a'];
	    else
	    {
			new_code[i] = 0;
			break;
		}
	}
	alsort(new_code);
	//printf("CODE: %s   NEW: %s\n", code, new_code);
	for (int i = 0; i < 10; i++)
	    if (strcmp(new_code, digs[i]) == 0) return i;
	return -1;
}

int		cmap::num_filled()
{
	int count = 0;
	for (int i = 0; i < NUM_SEGMENTS; i++)
	    if(segments[i]) count++;
	return count;
}

void	cmap::out()
{
	for (int i = 0; i < NUM_SEGMENTS; i++)
	    if(segments[i])
			printf("%c --> %c -- %s\n", i + 'a', segments[i], reasons[i].c_str());
}

bool	cmap::is_set(char a)
{
	for (int i = 0; i < NUM_SEGMENTS; i++)
	    if(segments[a - 'a']) return true;
	return false;
}
	

// seg_a = 0,2,3,5,6,7,8,9
// seg_b = 0,4.5.6.8.9
// seg_c = 0,1,2,3,4,7,8,9
// seg_d = 2,3,4,5,6,8,9
// seg_e = 0,2,6,8
// seg_f = 0,1,3,4,5,6,7,8,9
// seg_g = 0,2,3,5,6,8,9

char	*move (char *s)
{
	if (strlen(s) < 1) return NULL;
	while (*s != ' ' && *s != '\n') s++;
	*s = 0;
	s++;
	return s;
}

void get_segs(char *bf[], int *segs)
{
	for (char c = 'a'; c <= 'g'; c++)
		segs[c - 'a'] = 0;
	for (int i = 0; i < 10; i++)
	{
		char	*d = bf[i];
		for (; *d; d++)
			segs[*d - 'a']++;
	}
	for (int i = 0; i < 7; i++)
	{
		//printf("Segment: %c - %d\n", i + 'a', segs[i]);
	}
}

char	chdiff(char o[2], char s[3])
{
	for (int i = 0; i < 3; i++)
		if ( (s[i] != o[0]) && (s[i] != o[1])) return s[i];
	printf("ERROR in chdiff - o: %s  s: %s\n", o, s);
	return 0;
}

char	one_seven(char *bf[])
{
	char	*o = NULL;
	char	*s = NULL;
	for (int i = 0; i < 10; i++)
	{
		if (strlen(bf[i]) == 2) o = bf[i];
		if (strlen(bf[i]) == 3) s = bf[i];
	}
	return chdiff(o, s);
}

/*
seg: a - count: 4  -> e
seg: b - count: 8
seg: c - count: 7
seg: d - count: 8
seg: e - count: 9  -> f
seg: f - count: 7
seg: g - count: 6  -> b
*/

bool incmap(char a, char *m)
{
	for (int i = 0; i < 4; i++) if (a == m[i]) return true;
	return false;
}

// cmap will get filled in for the 'd' segment, the empty cell
// will be the 'g' segment
void    four_seg(char *bf[], cmap &cm)
{
	char	*f = NULL;
	// get the four-segment value (this represents the number four)
	for (int i = 0; i < 10; i++)
	{
		if (strlen(bf[i]) == 4) f = bf[i];
	}
	for (int i = 0; i < 4; i++)
	{
		if (cm.is_set(f[i])) continue;
		cm.add(f[i], 'd', "From four segment, left over segment is : d");
		break;
	}
	// the last 'not-set' segment is the 'g' segment
	for (int i = 0; i < NUM_SEGMENTS; i++)
		if (!cm.is_set(i + 'a')) cm.add(i + 'a', 'g', "Final segment that has not been set is 'g'");
}

int	out_digits(char *bf[], char *af[])
{
	cmap cm;
	int	segs[8];
	get_segs(bf, segs);

	
	char a_map = one_seven(bf);
	int a_index = a_map - 'a';
	cm.add(a_map, 'a', "Difference of '1' and '7' digits");
	for (int i = 0; i < 7; i++)
	{
		if (segs[i] == 4) cm.add(i + 'a', 'e', "Initial four segments used - 'e'");
		else if (segs[i] == 9) cm.add(i + 'a', 'f', "Initial nine segments used - 'f'");
		else if (segs[i] == 6) cm.add(i + 'a', 'b', "Initial six segments used - 'b'");
		if ( (segs[i] == 8) && ( i != a_index) )
			cm.add(i + 'a', 'c', "Eight segment - not the 'a' means it's the 'c'");
	}
	// get the number four (four segments) we now know segments
	// b, c and f  -- that leaves the one that matches segment d
	//    
	//  ....
	// b    c
	// b    c
	//  dddd
	// .    f
	// .    f
	//  ....
	
	four_seg(bf, cm);
	//cm.out();
	int  v = 0;
	for (int i = 0; i < 4; i++)
	{
		int	d = cm.decode(af[i]);
		v = 10 * v + d;
	    //printf("%s --> %d\n", af[i], d);
	}
	//printf("Display: %d\n", v);
	return v;
}

void	parseline(char *s, char *bf[], int &bf_num,
							char *af[], int &af_num)
{
	char *sd = strdup(s);
	bf_num = 0;
	af_num = 0;
	//printf("INPUT: %s\n", sd);
	while (!sd || *sd != '|')
	{
		bf[bf_num] = sd;
		sd = move(sd);
		//alsort(bf[bf_num]);
		bf_num++;
	}
	//for (int i = 0; i < bf_num; i++)
	//    printf("Before[%d] : %s\n", i, bf[i]);
	//printf("Remainder1: <%s>\n", sd);
	while (*sd == ' ' || *sd == '|') sd++;
	//printf("Remainder2: <%s>\n", sd);
	while (sd && *sd != '\n')
	{
		af[af_num] = sd;
		sd = move(sd);
		//alsort(af[af_num]);
		//printf("%s--\n", af[af_num]);
		af_num++;
	}
	//for (int i = 0; i < af_num; i++)
	    //printf("AFter[%d] : %s\n", i, af[i]);
}
#define MAXLINE 1000
int init(FILE *f)
{
	int counter = 0;
	char c[MAXLINE];
	char *bf[100];
	int  bf_num;
	char *af[100];
	int  af_num;
	rewind(f);

	fgets(c, MAXLINE, f);
	while (!feof(f))
	{
		parseline(c, bf, bf_num, af, af_num);
		counter += out_digits(bf, af);
		/*
		int v = 0;
	    for (int i = 0; i < af_num; i++)
	    {
			v = strlen(af[i]);
			if ( (v == 2) || (v == 3) || (v == 4) || (v == 7) )
			    counter++;
		}
		*/
		fgets(c, MAXLINE, f);
	}
	return counter;
}

int count_2_3_4_7s(FILE *f)
{
	int v = 0;
	int counter = 0;
	char c[MAXLINE];
	char *bf[100];
	int  bf_num;
	char *af[100];
	int  af_num;
	rewind(f);
	fgets(c, MAXLINE, f);
	while (!feof(f))
	{
		parseline(c, bf, bf_num, af, af_num);
	    for (int i = 0; i < af_num; i++)
	    {
			v = strlen(af[i]);
			if ( (v == 2) || (v == 3) || (v == 4) || (v == 7) )
			    counter++;
		}
		fgets(c, MAXLINE, f);
	}
	return counter;
}

int main(int argc, char **argv)
{
	FILE *f = fopen(argv[1], "r");

	printf("Count of 2's, 3's, 4's and 8's: %d\n", count_2_3_4_7s(f));
	printf("Sum of all outputs: %d\n", init(f));

	return 0;
}
