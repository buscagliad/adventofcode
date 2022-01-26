#ifndef __POINT_HH__
#define __POINT_HH__

#include <string>
#include <stdlib.h>

using namespace std;

class point {
	public:
		point() { clear(); } ;
		point(int _x, int _y, int _z) { x = _x; y = _y, z = _z; };
		int dist(point p) {  int d = abs(x - p.x) + abs(y - p.y) + abs(z - p.z); return d;};
		int x, y, z;
		void clear() { x = y = z = 0; };
		bool is_set() { if (x == 0 && y == 0 && z == 0) return false; return true;} ;
		void out(const string &s) const  {printf("%s: %d,%d,%d\n", s.c_str(), x, y, z); };
		void out(const char *s) const {printf("%s: %d,%d,%d\n", s, x, y, z); };
		void add(point p) { x += p.x; y += p.y; z += p.z; };
		int	&operator[] (int n) { if (n == 0) return x;
								  if (n == 1) return y;
								  return z;}; 
		point& operator+=( point rhs)
		{
			x += rhs.x;
			y += rhs.y;
			z += rhs.z;
			return *this;
		}
 
		// friends defined inside class body are inline and are hidden from non-ADL lookup
		friend point operator+(point lhs,        // passing lhs by value helps optimize chained a+b+c
					  const point& rhs)  // otherwise, both parameters may be const references
		{
			lhs += rhs; // reuse compound assignment
			return lhs; // return the result by value (uses move constructor)
		}
		point& operator-=( point &rhs)
		{
			x -= rhs.x;
			y -= rhs.y;
			z -= rhs.z;
			return *this;
		}
 
		// friends defined inside class body are inline and are hidden from non-ADL lookup
		friend point operator-(point lhs,        // passing lhs by value helps optimize chained a+b+c
					 point rhs) // otherwise, both parameters may be const references
		{
			//lhs.out("LHS");
			//rhs.out("RHS");
			lhs -= rhs; // reuse compound assignment
			//lhs.out("LHS - RHS");
			return lhs; // return the result by value (uses move constructor)
		}
};

inline bool operator==(const point& lhs, const point& rhs){
	 if ( (lhs.x == rhs.x) && (lhs.y == rhs.y) && (lhs.z == rhs.z) ) return true;
	 return false;
}

inline
int sign(int s)
{
	if (s < 0) return -1;
	if (s > 0) return 1;
	return 0;
}

inline
point	rotate(point t, int r1, int r2, int r3) 
{
	point k;
	k[0] = sign(r1) * t[abs(r1) - 1];
	k[1] = sign(r2) * t[abs(r2) - 1];
	k[3] = sign(r3) * t[abs(r3) - 1];
	return k;
}

inline
point	rotate(point t, point rv) 
{
	return rotate(t, rv.x, rv.y, rv.z);
}


#endif
