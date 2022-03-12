#include <stdio.h>

#include <stdint.h>

void	result(int day, int part, int ans, int exp_ans)
{
	printf("Day %2.2d - Part %d - Answer: %d", day, part, ans);
	if (ans == exp_ans) 
		printf("  --  CORRECT!!\n");
	else
		printf("  ERROR\n    -- expected answer: %d\n", exp_ans);
}

void	result64(int day, int part, int64_t ans, int64_t exp_ans)
{
	printf("Day %2.2d - Part %d - Answer: %ld", day, part, ans);
	if (ans == exp_ans) 
		printf("  --  CORRECT!!\n");
	else
		printf("  ERROR\n   -- expected answer: %ld\n", exp_ans);
}
