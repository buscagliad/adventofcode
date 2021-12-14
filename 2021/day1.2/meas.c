#include <stdio.h>

int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "r");
    int   first;
    int   second;
    int   third;
    int   current;
    int   last;
    int   inc_count = 0;
    int   dec_count = 0;
    int   eq_count = 0;

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
    printf("Increases: %d\n", inc_count);
    printf("Decreases: %d\n", dec_count);
    printf("Equals: %d\n", eq_count);
    return 0;
}
