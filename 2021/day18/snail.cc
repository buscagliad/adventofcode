
#include <vector>
#include <string>
#include <iostream>
#include <string.h>

using namespace std;


class comp {
	public:
		comp(const char *s) { str = s; };
		void		add(const char *s);
		void		add(string as);
		void 		out();
		int64_t 	evaluate();
		int64_t		magnitude();
		bool		explode();
		bool		split();
	private:
		uint32_t	index = 0;
		string		str;
		int			left_count = 0;
		int			right_count = 0;
};

void	comp::add(string as)
{
	str.insert(0, 1, '[');
	str += ',';
	str += as;
	str += ']';
	cout << "++" << str << endl;
	bool did_explode, did_split;
	do
	{
		did_explode = false;
		did_split = false;
		while (explode()) {did_explode = true; };
		cout << "EXPLODE::"; out();
		if (split()) { did_split = true; };
		cout << "  SPLIT::"; out();
	} while ( did_explode || did_split );
}

void	comp::add(const char *s)
{
	string as = s;
	add(as);
}

int64_t	sum(long x, long y)
{
	return 3 * x + 2 * y;
}

size_t	fnest(string &s)
{
	size_t	left = 0, right = 0;
	for (size_t i = 0; i < s.size(); i++)
	{
		if (s[i] == '[') left++;
		if (s[i] == ']') right++;
		if (left - right > 4 ) return i;
	}
	return string::npos;
}
bool isvalid(char c)
{
	return (c != ',' && c != '[' && c != ']');
}

char charadd(char s, char a)
{
	int	ai = a - '0';
	int nx = ai + s;
	if (nx > 127) {
	    printf("ERROR - charadd: char: %c   to char: %c\n", a, s);
	    exit(2);
	}
	s += ai;
	if (s >= '[') s+= 3;
	return s;
}

string newpair(char x)
{
	string np = "[x,x]";

	if (x > ']') x -= 3;
	
	int		val = x - '0';
	char	left = val / 2 + '0';
	char    right = (val + 1) / 2 + '0';
	
	np[1] = left;
	np[3] = right;
	return np;
}

void	add_left(string &s, size_t index)
{
	char c = s[index];
	for (index--; index > 0; index--)
	{
		if (isvalid(s[index]))
		{
		    s[index] = charadd(s[index], c);
		    if (!isvalid(s[index])) {
		        printf("ERROR - add_left invalid sum char\n");
		        exit(1);
		    }
		    return;
		}
	}
}

void	add_right(string &s, size_t index)
{
	char c = s[index];
	for (index++; index < s.size(); index++)
	{
		if (isvalid(s[index]))
		{
		    s[index] = charadd(s[index], c);
		    if (!isvalid(s[index])) {
		        printf("ERROR - add_right invalid sum char\n");
		        exit(1);
		    }
		    return;
		}
	}
}

void	split_insert(string &s, size_t ix, string is)
{
	s.erase(ix, 1);
	s.insert(ix, is);
	cout << s << endl;
}

#define AFTER_NINE	('9' + 1)
#define LAST_CHAR   ('9' + 9)
static const string spls[]= {"[5,5]", "[5,6]","[6,6]","[6,7]","[7,7]","[7,8]","[8,8]","[8,9]","[9,9]"};
bool	comp::split()
{
	string s = str;
	bool rv = false;
	for (size_t index = 0; index < s.size() - 1; index++)
	{
		if ( (s[index] >= AFTER_NINE) && isvalid(s[index]) )
		{
			cout << "Found insert char: " << s[index] << " at index " << index;
			cout << "  inserting: " << newpair(s[index]) << endl;
		    split_insert(s, index, newpair(s[index]));
			str = s;
		    return true;
		}
	}
	return rv;
}

bool	comp::explode()
{
	string sc = str;
	size_t ex = fnest(sc);
	if (ex != string::npos)
	{
		cout << "Found nested data at " << ex << " " << sc.substr(ex, 5) << endl;
		add_left(sc, ex+1);
		add_right(sc, ex+3);
		sc.erase(ex+1, 4);
		sc[ex] = '0';
		str = sc;
		out();
		str = sc;
		return true;
	}
	return false;
}
	    

