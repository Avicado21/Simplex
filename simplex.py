'''
Avinash Kottakota
A simple simplex custom implementation in python
Derived from my experience in Introduction to Optimization
'''

#simple simplex imports
from typing import Optional
from enum import Enum
from dataclasses import dataclass
import numpy as np

# need a given A, b, c, and x0
# A is the constraint matrix, b is the constraint vector, c is the cost vector,
# and x0 is the initial basic feasible solution

# have to handle terminal array input efficiently
def getArrayInput(prompt):
    
    print(prompt)
    
    array = []
    
    rows = input("enter number of rows: ")
    cols = input("enter number of columns: ")
    
    row = int(rows)
    col = int(cols)
    
    for i in range(row):
        r = input(f"enter row {i+1} values separated by space: ")
        vals = list(int(x) for x in r.split())
        if len(vals) != col:
            print(f"Error: expected {col} values, got {len(vals)}. Please try again.")
            return getArrayInput(prompt)
        array.append(vals)
        
    np_array = np.array(array)
    
    #print(np_array)
    
    return np_array

# do simplex starts with basic maximization,
def doSimplex(A, b, c):
    #we take the inputs and then run the simplex until our reduced costs are all non-negative, which means we are at an optimal point.
    
    #I'll handle the unboundness, infeasibility and mismatch cases later:
    #so first assumption is that the things match properly
    
    #step 0: find a basic feasible point
    #next assumption is assuming identity matrix in the basis
    r = A.shape[0]
    c = A.shape[1]
    
    x = np.zeros(c);
    
    Id = np.eye(r)
    AB = A[:, r:]
    
    
    #check assumption:
    if np.array_equal(AB, Id):
        print("okay")
    else:
        print("bruh")
        
    #if we proceed then the reverse layout of b will be the last entries in the x vector
    x[-r:] = b
    
    
    
    #step 1: reduced costs
    #r = cNT − cBT AB-1 AN
    
        
    
    


def main():
    #initialze variables, in this case the arrays for the method.
    A = getArrayInput("Enter in array A: ")
    B = getArrayInput("Enter in array B: ")
    C = getArrayInput("Enter in array C: ")
    
    #now for the method
    doSimplex(A, B, C)
    










if __name__ == "__main__":
    main()