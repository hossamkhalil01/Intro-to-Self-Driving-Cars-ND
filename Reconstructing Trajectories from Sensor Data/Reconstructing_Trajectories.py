#!/usr/bin/env python
# coding: utf-8

# ## Raw Input Data
# 
# The data you'll be working with has been preprocessed from CSVs that looks like this:
# 
# | timestamp | displacement  | yaw_rate | acceleration |
# | :-------: | :----------: | :------: | :----------: |
# | 0.0 | 0 | 0.0 | 0.0 |
# | 0.25 | 0.0 | 0.0 | 19.6 |
# | 0.5 | 1.225 | 0.0 | 19.6 |
# | 0.75 | 3.675 | 0.0 | 19.6 |
# | 1.0 | 7.35 | 0.0 | 19.6 |
# | 1.25 | 12.25 | 0.0 | 0.0 |
# | 1.5 | 17.15 | -2.82901631903 | 0.0 |
# | 1.75 | 22.05 | -2.82901631903 | 0.0 |
# | 2.0 | 26.95 | -2.82901631903 | 0.0 |
# | 2.25 | 31.85 | -2.82901631903 | 0.0 |
# | 2.5 | 36.75 | -2.82901631903 | 0.0 |
# | 2.75 | 41.65 | -2.82901631903 | 0.0 |
# | 3.0 | 46.55 | -2.82901631903 | 0.0 |
# | 3.25 | 51.45 | -2.82901631903 | 0.0 |
# | 3.5 | 56.35 | -2.82901631903 | 0.0 |
# 
# This data is currently saved in a file called `trajectory_example.pickle`. It can be loaded using a helper function we've provided (demonstrated below):

# In[1]:


from helpers import process_data
from math import cos,sin,pi
from matplotlib import pyplot as plt


data_list = process_data("trajectory_example.pickle")

for entry in data_list:
    print(entry)


# as you can see, each entry in `data_list` contains four fields. Those fields correspond to `timestamp` (seconds), `displacement` (meters), `yaw_rate` (rads / sec), and `acceleration` (m/s/s).
# 
# ### The Point of this Project!
# **Data tells a story but you have to know how to find it!** 
# 
# Contained in the data above is all the information you need to reconstruct a fairly complex vehicle trajectory. After processing **this** exact data, it's possible to generate this plot of the vehicle's X and Y position:
# 
# ![](https://d17h27t6h515a5.cloudfront.net/topher/2017/December/5a3044ac_example-trajectory/example-trajectory.png)
# 
# as you can see, this vehicle first accelerates forwards and then turns right until it almost completes a full circle turn.
# 
# ### Data Explained
# 
# **`timestamp`** - Timestamps are all measured in seconds. The time between successive timestamps ($\Delta t$) will always be the same *within* a trajectory's data set (but not *between* data sets).
# 
# **`displacement`** - Displacement data from the odometer is in meters and gives the **total** distance traveled up to this point.
# 
# **`yaw_rate`** - Yaw rate is measured in radians per second with the convention that positive yaw corresponds to *counter-clockwise* rotation. 
# 
# **`acceleration`** - Acceleration is measured in $\frac{m/s}{s}$ and is always **in the direction of motion of the vehicle** (forward). 
# 
# > **NOTE** - you may not need to use all of this data when reconstructing vehicle trajectories.

# ## Your Job
# Your job is to complete the following functions, all of which take a processed `data_list` (with $N$ entries, each $\Delta t$ apart) as input:
# 
# * `get_speeds` - returns a length $N$ list where entry $i$ contains the speed ($m/s$) of the vehicle at $t = i \times \Delta t$ 
# 
# * `get_headings` - returns a length $N$ list where entry $i$ contains the heading (radians, $0 \leq \theta < 2\pi$) of the vehicle at $t = i \times \Delta t$
# 
# * `get_x_y` - returns a length $N$ list where entry $i$ contains an `(x, y)` tuple corresponding to the $x$ and $y$ coordinates (meters) of the vehicle at $t = i \times \Delta t$ 
# 
# * `show_x_y` - generates an x vs. y scatter plot of vehicle positions. 

