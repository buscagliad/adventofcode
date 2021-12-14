#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <ctype.h>
#include <cstring>
#include <string>
#include <iostream>

using namespace std;

class cave {
	public:
		cave(const char *nm);
		void	connect(cave *c){ if ( (_name != "end") && (c->name() != "start") ) connections.push_back(c);};
		string  name(){ return _name;};
		cave	*next();
		cave	*first() {if (_name == "end") return NULL; it = connections.begin(); return *it;};
		void    reset() {it = connections.begin();};
		bool    is_small() { return small; };
	private:
		string		    _name;
		vector<cave *>  connections;
		vector<cave *>::iterator  it;
		bool		    small;	// if true, can only be entered/exited once
};

cave::cave(const char *nm)
{
	_name = nm;
	if (islower(*nm)) small = true; else small = false;
}

cave* cave::next()
{
	it++;
	if (it == connections.end()) return NULL;
	return *it;
}

int  path_count = 0;	// this is the counter for all paths from start to end
cave* path_head = NULL;

class caveNetwork {
	public:
		//caveNetwork(cave *c);
		int	 connect(const char *a, const char *b);
		cave *exists(const char *a);
		void display();
		int	 paths(vector<cave *> &path, cave *node, bool debug);
		void reset();
	private:
		cave*  create(const char *a);
		vector<cave *> cavelist;
		vector<cave *>::iterator it;
};

void	caveNetwork::reset()
{
	it = cavelist.begin();
	for (; it != cavelist.end(); it++)
	    (*it)->reset();
	it = cavelist.begin();
}	    
//caveNetwork::caveNetwork(cave *c)
//{
	// do nothing for now - may want to add start/end caves
//}

void	caveNetwork::display()
{
	reset();
	it = cavelist.begin();
	// for each cave node in the cavelist - 
	for (; it != cavelist.end(); it++)
	{
		// output each connection this node has
		for (cave *ci = (*it)->first(); ci != NULL; ci = (*it)->next())
		{
			cout << (*it)-> name() <<  " --> "  << ci -> name() << endl;
		}
	}
	printf("END OF DISPLAY\n");
}

cave	*caveNetwork::exists(const char *a)
{
	for (it = cavelist.begin(); it != cavelist.end(); it++)
	{
		if ((*it)->name() == a)
			return *it;
	}
	return 0;
}

cave *caveNetwork::create(const char *a)
{
	cave   *new_cave = new cave(a);
	//printf("New cave: %s\n", new_cave->name().c_str());
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
	if (!ac) ac = create(a);
	if (!bc) bc = create(b);
	//printf("Connecting %s(%c) <--> %s(%c)\n", a, (ac?'*':'-'), b, (bc?'*':'-'));
	ac->connect(bc);
	bc->connect(ac);
	return cavelist.size();
}

void cavepath_out(vector<cave *> &l, cave *c)
{
	vector<cave *>::iterator li = l.begin();
	printf("%3d :: %s", l.size(), (*li)->name().c_str());
	li++;
	for (; li != l.end(); li++)
	{
		printf(" -- %s", (*li)->name().c_str());
	}
	if (c) printf( " -- %s", c->name().c_str());
	printf("\n");
}

int	caveNetwork::paths(vector<cave *> &path, cave *node, bool debug)
{

	if (!node) 
	{
		printf("NULL Node\n");
		cavepath_out(path, 0);
		path.erase(path.end()-1);
		cave *nn = path.back();
		paths(path, nn->next(), debug);
	}
	printf("Node: %s\n", node->name().c_str());	
	if (node->name() == "start")
	{
		path.push_back(node);
		paths(path, node->next(), debug);
	}
	if (node->name() == "end")
	{
		path_count++;
		printf("SUCCESSFULL path - "); 
		cavepath_out(path, node);
		cave *last_node = *(path.end()-1);
		printf ("Last node: %s\n", last_node->name().c_str());
		//last_node->reset();	// reset this node so it can be used again
		//path.erase(path.end()-1);  // get rid of last node
		//cave *prev_node = path.back();
		//cave *next_node = prev_node->next();
		//while (!next_node)
		//{
		//   path.erase(path.end()-1);
		//   prev_node = path.back();
		//   next_node = prev_node->next();
		//}
		paths(path, last_node->next(), debug);
	}
	else if (node->is_small())
	{
		if (path.size() == 0)
		{
			printf("GOT HERE 1: %s\n", node->name().c_str());
			path.push_back(node);
			cave *nn = node->next();
			if (nn)
			  paths(path, nn, debug);
		    printf("A:FAILED path - "); 
			cavepath_out(path, node);
			// remove last node 
			// restart path
			path.erase(path.end()-1);
			nn = path.back();
			paths(path, nn->next(), debug);
		}
		else
		{
			printf("GOT HERE 2 - %s\n", node->name().c_str());

			cave *nn = node->next();
			if (!nn)
			{
				printf("B:FAILED path - "); 
				cavepath_out(path, node);
				//path.erase(path.end()-1);
				//cave *_node = *(path.end());
				paths(path, node->next(), debug);
			}
			else
			{
				path.push_back(node);
				paths(path, nn, debug);
			}
		}
	} 
	else
	{
			printf("GOT HERE 3\n");
		path.push_back(node);
		for (cave *n = node; n; n = n->next())
		   paths(path, n, debug);
	}
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
}


#define MAXLINE 20000
void cave_paths(const char *v, int tPathCount)
{
	FILE *f = fopen(v, "r");
	char c[MAXLINE];
	fgets(c, MAXLINE, f);
	caveNetwork cn;
	while (!feof(f))
	{
		parseline(cn, c);
		fgets(c, MAXLINE, f);
	}
	printf("Input file: %s\n", v);
	//cn.display();
	cn.reset();
	vector<cave *> cpath;
	cn.paths(cpath, path_head, false);
	
	fclose(f);
}

int main(int argc, char **argv)
{
	cave_paths("ex.txt", 100);

	return 0;
}