int64_t	reduce(string &s, size_t alp, size_t frp)
{
	string  ss = s.substr(alp + 1);
	long	x, y;
	size_t			idx = 1;
	x = stol(ss, &idx);
	y = stol(ss.substr(idx+1));

	int64_t	rval = sum(x, y);
	//cout << " alp: " <<  alp << "   frp: " << frp ;
	//cout << "   n = " << rval << endl;
	string ns;
	if (alp > 0)
	    ns = s.substr(0, alp);
	ns += to_string(rval);
	//cout << "A ns " << ns << endl;
	if (frp + 1 < s.size())
	{
		//cout << "frp " << frp << " s-size " << s.size() << " alp: " << alp << endl;
		ns += s.substr(frp + 1);
	}
	//cout << "B ns " << ns << endl;
	s = ns;
	return rval;
}

int64_t	subeval(string &s)
{
	size_t	frp;	// position of first right parantheis
	size_t	alp;	// position of associated left parenthesis
	frp = s.find_first_of("]");
	alp = frp;
	while (s[alp] != '[') alp--;
	//cout << "SUBEVAL: " << s << "  alp: " << alp << "  frp: " << frp << endl;
	int64_t rv = reduce(s, alp, frp);
	return rv;
}

int64_t	comp::magnitude()
{
	int64_t	v;
	string s = str;
	//cout << "MAGNITUDE: " << s << endl;
	while (s.find_first_of("]") != string::npos)
	{
	    v = subeval(s);
	    //cout << "STR:" << s << "  VAL: " << v << endl;
	}
	return v;
}

int64_t	comp::evaluate()
{
	int64_t	v;
	string s = str;
	//cout << "EVALUATE: " << s << endl;
	while (s.find_first_of("]") != string::npos)
	{
	    v = subeval(s);
	    //cout << "STR:" << s << "  VAL: " << v << endl;
	}
	return v;
}



void comp::out()
{
	cout << str << endl;
}

#define MAXBUF 10000
int64_t rmag(FILE *f)
{
	char	buf[MAXBUF];
	fgets(buf, MAXBUF, f);
	if (feof(f)) return 0;
	comp	m(buf);
	int64_t	v = m.magnitude();
	m.out();
	cout << "Mag is: " << v << endl;
	fgets(buf, MAXBUF, f);
	cout <<  "Truth: " << buf;

	return v;
}

int64_t fadd(FILE *f)
{
	char	buf[MAXBUF];
	fgets(buf, MAXBUF, f);
	buf[strlen(buf)-1] = 0;
	printf("<<%s\n", buf);
	if (feof(f)) return 0;
	comp m(buf);
	while (!feof(f))
	{
		fgets(buf, MAXBUF, f);
		if (feof(f)) break;
		printf("<<%s\n", buf);
		buf[strlen(buf)-1] = 0;
		m.add(buf);
		m.out();
	}
	return m.evaluate();
}

static string max1;
static string max2;
static int64_t max_val = 0;


int64_t	addtwo(const char *s1, const char *s2)
{
	comp	c(s1);
	c.add(s2);
	return c.magnitude();
}

int64_t maxtwo(const char *cA, const char *cB)
{
	int64_t	ab = addtwo(cA, cB);
	int64_t ba = addtwo(cB, cA);
	if (ab > max_val)
	{
		max_val = ab;
		max1 = cA;
		max2 = cB;
	}
	if (ba > max_val)
	{
		max_val = ba;
		max1 = cB;
		max2 = cA;
	}
	return max_val;
}


int findmax(FILE *f, int n)
{
	rewind(f);
	int     num_lines = 0;
	char	b1[MAXBUF];
	char	b2[MAXBUF];
	//
	// get first snail number
	for (int i = 0; i < n; i++)
	{
		fgets(b1, MAXBUF, f);
		b1[strlen(b1)-1] = 0;
		num_lines++;
	}

	if (feof(f)) return 0;
	while (!feof(f))
	{
		fgets(b2, MAXBUF, f);
		if (feof(f)) break;
		b2[strlen(b2)-1] = 0;
		maxtwo(b1, b2);
		num_lines++;
	}
	return num_lines;
}		

int main(int argc, char **argv)
{
	FILE *h = fopen("data.txt", "r");
	cout << "Evaluate: " << fadd(h) << endl;
	int maxn = findmax(h, 1);
	for (int i = 2; i < maxn; i++) findmax(h, i);
	cout << "MAX  FIRST: " << max1 << endl;
	cout << "MAX SECOND: " << max2 << endl;
	cout << "MAX  VALUE: " << max_val << endl; 
	fclose(h);
	return 1;
	/*
	FILE *g = fopen("ex2.txt", "r");
	cout << "Evaluate: " << fadd(g) << endl;
	* 
	FILE *f = fopen("ex.txt", "r");
	while (!feof(f))
	{
		rmag(f);
	}*/
	return 1;
}
