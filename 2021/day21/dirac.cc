#include <stdio.h>
#include <stdint.h>

// each play requires 3 rolls of the dice, which will create 27 universes
// the rolls are as follows:
//    1  total of 3
//    3  total of 4
//    6  total of 5
//    7  total of 6
//    6  total of 7
//    3  total of 8
//    1  total of 9

uint64_t	inc_pos(uint64_t cur_pos, uint64_t roll)
{
	cur_pos += roll;
	if (cur_pos > 10) cur_pos -= 10;
	return cur_pos;
}

#define PLAYER2(n, U)	NextPosition = inc_pos(player_2_pos, n);	\
						NextScore = player_2_score + NextPosition;	\
					if (NextScore >= 21) player_2_wins += U * num_universes; \
					else roll_dirac( player_1_pos,  player_1_score,  player_1_wins,					\
				                     NextPosition,  NextScore,  player_2_wins,				\
				                     1, U * num_universes); 

#define PLAYER1(n, U)	NextPosition = inc_pos(player_1_pos, n);	\
						NextScore = player_1_score + NextPosition;	\
					if (NextScore >= 21) player_1_wins += U * num_universes; \
					else roll_dirac( NextPosition,  NextScore,  player_1_wins,					\
				                     player_2_pos,  player_2_score,  player_2_wins,				\
				                     2, U * num_universes); 

void	roll_dirac(uint64_t player_1_pos, uint64_t player_1_score, uint64_t &player_1_wins,
				   uint64_t player_2_pos, uint64_t player_2_score, uint64_t &player_2_wins,
				   int which_player, uint64_t num_universes)
{
	uint64_t	NextPosition;
	uint64_t	NextScore;
	
	if (which_player == 1)
	{			
		// rolls adding to 3 (only 1)
		PLAYER1(3, 1);
		
		// rolls adding to 4 (3)
		PLAYER1(4, 3);
		
		// rolls adding to 5 (6)
		PLAYER1(5, 6);

		// rolls adding to 6 (7)
		PLAYER1(6, 7);

		// rolls adding to 7 (6)
		PLAYER1(7, 6);
		
		// rolls adding to 8 (3)
		PLAYER1(8, 3);

		// rolls adding to 9 (only 1)
		PLAYER1(9, 1);
	}
	else // (which_player == 2)
	{			
		// rolls adding to 3 (only 1)
		PLAYER2(3, 1);
		
		// rolls adding to 4 (3)
		PLAYER2(4, 3);
		
		// rolls adding to 5 (6)
		PLAYER2(5, 6);

		// rolls adding to 6 (7)
		PLAYER2(6, 7);

		// rolls adding to 7 (6)
		PLAYER2(7, 6);
		
		// rolls adding to 8 (3)
		PLAYER2(8, 3);

		// rolls adding to 9 (only 1)
		PLAYER2(9, 1);
	}
}

void	dirac_run(int p1_start, int p2_start,
				uint64_t p1_expected_wins, uint64_t p2_expected_wins)
{
	uint64_t	player_1_wins = 0;
	uint64_t	player_2_wins = 0;
	int 		player_1_pos = p1_start;
	int 		player_1_score = 0;
	int 		player_2_pos = p2_start;
	int 		player_2_score = 0;
	uint64_t	num_universes = 1; // initially - we have only 1
	
	// test
	roll_dirac( player_1_pos,  player_1_score,  player_1_wins,
			    player_2_pos,  player_2_score,  player_2_wins,
				1,  num_universes);
	printf("Player 1 starting position: %d\n", p1_start);
	printf("Player 2 starting position: %d\n\n", p2_start);
	printf("Player 1 wins %lu games\n", player_1_wins);
	if (player_1_wins == p1_expected_wins)
		printf("Correct solution for player 1!!\n");
	else
		printf("Inorrect solution for player 1 - expecting %lu\n", p1_expected_wins);
	printf("Player 2 wins %lu games\n", player_2_wins);
	if (player_2_wins == p2_expected_wins)
		printf("Correct solution for player 2!!\n");
	else
		printf("Inorrect solution for player 2 - expecting %lu\n", p2_expected_wins);
}

int main(int argc, char **argv)
{
	
	// test
	printf("Sample run...\n");
	dirac_run(4, 8, 444356092776315, 341960390180808);
	printf("\n\nFinal run...\n");
	dirac_run(10, 8, 444356092776315, 341960390180808);
				
	return 1;
	
}
