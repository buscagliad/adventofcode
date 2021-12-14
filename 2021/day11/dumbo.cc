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
int nflashes = 0;

#define MAXLINE 1000
///////////////////////////////////////////////////////////////////
// DEBUG outgrid outputs the grid to stdout
///////////////////////////////////////////////////////////////////
void outgrid()
{
	printf("Num flashes: %d\n", nflashes);
	for (int y = 0; y < ypts; y++)
	{
		for (int x = 0; x < xpts; x++)
		{
			printf("%d", grid[x][y]);
		}
		printf("\n");
	}
	printf("\n\n");
}

int sum_grid()
{
	int sum = 0;
	for (int y = 0; y < ypts; y++)
	{
		for (int x = 0; x < xpts; x++)
		{
			sum += grid[x][y];
		}
	}
	return sum;
}


void zerodata()  
{
	for(int i = 0; i < MAXX; i++) 
	    for(int j = 0; j < MAXY; j++)
	    {
			grid[i][j] = 0;
		}
	xpts = 0;
	ypts = 0;
	nflashes = 0;
	
}

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


int	connected(int x, int y, bool prime)
{
	//printf("Connected x: %d   y: %d   grp: %d\n", x, y, grp);
	if ( (x < 0) || (y < 0) || (x >= xpts) || (y >= ypts) ) return 0;
	grid[x][y]++;
	if ( (grid[x][y] <= 9) ) return 0; 
	// grid[x][y] is 10 - time to flash...
	if (grid[x][y] == 10) 
	{
		//printf("[%4d]Setting [%d][%d]::%d to group: %d\n", grp_update, x, y, grid[x][y], grp);
		connected(x-1,y,true);
		connected(x+1,y,true);
		connected(x,y-1,true);
		connected(x,y+1,true);
		connected(x-1,y-1,true);
		connected(x+1,y+1,true);
		connected(x+1,y-1,true);
		connected(x-1,y+1,true);
	}
	return 0;
}

int	zeroflashed()
{
	for (int x = 0; x < xpts; x++)
		for (int y = 0; y < ypts; y++)
		{
			if (grid[x][y] > 9) 
			{
				grid[x][y] = 0;
				nflashes++;
			}
		}
}

void step()
{
	for (int x = 0; x < xpts; x++)
		for (int y = 0; y < ypts; y++)
			connected(x, y, true);
	zeroflashed();
}

void flash_count(const char *v, int num_steps, int tflashes)
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
	//outgrid();
	for (int i = 0; i < num_steps; i++) {
		step();
		//printf("Step: %d\n", i+1);
		//outgrid();
	}
	printf("Input file: %s\n", v);
	printf("Number of flashes: %d\n", nflashes);
	if (tflashes > 0)
	{
		if (nflashes != tflashes)
			printf("ERROR - number of flashes does not agree with truth: %d!\n", tflashes);
		else
			printf("Successfully esimated number of flashes!!\n");\
	}
	/*	dtermine first 'synchronized flash' */
	
	fclose(f);
}

#define MAX_STEPS 20000
void flash_sync(const char *v, int tsteps)
{
	FILE *f = fopen(v, "r");
	int steps = 0;
	char c[MAXLINE];
	fgets(c, MAXLINE, f);
	zerodata();
	while (!feof(f))
	{
		parseline(c);
		fgets(c, MAXLINE, f);
	}
	//outgrid();
	for (int i = 0; i < MAX_STEPS; i++) {
		step();
		if (sum_grid() == 0)
		{
			steps = i+1;
			break;
		}
	}
	printf("Input file: %s\n", v);
	printf("Number of steps: %d\n", steps);
	if (tsteps > 0)
	{
		if (steps != tsteps)
			printf("ERROR - number of steps to synch does not agree with truth: %d!\n", tsteps);
		else
			printf("Successfully esimated number of steps!!\n");\
	}
	/*	dtermine first 'synchronized flash' */
	
	fclose(f);
}

int main(int argc, char **argv)
{
	flash_count("ex.txt", 100, 1656);
	flash_sync("ex.txt", 195);
    printf("\n\n");
	flash_count("data.txt", 100, 1793);
	flash_sync("data.txt", 247);

	return 0;
}
