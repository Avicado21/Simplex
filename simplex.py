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
    
    print(np_array)
    
    return np_array

def doSimplex(A, b, c, x0):
    #we take the inputs and then run the simplex until our reduced costs are all negative or zero
    
    #step 0: find a basic feasible point
    
    #step 1: reduced costs
        
    
    


def main():
    #initialze variables, in this case the arrays for the method.
    A = getArrayInput("Enter in array A: ")
    B = getArrayInput("Enter in array B: ")
    C = getArrayInput("Enter in array C: ")
    x0 = getArrayInput("Enter in array x0: ")
    
    #now for the method
    










if __name__ == "__main__":
    main()