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
    
    # get our x vector
    x = np.zeros(c);
    
    # get id
    Id = np.eye(r)
    AB = A[:, r-1:]
    print(AB)
    print(Id)
    
    
    #check assumption:
    if np.array_equal(AB, Id):
        print("okay")
    else:
        print("bruh")
        
    #if we proceed then the reverse layout of b will be the last entries in the x vector
    x[-r:] = b
    print(x)
    
    
    
    #step 1: reduced costs
    #r = cNT − cBT AB-1 AN
    
    done = False
    
    # while not done, we keep on doing each pivot and iteration
    while(not done):
        # do things
        
        cNT = c[:c-r]
        cBT = c[c-r:]
        
        ABinv = np.linalg.inv(AB)
        AN = A[:, :c-r]
        
        costs = cNT - cBT @ ABinv @ AN
        
        print(costs)
        
    
    
    
        
    
    


def main():
    #initialze variables, in this case the arrays for the method.
    '''
    A = getArrayInput("Enter in array A: ")
    b = getArrayInput("Enter in array B: ")
    c = getArrayInput("Enter in array C: ")
    '''
    #make test A, b and c
    
    A = np.array([[1, 1, 1, 0, 0], [1, 0, 0, 1, 0], [0, 1, 0, 0, 1]], dtype=float)

    b = np.array([4, 3, 2], dtype=float)

    c = np.array([3, 2, 0, 0, 0], dtype=float)

    
    
    
    #now for the method
    doSimplex(A, b, c)
    










if __name__ == "__main__":
    main()