# In[2]:


# I've provided a solution file called solution.py
# You are STRONGLY encouraged to NOT look at the code
# until after you have solved this yourself.
#
# You SHOULD, however, feel free to USE the solution 
# functions to help you understand what your code should
# be doing. For example...
from helpers import process_data
import solution

data_list = process_data("trajectory_example.pickle")
solution.show_x_y(data_list)


# In[3]:


# What about the other trajectories?

three_quarter_turn_data = process_data("trajectory_1.pickle")
solution.show_x_y(three_quarter_turn_data, increment=10)


# In[4]:


merge_data = process_data('trajectory_2.pickle')
solution.show_x_y(merge_data,increment=10)


# In[5]:


parallel_park = process_data("trajectory_3.pickle")
solution.show_x_y(parallel_park,increment=5)


# **How do you make those cool arrows?!**
# 
# I did a Google search for "python plot grid of arrows" and the second result led me to some [demonstration code](https://matplotlib.org/examples/pylab_examples/quiver_demo.html) that was really helpful. 

# ## Testing Correctness
# Testing code is provided at the bottom of this notebook. Note that only `get_speeds`, `get_x_y`, and `get_headings` are tested automatically. You will have to "test" your `show_x_y` function by manually comparing your plots to the expected plots. 

# ### Initial Vehicle State
# 
# The vehicle always begins with all state variables equal to zero. This means `x`, `y`, `theta` (heading), `speed`, `yaw_rate`, and `acceleration` are 0 at t=0.

# ----

# ## Your Code!
# Complete the functions in the cell below. I recommend completing them in the order shown. Use the cells at the end of the notebook to test as you go.

# In[6]:


def get_speeds(data_list):
    

    time = [p[0] for p in data_list] 
    accele = [p[3] for p in data_list]
    speed = []
    integral = 0
    speed.append(integral)
    
    for i in range(1,len(time)):
        integral+= accele[i]*(time[i]-time[i-1])
        speed.append(integral)
    return speed
    

def get_headings(data_list):
    
    time =  [p[0] for p in data_list] 
    yaw_rate =  [p[2] for p in data_list] 
    
    headings = []
    integral = 0
    headings.append(integral)
    
    for i in range(1,len(time)):
        
        integral+= yaw_rate[i]*(time[i]-time[i-1])
        #Remove a complete rotations
        integral %= (2*pi)
        headings.append(integral)        
    return headings


def get_x_y(data_list):
    
    displacement = [p[1] for p in data_list]    
    theta = get_headings(data_list)

    x_y = []
    x =0
    y =0
    x_y.append((x,y))
    
    for i in range(1,len(displacement)):
        x += (displacement[i]-displacement[i-1])* cos(theta[i])
        y += (displacement[i]-displacement[i-1])* sin(theta[i])
        
        x_y.append((x,y))
        
    return x_y


def show_x_y(data_list):
    x_y = get_x_y(data_list)
    X = [p[0] for p in x_y]
    Y = [p[1] for p in x_y]
    
    plt.scatter(X,Y)
    plt.title('X , Y Trajectory')
    plt.xlabel('Displacement in X')
    plt.ylabel('Displacement in Y')    
    plt.show()
    return


# ## Testing
# Test your functions by running the cells below.

# In[7]:


from testing import test_get_speeds, test_get_x_y, test_get_headings

test_get_speeds(get_speeds)


# In[8]:


test_get_headings(get_headings)


# In[83]:


test_get_x_y(get_x_y)


# In[9]:


show_x_y(data_list) #Trajectory 1


# In[10]:


show_x_y(three_quarter_turn_data) #Trajectory 2


# In[11]:


show_x_y(merge_data)  #Trajectory 3


# In[12]:


show_x_y(parallel_park)  #Trajectory 4


# In[ ]:




