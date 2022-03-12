#include <stdlib.h>
#include <stdio.h>
#include "log.hh"

#define DEBUG  0

class	graph {
	public:
		graph(int numx, int numy);
		int		mark(int x, int y) {return (*getp(x, y) )++;};	// increases mark at x/y
		int		count(int minval);	// returns number of cells with >= minval
		int		getv(int x, int y) {return *getp(x, y); };
		void	out();
	private:
		int *getp(int x, int y);
		int	*board;
		int	num_rows;
		int num_cols;
};

int	*graph::getp(int x, int y)
{
	return board + ( (x * num_cols) + y);
}

graph::graph(int nx, int ny)
{
	int	i = 0;
	num_rows = nx + 1;
	num_cols = ny + 1;
	int  MM = num_rows * num_cols;
	board = (int *) malloc(MM * sizeof(int));
	
	for (i = 0; i < MM; i++)
	    board[i] = 0;

}

int	graph::count(int mv)
{
	int rv = 0;
	for (int c = 0; c < num_cols; c++)
	{
		for (int r = 0; r < num_rows; r++)
		{
			if (getv(r, c) >= mv) rv++;
		}
	}
	return rv;
}

void	graph::out()
{
	for (int c = 0; c < num_cols; c++)
	{
		for (int r = 0; r < num_rows; r++)
		{
			char	dot = '0' + getv(r, c);
			if (dot == '0') dot = '.';
			printf("%c", dot);
		}
		printf("\n");
	}
	printf("\n");
}
#define MAXLINE 1000
bool		readline(FILE *f, int *x1, int *y1, int *x2, int *y2)
{
	// read line
	char	l[MAXLINE];
	l[0] = 0;
	if (feof(f)) return false;
	fgets(l, MAXLINE, f);
	// parse x1,y1 -> x2,y2
	if (sscanf(l, "%d,%d -> %d,%d", x1, y1, x2, y2) < 4) return false;
	if (DEBUG) printf("%d,%d -> %d,%d\n", *x1, *y1, *x2, *y2);
	return true;
}

void	fill(graph &g, FILE *f, bool use_diagonals)
{
	rewind(f);
	int	x1, y1, x2, y2;
	while(readline(f, &x1, &y1, &x2, &y2))
	{
		if (x1 == x2) 
		{
			if (y1 < y2)
			    for (int i = y1; i <= y2; i++)
				    g.mark(x1, i);
			else
			    for (int i = y2; i <= y1; i++)
			        g.mark(x1, i);
		}
		else if (y1 == y2)
		{
			if (x1 < x2)
			    for (int i = x1; i <= x2; i++)
				    g.mark(i, y1);
			else
			    for (int i = x2; i <= x1; i++)
			        g.mark(i, y1);
		}
		else if (use_diagonals)
		{
			int dx = (x2 > x1) ? 1 : -1;
			int dy = (y2 > y1) ? 1 : -1;
			g.mark(x1, y1);
			do 
			{
				x1 += dx;
				y1 += dy;
				g.mark(x1, y1);
			} while (x1 != x2);
		}
	}
	rewind(f);
}

void	maxnums(FILE *f, int &max_x, int &max_y)
{
	rewind(f);
	max_x = 0;
	max_y = 0;
	int	x1, y1, x2, y2;
	while(readline(f, &x1, &y1, &x2, &y2))
	{
		if ( (x1 == x2) || (y1 == y2) )
		{
			if (max_x < x1) max_x = x1;
			if (max_x < x2) max_x = x2;
			if (max_y < y1) max_y = y1;
			if (max_y < y2) max_y = y2;
		}
		else
		    if (DEBUG) printf("ratio: %.3f\n", (double)(y2 - y1)/(double)(x2 - x1));
	}
	rewind(f);
}
	

int main(int argc, char **argv)
{
	FILE	*f = fopen(argv[1], "r");
	int		max_x, max_y;
	maxnums(f, max_x, max_y);
	if (DEBUG) printf("MAX X: %d   MAX Y: %d\n", max_x, max_y);
	graph	p1(max_x, max_y);
	graph	p2(max_x, max_y);
	fill(p1, f, false);
	result(4, 1, p1.count(2), 5092);
	if (DEBUG) p1.out();
	fill(p2, f, true);
	result(4, 2, p2.count(2), 20484);
	return 0;
}
