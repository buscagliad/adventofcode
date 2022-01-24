#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>
#include <cstring>
#include <string>
#include <iostream>

#define DEBUG 0

static int num_enters = 0;
static int num_returns = 0;


using namespace std;

class cave {
	public:
		cave(const char *nm);
		cave*   dup();
		void	connect(cave *c);
		string  name(){ return _name;};
		int     size() {return connections.size();};
		cave	*next();
		cave	*first() {if (_name == "end") return NULL; it = 0; return next();};
		void    reset() {it = 0;};
		bool    is_small() { return small; };
		void	info();
	private:
		string		    _name;
		vector<cave *>  connections;
		unsigned long	it;
		bool		    small;	// if true, can only be entered/exited once
};

cave*  cave::dup()
{
	cave *c = new cave(_name.c_str());
	c->small = small;
	c->connections = connections;
	c->it = 0;
	c->small = small;
	return c;
}

void	cave::connect(cave *c)
{
	if ( (_name != "end") && (c->name() != "start") ) connections.push_back(c);
	if (DEBUG) printf("%s connected to %s [%lu]\n", _name.c_str(), c->name().c_str(), 
			connections.size());
}

void cave::info()
{
	if (DEBUG) printf("CAVE: %s  #connects: %lu   it = %lu   small=%s\n",
		_name.c_str(), connections.size(), it, (small?"true":"false"));
}

cave::cave(const char *nm)
{
	_name = nm;
	it = 0;
	if (islower(*nm)) small = true; else small = false;
}

cave* cave::next()
{
	if (it >= connections.size()) 
	{
		//if (DEBUG) printf("NEXT: %s  -->  NULL[%d]\n", _name.c_str(), it);
		return NULL;
	}
	cave* n = connections[it];
	//if (DEBUG) printf("NEXT: %s[%d]  -->  \n", _name.c_str(), it);
	it++;
	return n;
}

class pathList {
	public:
		pathList() { last_pop = NULL; };
		cave*	push(cave *c);
		cave*	pop() { path.pop_back();
						cave* rc = path[path.size() - 1];
						if (DEBUG) printf("Popping returning %s\n", rc->name().c_str());
						return rc; };	// remove and reset
		void	out(cave *c = NULL);
		int		size() { return path.size(); };
		cave	*end() { int n = path.size(); 
						if (n <= 0 ) return NULL;
						cave *r = path[n - 1]; 
						  //if (DEBUG) printf("END: r = %8.8x   size = %d\n", r, n);
						  return r;
						  };
		bool allowable(cave *c);
		int	exists(const char *nm);
		int	exists(cave *c);
	private:
		vector<cave *>	path;
		cave*			last_pop;
};

// all large caves are allowable
// small caves are allowable to have two if they are the only one in the path
//
bool	pathList::allowable(cave *c)
{
	if (!c->is_small()) return true;
	if (c->name() == "end") return true;
	int te = this->exists(c);
	if (te > 1) return false;
	if (te == 0) return true;
	for (unsigned long int i = 0; i < path.size(); i++)
	{
		if ( !(path[i]->is_small()) ) continue;
		int   ex = this->exists(path[i]);
		//printf("Path has %d of %s\n", ex, path[i]->name().c_str());
		if ( ( this->exists(path[i]) > 1 ) )return false; // already a small cave is twice
	}
	return true;
}

int	pathList::exists(const char *nm)
{
	int  count = 0;
	for (unsigned long int i = 0; i < path.size(); i++)
		if (path[i]->name() == nm) count++;
	return count;
}


int	pathList::exists(cave *c)
{
	return exists(c->name().c_str());
}

cave *pathList::push(cave *c) 
{
	cave *nc = c->dup(); 
	nc->reset(); 
	path.push_back(nc); 
	if (DEBUG) printf("Pushing %s - connections = %d\n", nc->name().c_str(), nc->size()); 
	return nc; 
}


cave* path_head = NULL;


//
// caveNetwork holds the UNIQUE list of caves
// each cave consists of a cave name and the list of caves it connects to
//
class caveNetwork {
	public:
		//caveNetwork(cave *c);
		int	 connect(const char *a, const char *b);
		cave *exists(const char *a);
		void display();
		int	 paths(pathList &path, cave *node, int &count);
		bool small_used_twice(pathList &path, cave *node);
		int  size() {return cavelist.size();};
		void reset();
		void clear() {cavelist.clear();};
	private:
		cave*  create(const char *a);
		vector<cave *> cavelist;
		int it;
};

caveNetwork cn;		// global cave network


void	caveNetwork::reset()
{
	it = 0;
	for (int i; i < cavelist[it]->size(); i++)
	    cavelist[i]->reset();
}	    

void	caveNetwork::display()
{
	// for each cave node in the cavelist - 
	for (unsigned long int i = 0; i < cavelist.size(); i++)
	{
		// output each connection this node has
		cave *ci = cavelist[i];
		ci -> reset();
		for (cave *ci = cavelist[i]->first(); ci != NULL; ci = cavelist[i]->next())
		{
//			cout << cavelist[i]-> name() <<  " --> "  << ci -> name() << endl;
			cout << cavelist[i]-> name() <<  " --> "  << ci -> name() << endl;
		}
	}
	if (DEBUG) printf("END OF DISPLAY\n");
}

cave	*caveNetwork::exists(const char *a)
{
	for (unsigned long int i = 0; i < cavelist.size(); i++)
	{
		if (cavelist[i]->name() == a)
			return cavelist[i];
	}
	return 0;
}

cave *caveNetwork::create(const char *a)
{
	cave   *new_cave = new cave(a);
	//if (DEBUG) printf("New cave: %s\n", new_cave->name().c_str());
	if (new_cave->name() == "start")
	{
		path_head = new_cave;
	    cavelist.insert(cavelist.begin(), new_cave);
	}
	else
		cavelist.push_back(new_cave);
	return new_cave;
}

int caveNetwork::connect(const char *a, const char *b)
{
	cave	*ac = exists(a);
	cave    *bc = exists(b);
	//if (DEBUG) printf("Connecting %s(%c) <--> %s(%c)\n", a, (ac?'*':'-'), b, (bc?'*':'-'));
	if (!ac) ac = create(a);
	if (!bc) bc = create(b);
	ac->connect(bc);
	bc->connect(ac);
	return cavelist.size();
}


void pathList::out(cave *c)
{
	for (unsigned long int i = 0; i < path.size(); i++)
	{
		if (i != 0) if (DEBUG) printf(",");
		if (DEBUG) printf("%s", path[i]->name().c_str());
	}
	if (path.size()) if (DEBUG) printf(",");
	if (c) if (DEBUG) printf( "(%s)", c->name().c_str());
	if (DEBUG) printf("\n");
}

int	caveNetwork::paths(pathList &path, cave *node, int &path_count)
{
	if (DEBUG) printf("\n\n===========================\n");
	num_enters++;
	fflush(stdout);
	cave *ln = path.end();
	if (path_count > 0 && !node)
	{
		if (ln  &&  (ln->name() == "start"))
		{
			num_returns++;
			return path_count;
		}
		if (DEBUG) printf("WTF!!!!!%s!!!!!!!!\n", ln->name().c_str());
	}
		
	if (path.size() == 0)	// put 'start' at the beginning
	{
		cave *st = cn.exists("start");
		if (!st)
		{
			if (DEBUG) printf("ERROR - no start cave found\n");
			exit(1);
		}
		path_count = 0;
		printf("Setting path_count = %d\n", path_count);
		st = path.push(st);
		paths(path, st->next(), path_count);
		num_returns++;
		return path_count;
	}
	else if (ln->name() == "end")
	{
		path_count++;
		if (DEBUG) printf("SUCCESSFULL path - "); 
		path.out();
		node = path.pop();
		paths(path, node->next(), path_count);
		num_returns++;
		return path_count;
	}
	
		
	if (!node) 
	{
		cave *nn = path.pop();
		if (DEBUG) printf("B::NULL ptr from %s\n", nn->name().c_str());
		if (DEBUG) printf("B:FAILED path - "); 
		path.out();
		paths(path, nn->next(), path_count);
		num_returns++;
		return path_count;

	}
	if (DEBUG) printf("[%3d] TRY:: ", path_count); path.out(node);	
	if (node->is_small())
	{
		if (DEBUG) printf("S::%s\n", node->name().c_str()); 
		if ( ! path.allowable(node))
		{
			if (DEBUG) printf("Small node: %s exists\n", node->name().c_str());
			if (DEBUG) printf("Next from obj: %s\n", ln->name().c_str());
			paths(path, ln->next(), path_count);
			num_returns++;
			return path_count;
		}
		else
		{
			cave *n = path.push(node);
			paths(path, n->next(), path_count);
			num_returns++;
			return path_count;
		}
	} 
	else
	{
		if (DEBUG) printf("C:");
		node = path.push(node);
		paths(path, node->next(), path_count);
		num_returns++;
		return path_count;
	}
	num_returns++;
	return path_count;
}
	
void	parseline(caveNetwork &cn, char *c)
{
	const char *from = c;
	const char *to = NULL;
	*strchr(c, '\n') = 0;
	char *dash = strchr(c, '-');
	*dash = 0;
	to = dash + 1;
	cn.connect(from, to);
	if (DEBUG) printf(">>>>>>>>> %s --- %s <<<<<<<<<<<<\n", from, to);
}


#define MAXLINE 20000
void cave_paths(const char *v, int tPathCount)
{
	FILE *f = fopen(v, "r");
	char c[MAXLINE];
	fgets(c, MAXLINE, f);
	cn.clear();
	while (!feof(f))
	{
		parseline(cn, c);
		fgets(c, MAXLINE, f);
	}
	printf("Input file: %s\n", v);
	//cn.reset();
	cn.display();
	//exit(1);
	cn.reset();
	pathList cpath;
	int pathCount = 0;
	cn.paths(cpath, path_head, pathCount);
	printf("Path count is: %d\n", pathCount);
	if (tPathCount > 0)
	{
		if (tPathCount == pathCount)
			printf("Successfully counted the paths!!\n");
		else
			printf("Path Count = %d, not in agreement with true count: %d\n",
				pathCount, tPathCount);
	}
	fclose(f);
}

int main(int argc, char **argv)
{
	num_enters = 0; num_returns = 0;
	cave_paths("ex1.txt", 36);
	printf("Num Enters: %d   Num Returns: %d\n", num_enters, num_returns);
	num_enters = 0; num_returns = 0;
	cave_paths("ex3.txt", 3509);
	printf("Num Enters: %d   Num Returns: %d\n", num_enters, num_returns);
	num_enters = 0; num_returns = 0;
	cave_paths("ex2.txt", 224);
	printf("Num Enters: %d   Num Returns: %d\n", num_enters, num_returns);
	num_enters = 0; num_returns = 0;
	cave_paths("data.txt", 2975);
	printf("Num Enters: %d   Num Returns: %d\n", num_enters, num_returns);
	num_enters = 0; num_returns = 0;
	return 0;
}
