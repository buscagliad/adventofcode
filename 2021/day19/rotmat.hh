#ifndef __ROTMAT_HH__
#define __ROTMAT_HH__

#include <stdint.h>
#include <vector>
#include <stdio.h>
#include "point.hh"

using namespace std;

class rotmat {
	public:
		rotmat();
		void	clear();
		int 	det();
		point	rot(point &x);
		point	rotTrans(point &x);
		void	set(int i, int j, int v) { m[i][j] = v; };
		void	out(bool transpose = false);
		rotmat	trans() {
			rotmat r;
			for (int i = 0; i < 3; i++)
			   for (int j = 0; j < 3; j++)
			       r.m[i][j] = m[j][i];
			r.m_valid = m_valid;
			return r;
		}
			
		rotmat  operator*( rotmat rhs)
		{
			rotmat g;
			for (int i = 0; i < 3; i++)
				for (int j = 0; j < 3; j++)
					for (int k = 0; k < 3; k++)
						g.m[i][j] += m[i][k] * rhs.m[k][j];
			return g;
		}
		point  operator*(point rhs)
		{
			point g;
			//rhs.out("RHS");
			for (int i = 0; i < 3; i++)
				for (int j = 0; j < 3; j++)
						g[i] += m[i][j] * rhs[j];
			//g.out("OP *");
			return g;
		}
 		
	private:
		int		m[3][3];
		bool    m_valid;
};

inline
point	rotmat::rot(point &p)
{
	point rp;
	for (int i = 0; i < 3; i++)
		for (int j = 0; j < 3; j++)
		    rp[i] += m[i][j] * p[j];
	return rp;
}

inline
point	rotmat::rotTrans(point &p)
{
	point rp;
	for (int i = 0; i < 3; i++)
		for (int j = 0; j < 3; j++)
		    rp[i] += m[j][i] * p[j];
	return rp;
}

inline
void	rotmat::clear()
{
	for (int i = 0; i < 3; i++)
	    for (int j = 0; j < 3; j++)
			m[i][j] = 0;
	m_valid = false;
}

inline
rotmat::rotmat()
{
	clear();
}

inline
void	rotmat::out(bool transpose)
{
	for (int i = 0; i < 3; i++)
	{
		printf(" | ");
	    for (int j = 0; j < 3; j++)
	    {
			if (transpose) printf("%3d ", m[j][i]);
			else           printf("%3d ", m[i][j]);
		}
		printf(" |\n");
	}
	printf("\n");
}

inline
int	rotmat::det()
{
	int	a = m[0][0], b = m[1][0], c = m[2][0];
	int	d = m[0][1], e = m[1][1], f = m[2][1];
	int	g = m[0][2], h = m[1][2], i = m[2][2];
	
	int rv = 
	a * (e * i - f * h) -
	b * (d * i - f * g) +
	c * (d * h - e * g);
	return rv;
}




typedef struct {
	rotmat			rm;
	point			translate;
	uint32_t		from;
	uint32_t		to;
} rmobj_t;

class rMatrices {
	public:
		void	add (rotmat &rm, point &offset, uint32_t f, uint32_t t);
		bool	get (rmobj_t &r, uint32_t f, uint32_t t);
		point	rot(point p, uint32_t f, uint32_t t);
		point	adjust(point p, uint32_t f, uint32_t t);
		void	out(uint32_t i, uint32_t j);
		void	out();
	private:
		vector<rmobj_t>	m;
};

bool	rMatrices::get(rmobj_t &rm, uint32_t f, uint32_t t)
{

	for (uint32_t i = 0; i < m.size(); i++)
	{
		//printf("GET(loop)   from: %d  to: %d  det: %d\n", m[i].from, m[i].to, m[i].rm.det());
		if ( (m[i].from == f) && (m[i].to == t) )
		{
			rm = m[i];
			//printf("GET    from: %d  to: %d  det: %d\n", f, t, rm.det());
			return true;
		}
	}
	return false;
}

void	rMatrices::out(uint32_t f, uint32_t t)
{
	for (uint32_t i = 0; i < m.size(); i++)
	{
		if ( (m[i].from == f) && (m[i].to == t) )
		{
			printf("From %d  To %d\n", f, t);
			m[i].rm.out(false);
			return;
		}
		if ( (m[i].from == t) && (m[i].to == f) )
			printf("From %d  To %d - TRANSPOSE\n", f, t);
			m[i].rm.out(true);
			return;
	}
	printf("ERROR from = %d  to = %d]\n", f, t);
	return;
}

void	rMatrices::out()
{
	for (uint32_t i = 0; i < m.size(); i++)
	{
		printf("From %d to %d   det; %d\n", m[i].from, m[i].to, m[i].rm.det());
		m[i].translate.out("Offset vector");
		m[i].rm.out(false);
	}
}


void	rMatrices::add(rotmat &rm, point &off, uint32_t f, uint32_t t)
{
	rmobj_t	r;
	r.rm = rm;
	r.from = f;
	r.to = t;
	r.translate = off;
	printf("From: %d  To: %d   Det: %d\n", f, t, r.rm.det());
	m.push_back(r);
}

point	rMatrices::rot(point p, uint32_t f, uint32_t t)
{
	for (uint32_t i = 0; i < m.size(); i++)
	{
		if ( (m[i].from == f) && (m[i].to == t) )
			return m[i].rm.rot(p) + m[i].translate;
		if ( (m[i].from == t) && (m[i].to == f) )
			return m[i].rm.rotTrans(p) + m[i].translate;
	}
	printf("ERROR from = %d  to = %d]\n", f, t);
	return point(0,0,0);
}



#endif
