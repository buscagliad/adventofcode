#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>
#include <cstring>
#include <string>

using namespace std;
#define MAXX 2000
#define MAXY 2000
#define MIDX 0
#define MIDY 0
#define STARTX 0
#define STARTY 0

int	gmap[MAXX];
int	gridA[MAXX][MAXY];
int gridB[MAXX][MAXY];
int xpts = 0;
int ypts = 0;

#define BLANK '.'
#define MARK  '#'

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

void set_infinite()
{
	if (inf_value == BLANK)	// odd
	{
		inf_value = gmap[0];
	}
	else if (inf_value == MARK)
	{
		inf_value = gmap[511];
	}
	printf("Inf value: %c\n", inf_value);
}

int BIT(int x, int y)
{
	if (x < 0) return inf_value;
	if (y < 0) return inf_value;
	if (x >= xpts) return inf_value;
	if (y >= ypts) return inf_value;
	return gridA[x][y];
}
	
void print3x3(int g[MAXX][MAXY], int x, int y)
{
	int val = 0;
	int pwr = 256;
	printf("  x: %d   y: %d\n", x, y);
	for (int j = -1; j <=1; j++)
	{
		for (int i = -1; i <= 1; i++)
		{
			int	v = BIT(x + i, y + j);
			if (v == MARK) val += pwr;
			pwr /= 2;
			printf("%c ", v);
		}
		if (j == 1)
		    printf("   val: %d", val);
		else
			printf("\n");
	}
}
			

int	newval(int g[MAXX][MAXY], int *img, int x, int y)
{
	int val = 0;
	int pwr = 1;
	for (int j = y + 1; j >= y - 1; j--)
	{
		for (int i = x + 1; i >= x - 1; i--)
		{
			if (BIT(i, j) == MARK) val += pwr;
			pwr *= 2;
		}
	}
	print3x3(g, x, y);
	printf ("   oval: %4d   char: %c\n", val, img[val]);
	return img[val];
}

void    update_image(int from[MAXX][MAXY], int to[MAXX][MAXY], int & nx, int & ny, int *img)
{
	ny += 2;
	nx += 2;
	//shift(from, nx, ny);
	for (int j = 0; j < ny; j++)
	{
		for (int i = 0; i < nx; i++)
		{
			to[i][j] = newval(from, img, i, j);
		}
	//printf("\n");
	}
}



#define IMAGE_SHIFT 4

void shift(int g[MAXX][MAXY], int &xp, int &yp)
{
	xp += 2;
	yp += 2;
	int shift_value = inf_value;
	for (int i = xp + 1; i >= 0; i--)
		//outgrid(gridA, xpts, ypts);
		update_image(gridA, gridB, xpts, ypts, gmap);
		copy(gridA, gridB);
		outgrid(gridA, xpts, ypts);
		set_infinite();
	}

	int num_lights = gridcount(gridA);
	printf("Number of lights: %d\n", num_lights);
	if (true_lights > 0)
	{
		if (num_lights != true_lights)
			printf("ERROR - light count does not agree with truth: %d!\n", true_lights);
		else
			printf("Successfully counted lights!!\n");
	}

	fclose(f);
}

int main(int argc, char **argv)
{
	const char *fname;
	if (argc < 2) fname = "ex2.txt";
	else fname = argv[1];
	solve(fname, 5180, 2);
	return 0;
}
