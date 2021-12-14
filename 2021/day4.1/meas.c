#include <stdio.h>
#include <string.h>
#include <stdlib.h>

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
		printf("%4d  Value: %s\n", i, v[i]);
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

int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "r");
    char  cmd[100];
    int   i;
    int	  oxygen = 0;
    int	  pwr_two = 1;
    int   err_rate = 0;
    char  values[MAXNUM][MAXBIT];
    int   val_num = 0;
	int	  num_bits = 0;
    int   digit = 0;

    fscanf(f, "%s", values[0]);
    num_bits = strlen(values[0]);
    while (!feof(f))
    {
		val_num++;
		fscanf(f, "%s", values[val_num]);
	}
	for (i = 0; i < val_num; i++)
	{
		printf("%4d  Value: %s\n", i, values[i]);
	}
//	char	*ox[MAXBIT], *c02[MAXBIT];
	char	ox[MAXNUM][MAXBIT], c02[MAXNUM][MAXBIT];
	int ox_c, c02_c;
	max_value(values, val_num, 0,
			ox, &ox_c, c02, &c02_c);
	
	for (i = 0; i < ox_c; i++)
	{
		printf("%4d  OX  Value: %s\n", i, ox[i]);
	} 
	for (i = 0; i < c02_c; i++)
	{
		printf("%4d  CO2  Value: %s\n", i, c02[i]);
	} 
	/*
	 * Get oxygen values ...
	 */
	for (digit = 1; ox_c > 1 && digit < num_bits; digit++)
	    max_value(ox, ox_c, digit,
			ox, &ox_c, c02, &c02_c);
    printf("Oxygen: %s\n", ox[0]);
    int ox_level = bvalue(ox[0]);
	/*
	 * Get c02 values ...
	 */
	max_value(values, val_num, 0,
			ox, &ox_c, c02, &c02_c);
	for (digit = 1; c02_c > 1 && digit < num_bits; digit++)
	    max_value(c02, c02_c, digit,
			ox, &ox_c, c02, &c02_c);
    printf("CO2: %s\n", c02[0]);
    int co2_level = bvalue(c02[0]);
	
    printf("Oxygen: %d\n", ox_level);
    printf("C02: %d\n", co2_level);
    printf("Product: %d\n", ox_level * co2_level); 
    return 0;
}
