#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>
#include <cstring>
#include <string>

using namespace std;
#define MAXX 2000
#define MAXY 2000


int	grid[MAXX][MAXY];
int xpts = 0;
int ypts = 0;

#define BLANK '.'
#define EAST  '>'
#define SOUTH 'v'

int inf_value = BLANK;

#define MAXLINE 1000
///////////////////////////////////////////////////////////////////
// DEBUG outgrid outputs the grid to stdout
///////////////////////////////////////////////////////////////////

/*

 .......................
 .......................
 .......................
 .......................
*/



void outgrid(int g[MAXX][MAXY], int xs, int ys)
{

	printf("GRID  X: %d  Y: %d\n", xs, ys);
	for (int y = 0; y < ys; y++)
	{
		for (int x = 0; x < xs; x++)
		{
			printf("%c", g[x][y]);
		}
		printf("\n");
	}
	printf("\n");
}


void zerodata()  
{
	for(int i = 0; i < MAXX; i++) 
	    for(int j = 0; j < MAXY; j++)
	    {
			grid[i][j] = BLANK;
		}
	xpts = 0;
	ypts = 0;
}


void add_slug(int g[MAXX][MAXY], int & xp, int & yp, char *s)
{
	int i;
	for (i = 0; *s != '\n'; i++, s++)
	{
		g[i][yp] = *s;
	}
	xp = i;
	yp++;
}

void parseline(FILE *f)
{
	char s[MAXLINE];

	//fgets(s, MAXX, f);
	ypts = 0;
	xpts = 0;
	while (!feof(f))
	{
		fgets(s, MAXLINE, f);
		if (feof(f)) break;
		add_slug(grid, xpts, ypts, s);
	}

}

int	*SPACE(int g[MAXX][MAXY], int x, int y, int xp, int yp)
{
	if ( x >= xp ) x = 0;
	if ( y >= yp ) y = 0;
	return &(g[x][y]);
}

int move(int g[MAXX][MAXY], int xp, int yp, bool east)	// east == true -> move east, 
{														// else move south
	char	SLUG;
	int		xdelta = 0;
	int		ydelta = 0;
	int		move_count = 0;
	vector<int*> from_spaces;
	vector<int*> to_spaces;
	if (east)
	{
		SLUG = EAST;
		xdelta = 1;
	}
	else
	{
		SLUG = SOUTH;
		ydelta = 1;
	}
	//
	// find all of the addresses holding a slug that can move and
	// the address of the cell it can move to
	for (int y = 0; y < yp; y++)
	{
		for (int x = 0; x < xp; x++)
		{
			if(g[x][y] == SLUG)
			{
				int	*t = SPACE(g, x+xdelta, y+ydelta, xp, yp);
				if (*t == BLANK) 
				{
					to_spaces.push_back(t);
					from_spaces.push_back(&(g[x][y]));
				}
			}
				    
		}
	}
	// move SLUG from -> to
	vector<int*>::iterator	fi = from_spaces.begin();
	vector<int*>::iterator  ti = to_spaces.begin();
	while (fi != from_spaces.end() && ti != to_spaces.end())
	{
		*(*ti) = *(*fi);
		*(*fi) = BLANK;
		ti++;
		fi++;
		move_count++;
	}
	return move_count;
}

int	move()
{
	return move(grid, xpts, ypts, true) +
		   move(grid, xpts, ypts, false);
}

void solve(const char *v, int true_lights, int loops)
{
	FILE *f = fopen(v, "r");

	zerodata();

	parseline(f);
	printf("Input file: %s\n", v);
	outgrid(grid, xpts, ypts);
	int num_moves = -1;
	int steps = 0;
	while (num_moves != 0)
	{
		num_moves = move();
		outgrid(grid, xpts, ypts);
		steps++;
		printf("Number of steps: %d - moves: %d\n", steps, num_moves);
	}
	outgrid(grid, xpts, ypts);
	printf("Number of steps: %d\n", steps);
	fclose(f);
}

int main(int argc, char **argv)
{
	if (argc == 1)
	{
		solve("data.txt", 5203, 2);
		solve("data.txt", 18806, 50);
		return 1;
	}
	const char *fname;
	int loop;
	if (argc < 2) fname = "ex.txt";
	else fname = argv[1];
	if (argc < 3) loop = 2;
	else loop = atoi(argv[2]);
	solve(fname, 5180, loop);
	return 0;
}
