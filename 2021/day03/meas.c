#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "log.hh"

#define DEBUG 0
#define MAXBIT 50
#define MAXNUM 2000

/*
 * returns a 0 or 1 depending on which value is most prevalent
 * at the position of the mask
 */
int max_value(char v[MAXNUM][MAXBIT], int n, int mask,
				char high[MAXNUM][MAXBIT], int *high_count,
				char low[MAXNUM][MAXBIT], int *low_count)
{
	int	i;
	char	**ones = (char **) malloc(n * sizeof(char *));
	int  ones_count = 0;
	char	**zeroes = (char **)  malloc(n * sizeof(char *));
	int  zeroes_count = 0;
	
	for (i = 0; i < n; i++)
	{
		if (DEBUG) printf("%4d  Value: %s\n", i, v[i]);
	}
	

	for (i = 0; i < n; i++)
	{
		if (v[i][mask] == '1')
		{
			 ones[ones_count++] = v[i];
		}
		else 
		{
			zeroes[zeroes_count++] = v[i];
		}
	}

	if (zeroes_count > ones_count)
	{
		*high_count = zeroes_count;
		*low_count = ones_count;
		for (i = 0; i < zeroes_count; i++)
			strcpy(high[i], zeroes[i]);
		for (i = 0; i < ones_count; i++)
			strcpy(low[i], ones[i]);

		return 0;
	}
	else
	{
		*low_count = zeroes_count;
		*high_count = ones_count;
		for (i = 0; i < zeroes_count; i++)
			strcpy(low[i], zeroes[i]);
		for (i = 0; i < ones_count; i++)
			strcpy(high[i], ones[i]);

	}
		
	return 1;
}

int	bvalue(char v[MAXBIT])
{
	int	nbits = strlen(v) - 1;
	int pwr2 = 1;
	int	val = 0;
	for (; nbits >= 0; nbits--, pwr2 *= 2)
	    if (v[nbits] == '1') val += pwr2;
	return val;
}

void	part1(FILE *f, int answer)
{
    char  cmd[100];
    int   onebitcnt[MAXBIT];
    int   zerobitcnt[MAXBIT];
    int   errorbitcnt[MAXBIT];
    int   i;
    int	  gamma_rate = 0;
    int   eps_rate = 0;
    int	  pwr_two = 1;
    int   err_rate = 0;
    rewind(f);
    for (i = 0; i < MAXBIT; i++)
    {
		onebitcnt[i] = 0;
		zerobitcnt[i] = 0;
		errorbitcnt[i] = 0;
	}

    fscanf(f, "%s\n", cmd);
    while (!feof(f))
    {
		for (i = 0; i < (int)strlen(cmd); i++)
		{
			if (cmd[i] == '0') 
			    zerobitcnt[i]++;
			else if (cmd[i] == '1')
				onebitcnt[i]++;
			else
				errorbitcnt[i]++;
		}
		fscanf(f, "%s\n", cmd);
	}
	for (i = strlen(cmd) - 1; i >= 0; i--)
	{
		if (onebitcnt[i] > zerobitcnt[i])
		    gamma_rate += pwr_two;
		else if (onebitcnt[i] < zerobitcnt[i])
		    eps_rate += pwr_two;
		else
		    err_rate += pwr_two;
		pwr_two *= 2;
	}
    if (DEBUG) printf("Gamma: %d\n", gamma_rate);
    if (DEBUG) printf("Eps: %d\n", eps_rate);
    if (DEBUG) printf("ERR: %d\n", err_rate);
    if (DEBUG) printf("Product: %d\n", gamma_rate * eps_rate);
    result(3, 1, gamma_rate * eps_rate, answer);
}

void part2(FILE *f, int ans)
{
    int   i;
    char  values[MAXNUM][MAXBIT];
    int   val_num = 0;
	int	  num_bits = 0;
    int   digit = 0;

    rewind(f);
    fscanf(f, "%s", values[0]);
    num_bits = strlen(values[0]);
    while (!feof(f))
    {
		val_num++;
		fscanf(f, "%s", values[val_num]);
	}
	for (i = 0; i < val_num; i++)
	{
		if (DEBUG) printf("%4d  Value: %s\n", i, values[i]);
	}
//	char	*ox[MAXBIT], *c02[MAXBIT];
	char	ox[MAXNUM][MAXBIT], c02[MAXNUM][MAXBIT];
	int ox_c, c02_c;
	max_value(values, val_num, 0,
			ox, &ox_c, c02, &c02_c);
	
	for (i = 0; i < ox_c; i++)
	{
		if (DEBUG) printf("%4d  OX  Value: %s\n", i, ox[i]);
	} 
	for (i = 0; i < c02_c; i++)
	{
		if (DEBUG) printf("%4d  CO2  Value: %s\n", i, c02[i]);
	} 
	/*
	 * Get oxygen values ...
	 */
	for (digit = 1; ox_c > 1 && digit < num_bits; digit++)
	    max_value(ox, ox_c, digit,
			ox, &ox_c, c02, &c02_c);
    if (DEBUG) printf("Oxygen: %s\n", ox[0]);
    int ox_level = bvalue(ox[0]);
	/*
	 * Get c02 values ...
	 */
	max_value(values, val_num, 0,
			ox, &ox_c, c02, &c02_c);
	for (digit = 1; c02_c > 1 && digit < num_bits; digit++)
	    max_value(c02, c02_c, digit,
			ox, &ox_c, c02, &c02_c);
    if (DEBUG) printf("CO2: %s\n", c02[0]);
    int co2_level = bvalue(c02[0]);
	
    if (DEBUG) printf("Oxygen: %d\n", ox_level);
    if (DEBUG) printf("C02: %d\n", co2_level);
    if (DEBUG) printf("Product: %d\n", ox_level * co2_level);
    result(3, 2, ox_level * co2_level, ans);
}

int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "r");
	part1(f, 845186);
	part2(f, 4636702);
    return 0;
}
