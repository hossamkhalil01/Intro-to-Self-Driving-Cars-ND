#include "headers/normalize.h"
using namespace std;

// OPTIMIZATION: Pass variable by reference
vector< vector<float> > normalize(vector< vector <float> > &grid) {

  	// OPTIMIZATION: Avoid declaring and defining 				
	// intermediate variables that are not needed.

	int h = grid.size();
	int w = grid[0].size();
	static float total = 0.0;
	
	int i,j;

	for (i = 0; i <h; i++)
	{
		for (j=0; j<w; j++)
		{
			total += grid[i][j];
		}
	}
	

	for (i = 0; i < h; i++) 
	{
		for (j=0; j< w; j++) 
		{
			grid[i][j] =grid[i][j]/ total;
		}
	}

	return grid;
}
