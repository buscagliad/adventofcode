#include <stdio.h>
#include <math.h>
#include <stdlib.h>

class probe {
	public:
		probe(int upper_left_x, int upper_left_y,
			  int lower_right_x, int lower_right_y);
		bool	launch(int x_vel, int y_vel);
		bool	get_highpoint(int &x, int &y);
		void	set_trace(bool t = false) {trace = t; };
		int		search();
	private:
		bool	in_sector() { return ( (cur_x >= ulx) && (cur_x <= lrx) &&
									   (cur_y <= uly) && (cur_y >= lry) ); };
		bool	beyond_sector() { return ( (cur_x > lrx) || (cur_y < lry) ); };
		void 	step();
		int	ulx;  // boundary points
		int uly;
		int lrx;
		int lry;
		int	cur_x;  // current x position
		int cur_y;  // currect y position
		int cur_xv; // current x velocity
		int cur_yv;	// current y velocity
		bool success_launch;
		int high_x;
		int high_y;
		int step_count;
		bool trace;
};

probe::probe(int ux, int uy, int lx, int ly) {
	ulx = ux;  // boundary points
	uly = uy;
	lrx = lx;
	lry = ly;
	trace = false;
}

int	probe::search()
{
	int	count = 0;
	/*
	 * verify all one-shot solutions
	 */
	for (int xv = ulx; xv <= lrx; xv++)
	    for (int yv = uly; yv >= lry; yv--)
			if (launch(xv, yv))
			{
				count++;
				printf("%d   (%d,%d)\n", count, xv, yv);
			}
	int  yv_low = uly + 1;
	int yv_high = abs(lry) + 1;
	
	int xv_low = sqrt(2 * ulx) - 1;
	int xv_high = ulx - 1;
	printf("Range:  %d,%d  to %d,%d\n", xv_low, yv_low, xv_high, yv_high);
	for (int xv = xv_low; xv <= xv_high; xv++)
	    for (int yv = yv_low; yv <= yv_high; yv++)
			if (launch(xv, yv))
			{
				count++;
				printf("%d   (%d,%d)\n", count, xv, yv);
			}
	
	return count;
}

void    probe::step()
{
	step_count++;
	cur_x += cur_xv;
	cur_y += cur_yv;
	if (cur_xv < 0) cur_xv++;
	if (cur_xv > 0) cur_xv--;
	cur_yv--;
	if (cur_yv == 0)
	{
		high_x = cur_x;
		high_y = cur_y;
	}
	if (trace)
		printf("Step: %3d    x:%4d  y:%4d    dx:%4d  dy:%4d\n",
			step_count, cur_x, cur_y, cur_xv, cur_yv);
}

bool	probe::launch(int x_vel, int y_vel)
{
	cur_x = cur_y = 0;
	cur_xv = x_vel;
	cur_yv = y_vel;
	success_launch = false;
	step_count = 0;
	if (trace)
	{
		printf("Upper Left:  (%d, %d)    Lower Right: (%d, %d)\n",
			ulx, uly, lrx, lry);
		printf("Step: %3d    x:%4d  y:%4d    dx:%4d  dy:%4d\n",
			step_count, cur_x, cur_y, cur_xv, cur_yv);
	}
	while (!in_sector() && !beyond_sector())
	{
		step();
	}
	if (in_sector())
	{
		printf("Target hit:  x: %d  y: %d   after %d steps\n", cur_x, cur_y, step_count);
		printf("High point at x: %d  y: %d\n", high_x, high_y);
		success_launch = true;
		return true;
	}
	else
	{
		//printf("Failed after %d steps\n", step_count);
		//printf("Current position:  x: %d  y: %d\n", cur_x, cur_y);
	}
	return false;
}


int main(int argc, char **argv)
{
	probe p(20, -5, 30, -10);
	p.launch(7,2);
	p.launch(6,3);
	p.launch(9,0);
	p.launch(17,-4);
	//p.set_trace(true);
	p.launch(6,9);
	p.search();
	
	//target area: x=206..250, y=-105..-57
	probe f(206,-57, 250, -105);
	/*f.set_trace(true);*/
	f.launch(20,104);
	f.launch(20,105);
	f.launch(21,104);
	f.launch(21,105);
	f.search(); 
	return 1;
}
