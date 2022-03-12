#include <stdio.h>
#include <string.h>
#include "log.hh"

#define DEBUG 0

void part1(FILE *f, int answer)
{
    int   depth = 0;
    int   horizontal = 0;
    char  cmd[100];
    int   value;

    fscanf(f, "%s %d", cmd, &value);
    while (!feof(f))
    {
		if (strcmp(cmd, "forward") == 0)
		{
		    if (DEBUG) printf("Forward: %d\n", value);
		    horizontal += value;
		}
		else if (strcmp(cmd, "down") == 0)
		{
		    if (DEBUG) printf("Down: %d\n", value);
		    depth += value;
		}
		else if (strcmp(cmd, "up") == 0)
		{
		    if (DEBUG) printf("Up: %d\n", value);
		    depth -= value;
		}
 		else 
		{
		    printf("ERROR: %d\n", value);
		}
		fscanf(f, "%s %d", cmd, &value);
	}
    if (DEBUG) printf("Horizontal: %d\n", horizontal);
    if (DEBUG) printf("Depth: %d\n", depth);
    if (DEBUG) printf("Product: %d\n", horizontal * depth);
    result(2, 1, horizontal * depth, answer);
}

void part2(FILE *f, int64_t answer)
{
	int64_t   depth = 0;
    int64_t   horizontal = 0;
    int64_t   aim = 0;
    char  cmd[100];
    int64_t   value;
	rewind(f);
    fscanf(f, "%s %ld", cmd, &value);
    while (!feof(f))
    {
		if (strcmp(cmd, "forward") == 0)
		{
		    if (DEBUG) printf("Forward: %ld\n", value);
		    horizontal += value;
		    depth += value * aim;
		}
		else if (strcmp(cmd, "down") == 0)
		{
		    if (DEBUG) printf("Down: %ld\n", value);
		    aim += value;
		}
		else if (strcmp(cmd, "up") == 0)
		{
		    if (DEBUG) printf("Up: %ld\n", value);
		    aim -= value;
		}
 		else 
		{
		    printf("ERROR: %ld\n", value);
		}
		fscanf(f, "%s %ld", cmd, &value);
	}
    if (DEBUG) printf("Horizontal: %ld\n", horizontal);
    if (DEBUG) printf("Depth: %ld\n", depth);
    result64(2, 2, horizontal * depth, answer);
}

int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "r");
	part1(f, 2102357);
 	part2(f, 2101031224);
   return 0;
}
