
#include <vector>
#include <string>
#include <iostream>
#include <string.h>

using namespace std;

/*
#define NONE     -1
#define ADD 	 0
#define PRODUCT  1
#define MINIMUM  2
#define MAXIMUM  3
#define LITERAL  4
#define GREATER  5
#define LESS	 6
#define EQUAL    7
#define END		 8
*/
typedef enum 
	{	NONE = -1,
		ADD = 0,
		PRODUCT   = 1,
		MINIMUM   = 2,
		MAXIMUM   = 3,
		LITERAL   = 4,
		GREATER   = 5,
		LESS	  = 6,
		EQUAL     = 7,
		END		  = 8 } op_type;

#define OPERATOR(n)	\
	((n == ADD) ? "add" :	\
	(n == PRODUCT) ? "product" :	\
	(n == MINIMUM) ? "minimum" :    \
	(n == MAXIMUM) ? "maximum" :	\
	(n == LITERAL) ? "literal" :   \
	(n == EQUAL) ? "equal" :	\
	(n == LESS)	? "less-than" : \
	(n == GREATER)	? "greater-than": \
	(n == END)	? "END": \
	"ERROR")

const char *operand(int n)
{
	return OPERATOR(n);
}

class opobj {
	public:
		opobj();
		opobj(int64_t _v, op_type _op) {v = _v; op = _op;} ;
		int64_t		v;
		op_type		op;
};

opobj::opobj() { v = 0; op = NONE; }

class comp {
	public:
		int			push(int64_t _v, op_type _op) { return push(opobj(_v,_op)); }
		int			push(opobj o);
		opobj		pop();
		bool		next(opobj &o) { if (at_end()) return false;
									 o = v[index++]; return true;}
		void 		out();
		int64_t 	evaluate();
		bool 		is_next(int _op) 
						{  if (_op  == NONE) return true;
						   opobj o = v[index];
						   bool rv = (o.op == _op);
						   return rv;
						 }
		int			insert(opobj o) { v[--index] = o; /*printf("Inserted %s/%ld - size: %lu\n",
										OPERATOR(o.op), o.v, v.size()); */
										return index; }
		bool        at_end() { return (index + 1  >= v.size()); }
	private:
		int64_t compute(op_type op, int64_t &v, bool first);
		vector<opobj> v;
		uint32_t	index = 0;
		string		str;
		int			left_count = 0;
		int			right_count = 0;
};

int64_t	sum(vector<long> &v)
{
	int64_t	s = 0;
	size_t		n;
	for (n = 0; n < v.size(); n++) s += v[n];
	return s;
}
int64_t	product(vector<long> &v)
{
	int64_t	s = 1;
	size_t		n;
	for (n = 0; n < v.size(); n++) s *= v[n];
	return s;
}
int64_t	max(vector<long> &v)
{
	int64_t	s = v[0];
	size_t		n;
	for (n = 1; n < v.size(); n++)
		if (s < v[n]) s = v[n];
	return s;
}
int64_t	min(vector<long> &v)
{
	int64_t	s = v[0];
	size_t		n;
	for (n = 1; n < v.size(); n++)
		if (s > v[n]) s = v[n];
	return s;
}
int64_t	gthan(vector<long> &v)
{
	return v[0] > v[1];
}
int64_t	lthan(vector<long> &v)
{
	return v[0] < v[1];
}
int64_t	equal(vector<long> &v)
{
	return v[0] == v[1];
}

int64_t	number(char op, vector<long> &v)
{
	switch(op)
	{
		case '+': return sum(v);
		case '*': return product(v);
		case 'M': return max(v);
		case 'm': return min(v);
		case '>': return gthan(v);
		case '<': return lthan(v);
		case '=': return equal(v);
	}
	return -1;
}

int64_t	reduce(string &s, size_t alp, size_t frp)
{
	string  ss = s.substr(alp + 2);
	vector<long>	v;
	size_t			idx = 1;
	while (true)
	{
		int64_t	n = stol(ss, &idx);
		v.push_back(n);
		if (ss[idx] == ',') idx++;
		else if (ss[idx] == ')') break;
		ss = ss.substr(idx);
	}
	int64_t	rval = number(s[alp], v);
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
	frp = s.find_first_of(")");
	alp = frp;
	while (s[alp] != '(') alp--;
	alp--;	// captures the operator
	//cout << "SUBEVAL: " << s << "  alp: " << alp << "  frp: " << frp << endl;
	int64_t rv = reduce(s, alp, frp);
	return rv;
}

int64_t	comp::evaluate()
{
	int64_t	v;
	string s = str;
	cout << "EVALUATE: " << s << endl;
	while (s.find_first_of(")") != string::npos)
	{
	    v = subeval(s);
	    cout << "STR:" << s << "  VAL: " << v << endl;
	}
	return v;
}

int		comp::push(opobj o) 
{ 
	v.push_back(o); 
	switch (o.op)
	{	case NONE:		str += "NONE"; break;
		case ADD:      	str += "+("; left_count++; break;
		case PRODUCT:	str += "*("; left_count++; break;
		case MINIMUM:	str += "m("; left_count++; break;
		case MAXIMUM:	str += "M("; left_count++; break;
		case LITERAL:	str += to_string(o.v) + ','; break;
		case GREATER:	str += ">("; left_count++; break;
		case LESS:		str += "<("; left_count++; break;
		case EQUAL:		str += "=("; left_count++; break;
		case END: 		right_count++;
						if (str.back() == ',') 
							*(str.rbegin()) = ')';
						else
							str += ")"; 
						if (left_count > right_count) // not done
						    str += ',';
						break;
						
	}
	//printf("Pushed %s/%ld - size: %lu\n", OPERATOR(o.op), o.v, v.size());
	return v.size(); 
}

opobj	comp::pop()
{
	opobj o = v[index];
	index++;
	return o;
}



void comp::out()
{
	printf("SIZE: %ld\n", v.size());
	for (uint32_t i = 0; i < v.size(); i++)
	{
		int64_t	val = v[i].v;
		int     op = v[i].op;
		if (op != LITERAL)
		    printf("%s\n", OPERATOR(op));
		else
	        printf("%ld\n", val);
	}
	cout << str << endl;
}
