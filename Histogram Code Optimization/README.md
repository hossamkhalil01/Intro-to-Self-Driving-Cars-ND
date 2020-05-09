#Overview

This project is an optimization for an already exicted C++ histogram filter code (both are provided) to make more efficient and faster to execute.

It can be used as a demonstration of what aspects to look for while optimizing the code and how big of a difference can it make.


#Demo

Execution time for each function before optimization is:

![orig](https://user-images.githubusercontent.com/47195928/81477366-c4b01a80-9217-11ea-8ae7-f23ae64b3934.JPG)


Execution time for each function after optimization is:

![res](https://user-images.githubusercontent.com/47195928/81477374-d1347300-9217-11ea-9d8b-8046b7d95a13.JPG)


#Description

There are two projects the original conde and its optimized version. Some of the files included in each project are:



##blur.cpp:
Changes the position beliefs after each movement step.

##sense.cpp:
Perform the measurement step according to the initialized world map.

##main.cpp:
The main program as it iterates multiple times over each function while computing the execution time and outputs the results.



#Instructions

Compile using c++11 standard, an example of compiling command using g++ compiler is:

`g++ -std=c++11 main.cpp blur.cpp initialize_beliefs.cpp move.cpp normalize.cpp print.cpp sense.cpp zeros.cpp`

**Note**: The project is already compiled and provided as (main.exe) file

