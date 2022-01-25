#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>
#include <cstring>
#include <string>

using namespace std;
#define MAXX 1000
#define MAXY 1000
#define MAX_RV 88888

int	s_grid[MAXX][MAXY];
int	g_grid[MAXX][MAXY];

int  g_nx = 0;
int  g_ny = 0;

int xpts = 0;
int ypts = 0;
#define NOT_SET -1
int save_first = 0;
#define MAXLINE 1000
///////////////////////////////////////////////////////////////////
// DEBUG outgrid outputs the grid to stdout
///////////////////////////////////////////////////////////////////
void outgrid(int g[MAXX][MAXY], int nx, int ny)
{
	printf("GRID  X: %d  Y: %d\n", nx, ny);
	for (int y = 0; y < ny; y++)
	{
		for (int x = 0; x < nx; x++)
		{
			printf("%2d", g[x][y]);
		}
		printf("\n");
	}
	printf("\n");
}



bool mindval(int g[MAXX][MAXY], int s[MAXX][MAXY], int nx, int ny, int x, int y)
{
	bool	rv = false;
	int	sumv = 0;
	if (s[x][y] != NOT_SET)
	{
        if (x - 1 >= 0) // LEFT
        {
            sumv = s[x][y] + g[x-1][y];
            if ( (sumv < s[x-1][y]) || (s[x-1][y] == NOT_SET) )
            {
                s[x-1][y] = sumv;
                rv = true;
            }
        }
        if (x + 1 < nx) // RIGHT
        {
            sumv = s[x][y] + g[x+1][y];
            if ( (sumv < s[x+1][y]) || (s[x+1][y] == NOT_SET) )
            {
                s[x+1][y] = sumv;
                rv = true;
            }
        }
        if (y - 1 >= 0) // ABOVE
        {
            sumv = s[x][y] + g[x][y-1];
            if ( (sumv < s[x][y-1]) || (s[x][y-1] == NOT_SET) )
            {
                s[x][y-1] = sumv;
                rv = true;
            }
        }
        if (y + 1 < ny) // BELOW
        {
            sumv = s[x][y] + g[x][y+1];
            if ( (sumv < s[x][y+1]) || (s[x][y+1] == NOT_SET) )
            {
                s[x][y+1] = sumv;
                rv = true;
            }
        }
	}
	return rv;
}

int route(int g[MAXX][MAXY], int s[MAXX][MAXY], int nx, int ny)
{
	save_first = g[0][0];
	g[0][0] = 0;
	s[0][0] = 0;
	bool done = false;
	while (!done)
	{
		done = true;
		for (int x = 0; x < nx; x++)
		{
			for (int y = 0; y < ny; y++)
			{
				if (mindval(g, s, nx, ny, x, y))
				    done = false;
			}
			//outgrid(g, nx, ny);
		}
	}
	return s[nx-1][ny-1];
}

void zerodata()  
{
	for(int i = 0; i < MAXX; i++) 
	    for(int j = 0; j < MAXY; j++)
	    {
			g_grid[i][j] = 0;
			s_grid[i][j] = NOT_SET;	// set the sum-path to not be set
		}
	xpts = 0;
	ypts = 0;
	
}

void parseline(char *c)
{
	int   x = 0;
	int   y = ypts;
	while (*c != '\n')
	{
		g_grid[x++][y] = *c - '0';
		c++;
	}
	ypts++;
	xpts = x;
}

void init(const char *v)
{
	FILE *f = fopen(v, "r");

	printf("Input file: %s\n", v);
	char c[MAXLINE];
	fgets(c, MAXLINE, f);
	zerodata();
	while (!feof(f))
	{
		parseline(c);
		fgets(c, MAXLINE, f);
	}
	
	g_nx = xpts;
	g_ny = ypts;
	//outgrid(g_grid, g_nx, g_ny);
	fclose(f);
}

void solve(int trisk)
{
	int my_risk = 0;
	my_risk = route(g_grid, s_grid, g_nx, g_ny);
	//outgrid(s_grid, g_nx, g_ny);

	printf("Risk level: %d\n", my_risk);
	if (trisk > 0)
	{
		if (my_risk != trisk)
			printf("ERROR - risk answer does not agree with truth: %d!\n", trisk);
		else
			printf("Successfully esimated risk level!!\n");
	}

}

#define NEXT(n)	((n) < 9 ? n + 1 : 1)
void fill_five(int xs, int ys)
{
	//int v = g_grid[xs][ys];
	//printf("xs: %d  ys: %d  v: %d\n", xs, ys, v);
	for (int i = 1; i < 5; i++)
	{
	    g_grid[xs + i * g_nx][ys] = NEXT(g_grid[xs + (i - 1) * g_nx][ys]); // fill right
	}
	for (int i = 0; i < 5; i++)
	{
		for (int j = 1; j < 5; j++)
		{
			g_grid[xs + i * g_nx][ys + j * g_ny] = NEXT(g_grid[xs + i * g_nx][ys + (j - 1) * g_ny]);
		}
	}
}
	

void new_matrix()
{
	g_grid[0][0] = save_first;
	for (int i = 0;  i < g_nx; i++)
	{
	    for (int j = 0; j < g_ny; j++)
	    {
			fill_five(i, j);
		}
	}
	g_nx *= 5;
	g_ny *= 5;
}

int main(int argc, char **argv)
{
	//solve("ex.txt", 15, 1134);
    //printf("\n\n");
	//solve("data.txt", 588, 964712);
	init("ex.txt");
	printf("Example for part 1\n");
	solve(40);
	printf("Example for part 2\n");
	new_matrix();
	solve(315);
	init(argv[1]);
	printf("Example for part 1\n");
	solve(458);
	new_matrix();
	printf("Example for part 2\n");
	//outgrid(g_grid, g_nx, g_ny);
	solve(2800);
	

	return 0;
}
