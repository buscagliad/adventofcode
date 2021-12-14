#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>
#include <cstring>
#include <string>

using namespace std;
#define MAXX 200
#define MAXY 200
int	grid[MAXX][MAXY];
int xpts = 0;
int ypts = 0;

#define MAXLINE 1000

void parseline(char *c)
{
	int   x = 0;
	int   y = ypts;
	while (*c != '\n')
	{
		grid[x++][y] = *c - '0';
		c++;
	}
	ypts++;
	xpts = x;
}

void getadjs(int x, int y, int &up, int &down, int &left, int &right)
{
	if (x == 0) left = 9;
	else left = grid[x-1][y];
	if (x == (xpts - 1)) right = 9;
	else right = grid[x+1][y];
	
	if (y == 0) up = 9;
	else up = grid[x][y-1];
	if (y == (ypts - 1)) down = 9;
	else down = grid[x][y+1];
}

void outgrid()
{
	for (int y = 0; y < ypts; y++)
	{
		for (int x = 0; x < xpts; x++)
		{
			printf("%d", grid[x][y]);
		}
		printf("\n");
	}
	printf("\n");
}

bool is_low(int p, int u, int d, int l, int r)
{
	if ( (p < u) && (p < d) && (p < l) && (p < r) ) return true;
	return false;
}

int lowgridsums()
{
	int sum = 0;
	int	up, down, left, right;
	for (int y = 0; y < ypts; y++)
	{
		for (int x = 0; x < xpts; x++)
		{
			getadjs(x, y, up, down, left, right);
			int pt = grid[x][y];
			if (is_low(pt, up, down, left, right))
			{
			    sum += pt + 1;
			    printf("[%d][%d]: %d   u: %d  d: %d  l: %d  r: %d\n",
					x, y, pt, up, down, left, right);
			}
		}
	}
	return sum;
}

int init(FILE *f)
{
	char c[MAXLINE];
	fgets(c, MAXLINE, f);

	while (!feof(f))
	{
		parseline(c);
		fgets(c, MAXLINE, f);
	}
	outgrid();
	return lowgridsums();
}


int main(int argc, char **argv)
{
	FILE *f = fopen(argv[1], "r");

	printf("Sum of all lows: %d\n", init(f));

	return 0;
}
