#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>

using namespace std;

class crabs {
	public:
	    int	add(int p);
	    int count() { return c.size(); };
	    int set_to(int p);	// sets crabs to position p - returns total fuel
	    int min() { return min_v; };
	    int max() { return max_v; };
	private:
		vector<int> c;
		int	min_v;
		int max_v;
};

int	crabs::add(int p)
{
	if (c.size() == 0)
	{
		min_v = p;
		max_v = p;
	}
	else
	{
		if (min_v > p) min_v = p;
		if (max_v < p) max_v = p;
	}
	c.push_back(p);
	printf("Adding crab at pos: %d\n", p);
	return c.size();
}

int	crabs::set_to(int p)
{
	vector<int>::iterator it = c.begin();
	int	fuel = 0;
	for (; it != c.end(); ++it)
	{
		fuel += abs(*it - p);
	}
	return fuel;
}

int init(FILE *f, crabs &s)
{
	int v = 0;
	char c = fgetc(f);
	while (c > 0)
	{
		if (isalnum(c))
		{
			int d = c - '0';
			v = 10 * v + d;
		}
	    if (!isalnum(c))
	    {
			s.add(v);
			v = 0;
		}
		c = fgetc(f);
	}
	return s.count();
}


int main(int argc, char **argv)
{
	FILE *f = fopen(argv[1], "r");
	crabs	s;
	init(f, s);
	int	min_fuel = s.set_to(s.min());
	int min_pos = s.min();

	for (int i = s.min() + 1; i <= s.max(); i++)
	{
		int	fuel_used = s.set_to(i);
		printf("Position %d:  Fuel: %d\n", i, s.set_to(i));
		if (min_fuel > fuel_used)
		{
			min_fuel = fuel_used;
			min_pos = i;
		}
	}
	printf("Minimum position: %d    Fuel: %d\n", min_pos, min_fuel);
	return 0;
}
