#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>
#include <cstring>
#include <string>

using namespace std;
#define MAXX 256
int	syncount[MAXX];

const char *opench = "([{<";
const char *closech = ")]}>";
const char ignore = '-';

#define MAXLINE 1000


void zerodata()  
{
	for(int i = 0; i < MAXX; i++) 
	    syncount[i] = 0;
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


void solve(const char *v, int tsynerr, int ttop3)
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
				//printf("Line is good\n");
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
	fclose(f);
}

int main(int argc, char **argv)
{
	solve("ex.txt", 26397, 1134);
    printf("\n\n");
	solve("data.txt", 588, 964712);

	return 0;
}
