/**
	localizer.cpp

	Purpose: implements a 2-dimensional histogram filter
	for a robot living on a colored cyclical grid by 
	correctly implementing the "initialize_beliefs", 
	"sense", and "move" functions.

	This file is incomplete! Your job is to make these
	functions work. Feel free to look at localizer.py 
	for working implementations which are written in python.
*/

#include "localizer.h"
#include "helpers.cpp"
#include <stdlib.h>
#include "debugging_helpers.cpp"
#include <cstdlib>


using namespace std;

/**
	TODO - implement this function 
    
    Initializes a grid of beliefs to a uniform distribution. 

    @param grid - a two dimensional grid map (vector of vectors 
    	   of chars) representing the robot's world. For example:
    	   
    	   g g g
    	   g r g
    	   g g g
		   
		   would be a 3x3 world where every cell is green except 
		   for the center, which is red.

    @return - a normalized two dimensional grid of floats. For 
           a 2x2 grid, for example, this would be:

           0.25 0.25
           0.25 0.25
*/

vector< vector <float> > initialize_beliefs(vector< vector <char> > grid) {
	
	// your code here

	//Calculate the distributed probability
	float norm_prob = 1.0 / (grid.size()*grid[0].size());

	//return new Grid with norm_prob values
	vector <vector<float> > newGrid (grid.size(),vector<float> (grid[0].size(),norm_prob));
	return newGrid;
}

/**
  TODO - implement this function 
    
    Implements robot motion by updating beliefs based on the 
    intended dx and dy of the robot. 

    For example, if a localized robot with the following beliefs

    0.00  0.00  0.00
    0.00  1.00  0.00
    0.00  0.00  0.00 

    and dx and dy are both 1 and blurring is 0 (noiseless motion),
    than after calling this function the returned beliefs would be

    0.00  0.00  0.00
    0.00  0.00  0.00
    0.00  0.00  1.00 

  @param dy - the intended change in y position of the robot

  @param dx - the intended change in x position of the robot

    @param beliefs - a two dimensional grid of floats representing
         the robot's beliefs for each cell before sensing. For 
         example, a robot which has almost certainly localized 
         itself in a 2D world might have the following beliefs:

         0.01 0.98
         0.00 0.01

    @param blurring - A number representing how noisy robot motion
           is. If blurring = 0.0 then motion is noiseless.

    @return - a normalized two dimensional grid of floats 
         representing the updated beliefs for the robot. 
*/
vector< vector <float> > move(int dy, int dx, 
  vector < vector <float> > beliefs,
  float blurring) 
{
	// your code here

	//Store the dimensions of the grid
	int h = beliefs.size();
	int w = beliefs[0].size();

	//Init the new grid
	vector < vector <float> > newGrid (h,vector<float> (w,0.0));

	//Variables to hold the new position after shifting
	int new_i ;
	int new_j ;


	/*A complete rotation removal (to keep the boundries conditions valid)*/
	
	//Check the complete rotation condition in Y direction
	if (abs(dy) >= h)
	{
		//Remove it from the shifting steps
		if (dy > 0)
		{
			dy-=h;
		}
		else  if (dy<0)
		{
			dy+=h;
		}
	}

	//Check the complete rotation condition in X direction
	if (abs(dx) >= w)
	{
		//Remove it from the shifting steps
		if (dx > 0)
		{
			dx-=w ;
		}
		else  if (dx<0)
		{
			dx+=w;
		}
	}

	//Shifting the Grid 
	for (int i = 0 ; i < h ; i++)
	{
		//Defining the y axis boundries
		if (i + dy < 0)
		{
			new_i = (h - (dy - i)) % h ; 
		}
		else 
		{
			new_i = (i + dy)%h;
		}
		for (int j = 0 ; j < w ; j++)
		{
			//Defining the x axis boundries	
			if (j + dx < 0)
			{
				new_j = (w - (dx - j )) % w;
			}
			else 
			{
				new_j = (j + dx)%w;
			}

			//Assign the new value
			newGrid[new_i][new_j] = beliefs[i][j];
		}
	
	    /*for (int i = 0 ; i < h ; i++)
		{
        for (int j = 0 ; j < w ; j++)
		{
            new_i = (i + dy ) % h;
            new_j = (j + dx ) % w;
            newGrid[new_i][new_j] = beliefs[i][j];
		}*/
		}
	return blur(newGrid, blurring);
}


/**
	TODO - implement this function 
    
    Implements robot sensing by updating beliefs based on the 
    color of a sensor measurement 

	@param color - the color the robot has sensed at its location

	@param grid - the current map of the world, stored as a grid
		   (vector of vectors of chars) where each char represents a 
		   color. For example:

		   g g g
    	   g r g
    	   g g g

   	@param beliefs - a two dimensional grid of floats representing
   		   the robot's beliefs for each cell before sensing. For 
   		   example, a robot which has almost certainly localized 
   		   itself in a 2D world might have the following beliefs:

   		   0.01 0.98
   		   0.00 0.01

    @param p_hit - the RELATIVE probability that any "sense" is 
    	   correct. The ratio of p_hit / p_miss indicates how many
    	   times MORE likely it is to have a correct "sense" than
    	   an incorrect one.

   	@param p_miss - the RELATIVE probability that any "sense" is 
    	   incorrect. The ratio of p_hit / p_miss indicates how many
    	   times MORE likely it is to have a correct "sense" than
    	   an incorrect one.

    @return - a normalized two dimensional grid of floats 
    	   representing the updated beliefs for the robot. 
*/
vector< vector <float> > sense(char color, 
	vector< vector <char> > grid, 
	vector< vector <float> > beliefs, 
	float p_hit,
	float p_miss) 
	
{
	bool hit;
	//Init the new output grid 
	vector<vector<float> > newGrid (beliefs.size(),vector<float> (beliefs[0].size(),0.0));

	// Assign the new grid values according to the 
	for (int i =0 ; i < grid.size() ; i++)
	{
		for(int j = 0 ; j < grid[0].size() ; j++)
		{
			//Check if it's hit or miss
			hit =(grid[i][j] == color);

			//scale by the hit or miss factor according to the condition
			newGrid[i][j] = hit*beliefs[i][j]*p_hit + (1-hit)*beliefs[i][j]*p_miss;

		}

	}
	return normalize(newGrid);
}