#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>
#include <cstring>

using namespace std;

char	*move (char *s)
{
	if (strlen(s) < 1) return NULL;
	while (*s != ' ' && *s != '\n') s++;
	*s = 0;
	s++;
	return s;
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
		//printf("%s--\n", af[af_num]);
		af_num++;
	}
	//for (int i = 0; i < af_num; i++)
	    //printf("AFter[%d] : %s\n", i, af[i]);
}
#define MAXLINE 1000
int init(FILE *f)
{
	int v = 0;
	int counter = 0;
	char c[MAXLINE];
	char *bf[100];
	int  bf_num;
	char *af[100];
	int  af_num;

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

	printf("Number of 1's, 4's, 7's and 8's is: %d\n", init(f));

	return 0;
}
