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

#define BLANK ' '
#define MARK  '#'

#define MAXLINE 1000
///////////////////////////////////////////////////////////////////
// DEBUG outgrid outputs the grid to stdout
///////////////////////////////////////////////////////////////////

void outgridcsv(const char *csvf)
{
	FILE *f = fopen(csvf, "w");
	fprintf(f, "%d, %d\n", xpts, ypts);
	for (int y = 0; y < ypts; y++)
	{
		for (int x = 0; x < xpts; x++)
		{
			fprintf(f, "%c,", grid[x][y]);
		}
		fprintf(f,"\n");
	}
	fprintf(f,"\n");
	fclose(f);
}
void outgrid()
{
	char	fname[400];
	sprintf(fname, "GRID_%d_%d.csv", xpts, ypts);
	outgridcsv(fname);
	printf("GRID  X: %d  Y: %d\n", xpts, ypts);
	for (int y = 0; y < ypts; y++)
	{
		for (int x = 0; x < xpts; x++)
		{
			printf("%c", grid[x][y]);
		}
		printf("\n");
	}
	printf("\n");
}

int	gridcount()
{
	int sum = 0;
	for (int y = 0; y < ypts; y++)
	{
		for (int x = 0; x < xpts; x++)
		{
			if(grid[x][y] == MARK) sum++;
		}
	}
	return sum;
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

//#define GRID(x,y)	( ((x >= 0) && (y >= 0) && (x < xpts) && (y < ypts) ) ? grid[x][y] : BLANK)
//#define MAP(x1, y1, x2, y2)	( ( (GRID(x1,y1) == MARK) || (GRID(x2,y2) == MARK) ) ? MARK : BLANK)


char GRID(int x, int y)
{
	if ((x >= 0) && (y >= 0) && (x < xpts) && (y < ypts) ) 
	    return grid[x][y];
	printf("OUT OF BAND: (x,y) = (%d,%d) for GRID: %d x %d\n", x, y, xpts, ypts);
	return BLANK;
}

char MAP(int x1, int y1, int x2, int y2)
{
	if (GRID(x1, y1) == MARK) return MARK;
	if (GRID(x2, y2) == MARK) return MARK;
	return BLANK;
}

#define XFOLD 1
#define YFOLD 2

int map(int x1, int y1, int x2, int y2, int ft)
{
	if ( (ft == XFOLD) && (x1 == x2) ) return BLANK;
	if ( (ft == YFOLD) && (y1 == y2) ) return BLANK;
	return MAP(x1, y1, x2, y2);
}

void fold(int x, int y)
{
	if (x == 0)  // fold is along y - axis
	{
		printf("Y Fold at y = %d   ypts = %d", y, ypts);
		int ystart = (ypts - 2 * y);
		int y2 = y + 1;
		for (int y1 = y - 1; y1 >= 0 ; y1--)
		{
			for (int i = 0; i < xpts; i++)
			{
				grid[i][y1] = map(i, y1, i, y2, YFOLD);
				//printf("%d,%d  %d,%d  %c\n", i, j, i, ypts - j - 1, grid[i][j]);
			}
			y2++;
		}
		printf("   New ypts = %d  ystart = %d\n", ypts, ystart);
		ypts = y;
	}
	else if (y == 0) // fold is along x - axis
	{
		int xstart = (xpts - 2 * x);
		printf("X Fold at x = %d   xpts = %d", x, xpts);
		for (int i = 0; i < x; i++)
		{
			int x2 = xpts - i - 1;
			for (int j = 0; j < ypts; j++)
			{
				grid[i][j] = map(i, j, x2, j, XFOLD);
			}
		}
		printf("   New xpts = %d  xstart = %d\n", xpts, xstart);
		xpts = x;
	}
}

void parseline(FILE *f, int &num_folds)
{
	char s[MAXLINE];
	int	x, y;
	fgets(s, MAXLINE, f);
	if (feof(f) || (strlen(s) < 2) ) return;
	char *foldx = strstr(s, "fold along x=");
	char *foldy = strstr(s, "fold along y=");
	if (foldx)
	{
		//outgrid();
		foldx += 13;
		sscanf(foldx, "%d", &x);
		fold(x, 0);
		//printf("X fold: %d::%s", x, foldx);
		num_folds++;
		//outgrid();
	}
	else if (foldy) 
	{
		//outgrid();
		foldy += 13;
		sscanf(foldy, "%d", &y);
		fold(0, y);
		//printf("Y fold: %d::%s", y, foldy);
		num_folds++;
		//outgrid();
	}
	else
	{
		sscanf(s, "%d,%d", &x, &y);
		//printf("x = %d   y = %d\n", x, y);
		grid[x][y] = MARK;
		if (x+1 > xpts) xpts = x+1;
		if (y+1 > ypts) ypts = y+1;
	}
}


void solve(const char *v, int tfolds, int num_folds)
{
	FILE *f = fopen(v, "r");

	zerodata();
	int fold_count = 0;
	while (!feof(f))
	{
		parseline(f, fold_count);
		if (fold_count >= num_folds) break;
	}
	printf("Input file: %s\n", v);
	int my_folds = gridcount();
	printf("Dots after %d folds: %d\n", num_folds, my_folds);
	if (tfolds > 0)
	{
		if (my_folds != tfolds)
			printf("ERROR - dots count does not agree with truth: %d!\n", tfolds);
		else
			printf("Successfully counted dots!!\n");\
	}

	fclose(f);
}

int main(int argc, char **argv)
{
	//solve("ex.txt", 17, 1);
	//solve("data.txt", 638, 1);
    //printf("\n\n");
	//solve("data.txt", 588, 964712);
	//solve("ex.txt", 17, 55);
	//outgrid();
	solve(argv[1], 638, 100);
	outgrid();
	return 0;
}
