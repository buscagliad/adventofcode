#include <stdint.h>
#include <ctype.h>
#include <stdio.h>
#include <vector>
#include <stdlib.h>

using namespace std;

#define P_SIZE 27	// 'A' - 'Z' + ' '
typedef struct rule_t {
	int insert;
	int left;
	int right;
	char pair[3];
	char in_char;
} rule_t;

class poly{
	public:
		poly(const char *f);	// initialize from file
		int64_t step();	// applies rules to existing polymer
		int64_t least(char &n);
		int64_t most(char &n);
		int64_t length();
		int64_t occurs(char c);
		void out_rules();
		void info();
		int rule(char insert, char left, char right);	// add rull to insert 'insert' between left right chars
	private:
		void rule_init(const char *s);
		void pmer_init(const char *s);
		int64_t sum();
		int64_t pmer[P_SIZE][P_SIZE];
		int64_t delta[P_SIZE][P_SIZE];
		int64_t count[P_SIZE];
		vector<rule_t> rules;
		int     num_rules;
};
/*
#define INDEX(c)	((toupper(c) - 'A'))
#define ASCII(c)	(('A' + c))
*/

void poly::out_rules()
{
	printf("There are %d rules:\n", num_rules);
	for (int i = 0; i < num_rules; i++)
	{
		printf("%s -> %c\n", rules[i].pair, rules[i].in_char);
	}
}

		

int  INDEX(char c)
{
	c = toupper(c);
	if (isalpha(c)) return c - 'A';
	return P_SIZE - 1;
}

char ASCII(int c)
{
	c += 'A';
	if (isalpha(c)) return c;
	return ' ';
}


int64_t poly::occurs(char c)
{
	int ch = INDEX(c);
	return count[ch];
}

void poly::info()
{
	char nm, nl;
	int64_t m = most(nm);
	int64_t l = least(nl);
	for (char c = 'A'; c <= 'Z'; c++)
	{
		int64_t s = occurs(c);
		if (s > 0)
			printf("%c occurs %ld times\n", c, s);
	}
	printf("Most occuring polymer: %c - %ld times\n", nm, m);
	printf("Least occuring polymer: %c - %ld times\n", nl, l);
	printf("DIFFERENCE: %ld times\n", m - l);
	printf("Total polymer pairs: %ld\n", length());

}

const char *next_pair(const char *s, int &x, int &y, bool &first)
{
	//printf("NEXT_PAIR: %s\n", s);
	if (first)
	{
		first = false;
		x = P_SIZE - 1;
		y = INDEX(*s);
		return s;
	}
	if (*s == '\n') return NULL;
	x = INDEX(*s);
	s++;
	y = INDEX(*s);
	//printf("      x: %d  y: %d\n", x, y);
	return s;
}

void zero(int64_t p[P_SIZE][P_SIZE])
{
	int i,j;
	for (i = 0; i < P_SIZE; i++)
	    for (j = 0; j < P_SIZE; j++)
			p[i][j] = 0;
}

int64_t poly::length()
{
	int i,j;
	int64_t s = 0;
	for (i = 0; i < P_SIZE; i++)
	    for (j = 0; j < P_SIZE; j++)
			s+= pmer[i][j];
	return s;
}

void poly::pmer_init(const char *s)
{
	int i, j;
	printf("INIT: %s", s);
	num_rules = 0;
	zero(pmer);
	zero(delta);
	bool first = true;
	for (i = 0; i < P_SIZE; i++) count[i] = 0;
	for (const char *t = s; *t != '\n'; t++)
	    count[INDEX(*t)]++;
	while ((s = next_pair(s, i, j, first)))
	    pmer[i][j]++;
}

// CB -> P
void poly::rule_init(const char *s)
{
	//printf("RULE: %s\n", s);
	rule(s[0], s[1], s[6]);
}

poly::poly(const char *fn)
{
	FILE *f = fopen(fn, "r");
	char s[1000];
	fgets(s, 1000, f);
	pmer_init(s);
	fgets(s, 1000, f);
	fgets(s, 1000, f);
	while (!feof(f))
	{
		rule_init(s);
		fgets(s, 1000, f);
	}
}

int poly::rule(char left, char right, char insert)
{
	rule_t k;
	k.insert = INDEX(insert);
	k.in_char = insert;
	k.pair[0] = left;
	k.pair[1] = right;
	k.pair[2] = 0;
	k.left = INDEX(left);
	k.right = INDEX(right);
	rules.push_back(k);

	num_rules = rules.size();
	return num_rules;
}

#ifdef OLD_STUFF
int64_t poly::most(char pair[3])
{
	int64_t m = 0;
	int	i, j;
	pair[2] = 0;
	
	for (i = 0; i < P_SIZE; i++)
	    for (j = 0; j < P_SIZE; j++)
	    {
			if (pmer[i][j] > m) 
			{
				pair[0] = ASCII(i);
				pair[1] = ASCII(j);
				m = pmer[i][j];
			}
		}
	return m;
}
	

int64_t poly::least(char pair[3])
{
	int64_t m = 0x7FFFFFFFFFFFFFFF;
	pair[2] = 0;
	int i, j;
	for (i = 0; i < P_SIZE; i++)
	    for (j = 0; j < P_SIZE; j++)
	    {
			int64_t p = pmer[i][j];
			if (p > 0 && p < m) 
			{
				pair[0] = ASCII(i);
				pair[1] = ASCII(j);
				m = pmer[i][j];
			}
		}
	return m;
}
#else
int64_t poly::most(char &n)
{
	int64_t m = 0;
	int	i;
	
	for (i = 0; i < P_SIZE - 1; i++)
	if (count[i] > m) 
	{
		n = ASCII(i);
		m = count[i];
	}
	return m;
}
	

int64_t poly::least(char &n)
{
	int64_t m = 0x7FFFFFFFFFFFFFFF;
	int i;
	for (i = 0; i < P_SIZE - 1; i++)
		if (count[i] && count[i] < m) 
		{
			n = ASCII(i);
			m = count[i];
		}
	return m;
}
#endif

int64_t	poly::step()
{
	int	ri;
	for (ri = 0; ri < num_rules; ri++)
	{
		int	ins = rules[ri].insert;
		int l = rules[ri].left;
		int r = rules[ri].right;
		int64_t n = pmer[l][r];
		if (n == 0) continue;
		//printf("Rule %d   Insert: %c   Between: %s\n", ri+1, rules[ri].in_char, rules[ri].pair);
		//printf("  Found %d pairs ", n);
		delta[ins][r] += n;
		count[ins] += n;
		delta[l][ins] += n;
		//printf("  removing %c%c  inserting %c\n", ASCII(l), ASCII(r), ASCII(ins));
		delta[l][r] -= n;
	}
	for (int i = 0; i < P_SIZE-1; i++)
	    for (int j = 0; j < P_SIZE-1; j++)
	        pmer[i][j] += delta[i][j];
	zero(delta);
	return length();
}

int main(int argc, char** argv)
{
	poly p(argv[1]);
	p.info();
	p.out_rules();
	int num_steps = atoi(argv[2]);
	
	for (int i = 1; i <= num_steps; i++)
	{
		p.step();

	}
	printf("\n\nAfter step %d:\n", num_steps);
	p.info();
}
