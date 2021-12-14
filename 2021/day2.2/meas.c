#include <stdio.h>

#define DEBUG 0

int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "r");
    int   depth = 0;
    int   horizontal = 0;
    int   aim = 0;
    char  cmd[100];
    int   value;

    fscanf(f, "%s %d", cmd, &value);
    while (!feof(f))
    {
		if (strcmp(cmd, "forward") == 0)
		{
		    if (DEBUG) printf("Forward: %d\n", value);
		    horizontal += value;
		    depth += value * aim;
		}
		else if (strcmp(cmd, "down") == 0)
		{
		    if (DEBUG) printf("Down: %d\n", value);
		    aim += value;
		}
		else if (strcmp(cmd, "up") == 0)
		{
		    if (DEBUG) printf("Up: %d\n", value);
		    aim -= value;
		}
 		else 
		{
		    printf("ERROR: %d\n", value);
		}
		fscanf(f, "%s %d", cmd, &value);
	}
    printf("Horizontal: %d\n", horizontal);
    printf("Depth: %d\n", depth);
    printf("Product: %d\n", horizontal * depth);
    return 0;
}
