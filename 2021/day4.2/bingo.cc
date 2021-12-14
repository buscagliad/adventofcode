#include <vector>
#include <stdio.h>

class	cell {
	public:
		cell(int r, int c, int v) { row = r; col = c; val = v; marked = false;};
		bool is_marked() {return marked;};
		void set_mark() { marked = true;};
		void clear_mark() { marked = false;};
		int  value() { return val;};
	private:
		int		row;
		int		col;
		int		val;
		bool	marked;
};

#define	NUM_ROWS 5
#define NUM_COLS 5
#define NO_SOLUTION -1

class	bingo {
	public:
		bingo(FILE *f);
		bool	mark(int val);	// returns true if row/col bingo
		int		unmarked_sum();
		int		marked_sum();
		bool	is_bingo();	// returns true if row or column bingo
		void	out();
	private:
		cell	*board[NUM_ROWS][NUM_COLS];
		bool	is_row_bingo(int r);	// returns true if row r is a bingo
		bool    is_col_bingo(int c);	// returns true if col c is a bingo
};

bingo::bingo(FILE *f)
{
	int	r = 0;
	int	c = 0;
	int	v1, v2, v3, v4, v5;
	for (r = 0; r < NUM_ROWS; r++)
	{
		fscanf(f, "%d %d %d %d %d\n", &v1, &v2, &v3, &v4, &v5);
		board[r][0] = new cell(r, 0, v1);
		board[r][1] = new cell(r, 1, v2);
		board[r][2] = new cell(r, 2, v3);
		board[r][3] = new cell(r, 3, v4);
		board[r][4] = new cell(r, 4, v5);
	}
}

void	bingo::out()
{
	for (int r = 0; r < NUM_ROWS; r++)
	{
		for (int c = 0; c < NUM_COLS; c++)
		{
			printf("%2d%c ", board[r][c]->value(),
					board[r][c]->is_marked() ? '*' : ' ');
		}
		printf("\n");
	}
	printf("\n");
}

bool	bingo::mark(int val)	// returns true if row/col bingo
{
	for (int r = 0; r < NUM_ROWS; r++)
	{
		for (int c = 0; c < NUM_COLS; c++)
		{
			if (board[r][c]->value() == val)
				board[r][c]->set_mark();
		}
	}
}
	
int		bingo::unmarked_sum()
{
	int sum = 0;
	for (int r = 0; r < NUM_ROWS; r++)
	{
		for (int c = 0; c < NUM_COLS; c++)
		{
			if (!board[r][c]->is_marked())
				sum += board[r][c]->value();
		}
	}
	return sum;
}

int		bingo::marked_sum()
{
	int sum = 0;
	for (int r = 0; r < NUM_ROWS; r++)
	{
		for (int c = 0; c < NUM_COLS; c++)
		{
			if (board[r][c]->is_marked())
				sum += board[r][c]->value();
		}
	}
	return sum;
}

bool	bingo::is_row_bingo(int r)	// returns true if row r is a bingo
{
	int count = 0;
	for (int c = 0; c < NUM_COLS; c++)
	{
		if (board[r][c]->is_marked())
			count++;
	}
	return count >= NUM_COLS;
}

bool    bingo::is_col_bingo(int c)	// returns true if col c is a bingo
{
	int count = 0;
	for (int r = 0; r < NUM_ROWS; r++)
	{
		if (board[r][c]->is_marked())
			count++;
	}
	return count >= NUM_ROWS;
}

bool	bingo::is_bingo()	// returns true if row or column bingo
{
	for (int c = 0; c < NUM_COLS; c++)
	{
		if (is_col_bingo(c)) return true;
	}
	for (int r = 0; r < NUM_ROWS; r++)
	{
		if (is_row_bingo(r)) return true;
	}
	return false;
}


int main(int argc, char **argv)
{
	int		balls[100];
	int		ball_count = 0;
	char	line[500];
	FILE	*f = fopen(argv[1], "r");
	fgets(line, 500, f);
	std::vector<bingo> boards;
	std::vector<int> numbers;
	
	char *p = line;
	int	v = 0;
	while ( (*p != '\n') || !(*p) )
	{
		if (*p == ',')
		{
			numbers.push_back(v);
			v = 0;
			p++;
			continue;
		}
		v = 10 * v + ((*p) - '0');
		p++;
	}
	
	numbers.push_back(v);

	std::vector<int>::iterator ni = numbers.begin();
//	for (; ni != numbers.end(); ++ni)
//	    printf("Number is: %d\n", *ni);
	    
	while (!feof(f))
	{
		bingo	b(f);
		boards.push_back(b);
	}
	std::vector<bingo>::iterator it = boards.begin();
	int	board_count = boards.size();
	for (ni = numbers.begin(); ni != numbers.end(); ++ni)
	{
		for (it = boards.begin(); it != boards.end(); ++it)
		{
			if (it -> is_bingo()) continue;
			it -> mark(*ni);

			if (it -> is_bingo()) 
			{
				it -> out();
				printf("BINGO!!!!!!!\n\n");
				int	msum = it->marked_sum();
				int usum = it->unmarked_sum();
				int fnum = *ni;
				printf("Final number: %d\n", fnum);
				printf("Sum unmarked: %d\n", usum);
				printf("Product: %d\n", fnum * usum);
				board_count --;
				if (board_count == 0) return 0;
			}
		}
	}
	
}
