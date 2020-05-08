import math
from math import sqrt
import numbers

#Creating  a matrix object of zeroes
def zeroes(m,n):
    #Checking if both m and n are less than 1
    if (m < 1 or n < 1)  :
        raise ValueError('Invalid Input Dimensions!')       
    return Matrix([[0.0 for j in range(n)]for i in range(m)])

#Creating  Identity matrix object of (nxn) size
def identity(n):
    #Check the input argument
    if n < 1:
        raise ValueError('Invalid Input Dimensions!')
    #initialize the matrix
    iden = zeroes(n,n)

    for i in range(n):
        #Filling the Diagonal
        iden[i][i] = 1    
    return iden

class Matrix (object):
    
    #Initialize the class 
    def __init__ (self,grid):
        
        #checking the input dimensions
        if (len(grid) <1) or (len(grid[0])<1):
            raise ValueError('Invalid input! Empty list')
            
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])
 
    #Checks if a matrix is square    
    def is_square(self):
        return self.h == self.w
  
    #Get row vector of index m  in a matrix
    def get_row (self,m):
        return self.g[m]
    
    #Get column vector of index n in a matrix
    def get_col (self,n):
        
        #check the input index
        if (n > self.w):
            raise ValueError('Index out of range!')

        #Return the required column    
        return  [self.g[i][j] for j in range(self.w) for i in range(self.h) if j==n]  
      
    #Calculate Determinant for up to 2x2 matrix
    def determinant (self):  
        #Check if the matrix is square
        if not self.is_square():
            raise ValueError('Cannot calculate determinant of non-square matrix.')
            
        
        #check dimensions bigger than 2x2
        if self.w >2 or self.h > 2:
            raise NotImplementedError("Calculating determinant not implemented for matrices largerer than 2x2.")
            
        
        #implement 1x1 determinant
        if self.h == 1:
            return self.g[0][0]
        
        
        elif self.h == 2:
            ad = self.g[0][0] * self.g[1][1]
            bc = self.g[0][1] * self.g[1][0]
   
            return (ad - bc)
       
    #Calculate the trace of a matrix
    def trace (self): 
        #Check if the matrix is square
        if not self.is_square():
            raise ValueError('Cannot calculate trace of non-square matrix.')
        
        #Calculate sum of the main diagonal
        trace = 0
        for i in range(self.h):
            trace += self.g[i][i]
        return trace

    #Calculate the transpose of a matrix
    def T (self):

        return Matrix([[self.g[j][i] for j in range(self.h)] for i in range(self.w)])
        
    #Calculate inverse for up to 2x2 matrix
    def inverse (self):  
        #Check if the matrix is square
        if not self.is_square():
            raise ValueError('Non-square Matrix does not have an inverse.')
        
        #check dimensions bigger than 2x2
        if self.w >2 or self.h > 2:
            raise NotImplementedError("inversion not implemented for matrices larger than 2x2.")
        
        #inverse for 1x1 
        if self.h == 1:
            inv = [[1.0/self.g[0][0]]]
            return Matrix(inv)
        
        #inverse for 2x2 
        elif self.h == 2:
            #Create a grid of the same dimensions
            inv = zeroes(self.h,self.w)
            
            #Compute the determinant
            det = self.determinant()
            
            #Calculate the inverse
            inv[0][0] = self.g[1][1]/det
            inv[0][1] = -1*self.g[0][1]/det
            inv[1][0] = -1*self.g[1][0]/det
            inv[1][1] = self.g[0][0]/det
            
            return inv
            

    ###########################
    ###Operators Overloading###
    ###########################

    #Indexing
    def __getitem__ (self,idx):   
        return self.g[idx]

    #Printing behavior of an object of the class
    def __repr__(self):
        #initialize a string
        p = ""
        #return string of each row + new line
        for row in self.g:
            p += str(row) + "\n"
        return p
                  
    #Performing addition
    def __add__(self,other):   
        #Checking that both have the same dimensions
        if  (self.w != other.w) or (self.h != other.h):
            raise  ValueError('Matrices of un equal dimensions can\'t be added')
            
        return Matrix([[other[i][j]+self.g[i][j] for i in range(self.h)] for j in range(self.w)])

    #The negative operator
    def __neg__(self):
        #invert the sign of each element
        return Matrix([[-self.g[i][j] for j in range(self.w)] for i in range(self.h)])
 
    #Performing Subtraction
    def __sub__(self,other): 

        #inverting the sign to perform addition
        return (self + (-1*other))
       
    #Performing Multiplication
    def __mul__(self,other):

        #Check dimensions
        if (self.w != other.h):
            raise ValueError('Dimennsions not correct multiplication can\'t be performed')
        
        #Utilizing matrix transpose in multiplication
        other_T = other.T()
        
        #Init mult result matrx
        mul = zeroes(self.h,other.w) 
        
        #Multiplication
        for i,row in enumerate(self.g):
            for j,col in enumerate(other_T):
                #dot product of the two vectors
                dot_sum = 0
                for ind in range(len(row)):
                    dot_sum += (row[ind]*col[ind])
                mul[i][j] = dot_sum
                    
        return mul  
                           
    #Matrix Scaling (multiplying by a scalar)
    def __rmul__(self,other): 
        
        #Check the data type of the input
        if not isinstance(other, numbers.Number):
            raise ValueError('This Data type can\'t be multiplied')
            
        #scaling each element by factor (Other)
        return Matrix([[other*self.g[i][j] for j in range(self.w)]for i in range(self.h)])