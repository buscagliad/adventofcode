#include <stdio.h>
#include "log.hh"

void part1(FILE *f, int answer)
{
	int   last;
    int   current;
    int   inc_count = 0;
    int   dec_count = 0;
    int   eq_count = 0;
	rewind(f);
    fscanf(f, "%d", &last);
    fscanf(f, "%d", &current);
    while (!feof(f))
    {
	    if (current > last) inc_count++;
	    else if (current < last) dec_count++;
	    else eq_count++;
	    last = current;
        fscanf(f, "%d", &current);
    }
    result(1, 1, inc_count, answer);
}

void part2(FILE *f, int answer)
{
    int   first;
    int   second;
    int   third;
    int   current;
    int   last;
    int   inc_count = 0;
    int   dec_count = 0;
    int   eq_count = 0;
	rewind(f);
    fscanf(f, "%d", &first);
    fscanf(f, "%d", &second);
    fscanf(f, "%d", &third);
    last = first + second + third;
    first = second;
    second = third;
    fscanf(f, "%d", &third);    
    while (!feof(f))
    {
		current = first + second + third;
	    if (current > last) inc_count++;
	    else if (current < last) dec_count++;
	    else eq_count++;
	    last = current;
		first = second;
		second = third;
		fscanf(f, "%d", &third);    
		current = first + second + third;
    }
    result(1, 2, inc_count, answer);
}


int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "r");
	part1(f, 1374);
	part2(f, 1418);
    return 0;
}
