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
    
    rows = input("enter number of rows")
    cols = input("enter number of columns")
    
    for i in range(rows):
        row = input(f"enter row {i+1} values separated by space")
        row_values = list(map(float, row.split()))
        if len(row_values) != cols:
            print("Invalid number of columns. Please try again.")
            return getArrayInput(prompt)
        array.append(row_values)
        
    return np.array(array)
    
    


def main():
    #initialze variables
    
    A = getArrayInput("Enter in array A")
    print(A)










if __name__ == "__main__":
    main()