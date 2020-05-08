#include "headers/zeros.h"

using namespace std;

vector < vector <float> > zeros(int height, int width) {


	// OPTIMIZATION: Reserve space in memory for vectors
	vector < vector <float> > newGrid (height, vector<float> (width,0.0));

	return newGrid;
}