#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>

using namespace std;

class	fish {
	public:
		fish(int day = 8){_timer = day;};
		bool	next(); // decreases its timer, returns true
					   // if a new fish should be spawned
		int		timer(){return _timer;};
	private:
		int _timer;
};

bool	fish::next()
{
	_timer --; 
	if (_timer < 0)
	{
		_timer = 6;
		return true;
	}
	return false;
}

class  school {
	public:
		school();
		void				add(int t);
		long long int		next();
		void				out();
		long long int		population();
	private:
		long long int		day[9];
};

school::school()
{
	for (int i = 0; i < 9; i++) day[i] = 0;
}

long long int school::population()
{
	long long int sum = 0;
	for (int i = 0; i < 9; i++) sum += day[i];
	return sum;
}

void	school::add(int timer)
{
	day[timer]++;
}

long long int	school::next()
{
	long long int	hold = day[0];
	for (int i = 0; i < 8; i++) day[i] = day[i+1];
	day[6] += hold;
	day[8] = hold;
	return population();
}

void	school::out()
{
	for (int i = 0; i < 9; i++)
		printf("Day %d fish: %lld\n", i, day[i]);
	printf("Total of %lld fish\n", population());
	printf("\n");
}

void init(FILE *f, school &s)
{
	char c = fgetc(f);
	while (c > 0)
	{
		if (isalnum(c))
	        s.add(c - '0');
	    c = fgetc(f);
	}
}


int main(int argc, char **argv)
{
	int		num_days = atoi(argv[2]);
	FILE *f = fopen(argv[1], "r");
	school	s;
	init(f, s);
	printf("Initial state: ");
	s.out();
	for (int i = 1; i <= num_days; i++)
	{
		s.next();
		printf("After %2d days: ", i);
		s.out();
	}
	printf("Total number of fish: %lld\n", s.population());
	return 0;
}
