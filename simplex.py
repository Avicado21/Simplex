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
    #we take the inputs and then run the simplex until our reduced costs are all negative, which means we are at an optimal point.
    #that is, for the maximization route
    
    #I'll handle the unboundness, infeasibility and mismatch cases later:
    #so first assumption is that the things match properly
    
    #step 0: find a basic feasible point
    #next assumption is assuming identity matrix in the basis
    row, col = A.shape  # row = m (constraints), col = n (variables)
    
    # Track basis by column indices, not by copying columns
    # Initially: slack variables (last m columns) are basic, original variables are nonbasic
    basis = list(range(col - row, col))      # e.g., [2, 3, 4] for 3x5 matrix
    nonbasis = list(range(col - row))        # e.g., [0, 1]
    
    # get our x vector
    # nonbasic vars = 0, basic vars = b (works because B = I, so x_B = B⁻¹b = b)
    x = np.zeros(col)
    x[basis] = b
    
    print(f"Initial x = {x}, objective = {c @ x}")
    
    #step 1: reduced costs
    #r = cNT − cBT AB-1 AN
    
    done = False
    
    # while not done, we keep on doing each pivot and iteration
    # this is maximizing route
    while(not done):
        
        # extract current basis and nonbasis matrices from A
        AB = A[:, basis]
        AN = A[:, nonbasis]
        cB = c[basis]
        cN = c[nonbasis]
        
        # reduced costs: how much objective improves per unit increase in each nonbasic var
        costs = cN - cB @ np.linalg.solve(AB, AN)
        
        print(f"Reduced costs: {costs}")
        
        # for maximization: all reduced costs <= 0 means optimal
        if np.all(costs <= 0):
            done = True
            
        else:
            # find the entering variable (largest positive reduced cost)
            entering_idx = np.argmax(costs)       # index within nonbasis list
            entering = nonbasis[entering_idx]     # actual column index in A
            
            # get the direction vector
            # d = B⁻¹ * a_j tells us how basic vars change per unit increase in entering var
            d = np.linalg.solve(AB, A[:, entering])
            
            # now we have the direction vector, we need to find the step size
            # we do this by finding the minimum ratio of xB / dB for all positive entries in dB
            x_B = x[basis]
            ratios = np.full(row, np.inf)
            
            for i in range(row):
                if d[i] > 0:
                    ratios[i] = x_B[i] / d[i]
                    
            step_size = np.min(ratios)
            leaving_idx = np.argmin(ratios)   # index within basis list
            leaving = basis[leaving_idx]       # actual column index in A
            
            # now we update our x vector
            # basic vars decrease along direction d
            x[basis] -= step_size * d
            # entering var was 0, now becomes step_size
            x[entering] = step_size
            # leaving var becomes 0 (now nonbasic)
            x[leaving] = 0
            
            # swap the entering and leaving variables in our index lists
            basis[leaving_idx] = entering
            nonbasis[entering_idx] = leaving
            
            print(f"Pivot: x{entering+1} enters, x{leaving+1} leaves")
            print(f"x = {x}, objective = {c @ x}")
    
    print(f"\nOptimal: x = {x}, objective = {c @ x}")
    
    return x, c @ x
    


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