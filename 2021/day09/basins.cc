#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>
#include <cstring>
#include <string>

using namespace std;
#define MAXX 200
#define MAXY 200
#define MAXBASINS 1000
int	grid[MAXX][MAXY];
int	group[MAXX][MAXY];
int basins[MAXBASINS];
int xpts = 0;
int ypts = 0;
int nbasins = 0;

#define MAXLINE 1000
///////////////////////////////////////////////////////////////////
// DEBUG outgrid outputs the grid to stdout
///////////////////////////////////////////////////////////////////
void outgrid()
{
	printf("GRID  X: %d  Y: %d\n", xpts, ypts);
	for (int y = 0; y < ypts; y++)
	{
		for (int x = 0; x < xpts; x++)
		{
			if (grid[x][y] > 8) printf("   ");
			else printf("%2d ", grid[x][y]);
		}
		printf("\n");
	}
	printf("\n");
}

///////////////////////////////////////////////////////////////////
// DEBUG outgroup outputs the group matrix to stdout
///////////////////////////////////////////////////////////////////
void outgroup()
{
	for (int y = 0; y < ypts; y++)
	{
		for (int x = 0; x < xpts; x++)
		{
			if (group[x][y] == 0) printf("   ");
			else printf("%2d ", group[x][y]);
		}
		printf("\n");
	}
	printf("\n");
}

void zerodata()  
{
	for(int i = 0; i < MAXBASINS; i++) basins[i] = 0;
	for(int i = 0; i < MAXX; i++) 
	    for(int j = 0; j < MAXY; j++)
	    {
			grid[i][j] = 0;
			group[i][j] = 0;\
		}
	xpts = 0;
	ypts = 0;
	nbasins = 0;
	
}

void parseline(char *c)
{
	int   x = 0;
	int   y = ypts;
	while (*c != '\n')
	{
		group[x][y] = 0;
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

int displayTopThree()
{
	int hold;
	for (int i = 1; i <= nbasins - 1; i++)
	{
		for (int j = i+1; j <= nbasins; j++)
		{
			if (basins[i] < basins[j])
			{
				hold = basins[i];
				basins[i] = basins[j];
				basins[j] = hold;
			}
		}
	}
	printf("Top three basins: %d  %d  %d  - Product: %d\n",
	    basins[1], basins[2], basins[3], basins[1] * basins[2] * basins[3]);
	return basins[1] * basins[2] * basins[3];
}

int grp_update = 0;

int	connected(int x, int y, int grp)
{
	//printf("Connected x: %d   y: %d   grp: %d\n", x, y, grp);
	if ( (x < 0) || (y < 0) || (x >= xpts) || (y >= ypts) ) return 0;
	if ( (grid[x][y] == 9)  ) return 0; //|| (grid[x][y] == 0) ) return 0;
	if (group[x][y]) return 0;
	group[x][y] = grp;
	grp_update++;
	//printf("[%4d]Setting [%d][%d]::%d to group: %d\n", grp_update, x, y, grid[x][y], grp);
	connected(x-1,y,grp);
	connected(x+1,y,grp);
	connected(x,y-1,grp);
	connected(x,y+1,grp);
	return 0;
}

void setrecursivegroups()
{
	int grp = 1;
	for (int x = 0; x < xpts; x++)
		for (int y = 0; y < ypts; y++)
		{
			grp_update = 0;
			connected(x, y, grp);
			if (grp_update) grp++;
		}
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
			    //printf("[%d][%d]: %d   u: %d  d: %d  l: %d  r: %d\n",
				//	x, y, pt, up, down, left, right);
			}
		}
	}
	return sum;
}

void createbasins()
{
	for (int y = 0; y < ypts; y++)
	{
		for (int x = 0; x < xpts; x++)
		{
			int g = group[x][y];
			basins[g] ++;
			if (g > nbasins) nbasins = g;
		}
	}
}

void solve(const char *v, int trisk, int ttop3)
{
	FILE *f = fopen(v, "r");

	char c[MAXLINE];
	fgets(c, MAXLINE, f);
	zerodata();
	while (!feof(f))
	{
		parseline(c);
		fgets(c, MAXLINE, f);
	}
	setrecursivegroups();
	createbasins();
	int my_risk = lowgridsums();
	printf("Input file: %s\n", v);
	printf("Risk level: %d\n", my_risk);
	if (trisk > 0)
	{
		if (my_risk != trisk)
			printf("ERROR - risk answer does not agree with truth: %d!\n", trisk);
		else
			printf("Successfully esimated risk level!!\n");\
	}
	int my_top3 = displayTopThree();
	if (ttop3 > 0)
	{
		if (my_top3 != ttop3)
			printf("ERROR - risk answer does not agree with truth: %d!\n", ttop3);
		else
			printf("Successfully esimated basin value!!\n");
	}
	fclose(f);
}

int main(int argc, char **argv)
{
	solve("data.txt", 588, 964712);

	return 0;
}
