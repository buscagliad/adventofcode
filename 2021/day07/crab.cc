#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>

#include "log.hh"

#define DEBUG 0

using namespace std;

class crabs {
	public:
		crabs(bool hard) : increasing_traverse(hard) {};
	    int	add(int p);
	    int count() { return c.size(); };
	    int set_to(int p);	// sets crabs to position p - returns total fuel
	    int min() { return min_v; };
	    int max() { return max_v; };
	private:
		bool increasing_traverse;	// when true, increase by 1 unit per step
		int	fuel_cost(int from, int to);
		vector<int> c;
		int	min_v;
		int max_v;
};

//
// either absolute difference from -> to   (OR)
// 1 + 2 + .. + abs(from-to)
int	crabs::fuel_cost(int from, int to)
{
	int	j = abs(from - to);
	if (!increasing_traverse) return j;
	return j * (j + 1) / 2;
}

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
	if (DEBUG) printf("Adding crab at pos: %d\n", p);
	return c.size();
}

int	crabs::set_to(int p)
{
	vector<int>::iterator it = c.begin();
	int	fuel = 0;
	for (; it != c.end(); ++it)
	{
		fuel += fuel_cost(*it, p);
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

int run_crabs(FILE *f, crabs &s)
{
	rewind(f);
	init(f, s);
	int	min_fuel = s.set_to(s.min());
	int min_pos = s.min();

	for (int i = s.min() + 1; i <= s.max(); i++)
	{
		int	fuel_used = s.set_to(i);
		if (DEBUG) printf("Position %d:  Fuel: %d\n", i, s.set_to(i));
		if (min_fuel > fuel_used)
		{
			min_fuel = fuel_used;
			min_pos = i;
		}
	}
	if (DEBUG) printf("Minimum position: %d    Fuel: %d\n", min_pos, min_fuel);
	return min_fuel;
}

int main(int argc, char **argv)
{
	FILE *f = fopen(argv[1], "r");
	crabs	s1(false);
	result(7, 1, run_crabs(f, s1), 345197);
	crabs	s2(true);
	result(7, 2, run_crabs(f, s2), 96361606);
	return 0;
}
