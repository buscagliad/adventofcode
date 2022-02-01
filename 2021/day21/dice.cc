#include <stdio.h>


int num_rolls = 0;
int dice_value = 0;


int get_dice()
{
	num_rolls++;
	dice_value++;
	if (dice_value > 100) dice_value = 1;
	return dice_value;
}


int	get_roll()
{
	int val = 0;
	val += get_dice();
	val += get_dice();
	val += get_dice();
	return val;
}

int	p1 = 4;
int p2 = 8;
class player {
	public:
		player(int id, int start) {_id = id; _pos = start; };
		void move(int N) { _pos = (_pos + N) % 10; if (_pos == 0) _pos = 10; _score += _pos; };	// returns true if score > N
		void move(int d1, int d2, int d3) { move(d1 + d2 + d3); 
					printf("Player %d  rolls %d+%d+%d and moves to space %d for a total score of %d\n", _id,    d1, d2, d3, _pos, _score); };
		int score() { return _score; };
		bool won() { if (_score >= 1000) return true; return false; };
		void out() { printf("Player %d  at space %d for a total score of %d\n", _id, _pos, _score); };
	private:
		int	_pos;
		int _score;
		int _id;
};

int main(int argc, char **argv)
{
	player	*p[1000];
	int		num_p = 2;
	int     won_p;
	p[0] = new player(1, 10);
	p[1] = new player(2, 8);
	
	bool	done = false;
	while (!done)
	{
		for (int i = 0; i < num_p; i++)
		{
			p[i]->move(get_dice(), get_dice(), get_dice());
			if (p[i]->won())
			{
				won_p = i;
				done = true;
				break;
			}
		}
	}
	int  loser_points = 0;
	for (int i = 0; i < num_p; i++)
	{
		if (i == won_p) continue;
		loser_points += p[i]->score();
	}
	int	answer = loser_points * num_rolls;
	printf("Winner is player %d  with %d points\n", won_p +1, p[won_p]->score());
	printf("Losing player(s) points: %d\n", loser_points);
	printf("Number of rolls: %d\n", num_rolls);
	printf("Answer: %d\n", answer);
	return 1;
	
}
