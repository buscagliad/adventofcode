#include <stdio.h>

int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "r");
    int   last;
    int   current;
    int   inc_count = 0;
    int   dec_count = 0;
    int   eq_count = 0;

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
    printf("Increases: %d\n", inc_count);
    printf("Decreases: %d\n", dec_count);
    printf("Equals: %d\n", eq_count);
    return 0;
}
