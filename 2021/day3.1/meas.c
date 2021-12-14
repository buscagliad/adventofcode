#include <stdio.h>
#include <string.h>

#define DEBUG 0
#define MAXBIT 50

int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "r");
    char  cmd[100];
    int   onebitcnt[MAXBIT];
    int   zerobitcnt[MAXBIT];
    int   errorbitcnt[MAXBIT];
    int   i;
    int	  gamma_rate = 0;
    int   eps_rate = 0;
    int	  pwr_two = 1;
    int   err_rate = 0;
    
    for (i = 0; i < MAXBIT; i++)
    {
		onebitcnt[i] = 0;
		zerobitcnt[i] = 0;
		errorbitcnt[i] = 0;
	}

    fscanf(f, "%s\n", cmd);
    while (!feof(f))
    {
		for (i = 0; i < strlen(cmd); i++)
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
    printf("Gamma: %d\n", gamma_rate);
    printf("Eps: %d\n", eps_rate);
    printf("ERR: %d\n", err_rate);
    printf("Product: %d\n", gamma_rate * eps_rate);
    return 0;
}
