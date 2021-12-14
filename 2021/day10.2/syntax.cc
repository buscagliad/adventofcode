#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>
#include <cstring>
#include <string>

using namespace std;
#define MAXX 256
long long int	syncount[MAXX];
int scn = 0;

const char *opench = "([{<";
const char *closech = ")]}>";
const char ignore = '-';

#define MAXLINE 1000

void    alswap(long long int *d, int i, int j)
{
        long long int s = d[i];
        d[i] = d[j];
        d[j] = s;
}

void    alsort(long long int *d, int n)
{
        for (int i = 0; i < n; i++)
            for (int j = i; j < n; j++)
                if (d[i] > d[j]) alswap(d, j, i);
}

void zerodata()  
{
	for(int i = 0; i < MAXX; i++) 
	    syncount[i] = 0;
	scn = 0;
}

char	cchar(char o)
{
	int i = 0;
	while (opench[i] != o) i++;
	return closech[i];
}

char	ochar(char c)
{
	int i = 0;
	while (closech[i] != c) i++;
	return opench[i];
}

bool collapse(char *head, char *cl)
{
	int	i = cl - head;
	char	oc = ochar(*cl);
	while (i >= 0)
	{
		i--;
		if (head[i] == ignore) continue;
		if (head[i] != oc) return false;
		head[i] = ignore;
		*cl = ignore;
		return true;
	}
	return true; // should never get here
}

char parseline(char *c)	// returns first bad char - OR - ignore if ok
{
	char  *p = c;
	char  *head = c; 
	while (*p != '\n')
	{
		if (strchr(closech, *p))
		{
			if (!collapse(head, p))
			{
				//printf("SE: %s  |%c|\n", head, *p);
				return *p;
			}
			//printf("%s\n", head);
		}
		p++;
	}
	return ignore;
}

long long int	autocomplete(char *s)
{
	long long int score = 0;
	for (int i = strlen(s) - 1; i >= 0; i--)
	{
		if (s[i] == ignore) continue;
		switch(s[i])
		{
			case '(' :
			    score = 5 * score + 1;
			    break;
			case '[' :
				score = 5 * score + 2;
			    break;
			case '{' :
				score = 5 * score + 3;
			    break;
			case '<' :
				score = 5 * score + 4;
			    break;
			default:
			    break;
		}
	}
	return score;
}

void solve(const char *v, int tsynerr, long long int tacomp)
{
	FILE *f = fopen(v, "r");

	char c[MAXLINE];
	fgets(c, MAXLINE, f);
	zerodata();
	int score = 0;
	while (!feof(f))
	{
		char z = parseline(c);
		switch (z)
		{
			case ')' : score += 3; break;
			case ']' : score += 57; break;
			case '}' : score += 1197; break;
			case '>' : score += 25137; break;
			case ignore : 
				syncount[scn] = autocomplete(c);
				//printf("Line: %s  Score: %lld\n", c, syncount[scn]);
				scn++;
			default:
				break;
		}
		fgets(c, MAXLINE, f);
	}

	printf("Syntax input file: %s\n", v);
	printf("Syntax error score: %d\n", score);
	if (tsynerr > 0)
	{
		if (score != tsynerr)
			printf("ERROR - syntax error answer does not agree with truth: %d!\n", tsynerr);
		else
			printf("Successfully esimated syntax error level!!\n");\
	}
	alsort(syncount, scn);
	long long int ascore = syncount[scn/2];
	printf("Autocomplete score is: %lld\n", ascore);
	if (tacomp > 0)
	{
		if (ascore != tacomp)
			printf("ERROR - auto complete answer does not agree with truth: %lld!\n", tacomp);
		else
			printf("Successfully esimated autocomplete answer!!\n");\
	}
	fclose(f);
}

int main(int argc, char **argv)
{
	solve("ex.txt", 26397, 288957);
    printf("\n\n");
	solve("data.txt", 339537, 2412013412);

	return 0;
}
