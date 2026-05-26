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


#alright 2 phase simplex check:
def needs_two_phase(A):
    row, col = A.shape
    
    # Check if last m columns form identity matrix
    I_check = A[:, -row:]
    
    if np.allclose(I_check, np.eye(row)):
        return False  # Easy basis exists, one-phase is fine
    else:
        return True   # Need two-phase

def doSimplex(A, b, c, basis=None):
    #we take the inputs and then run the simplex until our reduced costs are all negative, which means we are at an optimal point.
    #that is, for the maximization route
    
    #I'll handle the unboundness, infeasibility and mismatch cases later:
    #so first assumption is that the things match properly
    
    row, col = A.shape
    
    #step 0: find a basic feasible point
    if basis is None:
        # assume identity matrix in last m columns
        basis = list(range(col - row, col))
    else:
        # use provided basis
        basis = list(basis)  # copy to avoid mutating original
    
    # nonbasis is everything not in basis
    nonbasis = [i for i in range(col) if i not in basis]
    
    # get our x vector
    x = np.zeros(col)
    AB = A[:, basis]
    x[basis] = np.linalg.solve(AB, b)  # handles non-identity basis too
    
    # ... rest stays the same
    
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
            
            # unboundedness check: if no positive d entries, we can go to infinity
            if np.all(d <= 0):
                print("Problem is unbounded!")
                return None, np.inf
            
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
    
    return x, c @ x, basis

def two_phase_simplex(A, b, c):
    row, col = A.shape
    
    # Phase I: build augmented problem
    A_phase1 = np.hstack([A, np.eye(row)])
    c_phase1 = np.concatenate([np.zeros(col), -np.ones(row)])
    
    # Run simplex on Phase I
    x_phase1, obj_phase1, basis_phase1 = doSimplex(A_phase1, b, c_phase1)
    
    # Check feasibility
    if not np.isclose(obj_phase1, 0):
        print("Problem is infeasible")
        return None, None, None
    
    # Phase II: extract basis indices that are in original problem (< col)
    # Filter out any artificial variables still in basis
    basis_for_phase2 = [i for i in basis_phase1 if i < col]
    
    # If artificials still in basis at zero value, need to handle
    if len(basis_for_phase2) < row:
        print("Warning: artificial variable in basis (degenerate case)")
        # For now, just proceed — advanced handling needed for full robustness
    
    x, obj, basis = doSimplex(A, b, c, basis=basis_for_phase2)
    return x, obj, basis

    


def main():
    #initialze variables, in this case the arrays for the method.
    '''
    A = getArrayInput("Enter in array A: ")
    b = getArrayInput("Enter in array B: ")
    c = getArrayInput("Enter in array C: ")
    '''
    #make test A, b and c
    
    '''
    #basic feasible check
    A = np.array([[1, 1, 1, 0, 0], [1, 0, 0, 1, 0], [0, 1, 0, 0, 1]], dtype=float)

    b = np.array([4, 3, 2], dtype=float)

    c = np.array([3, 2, 0, 0, 0], dtype=float)
    '''
    
    '''
    #unbounded check
    # Maximize 2x₁ + x₂
    # Subject to:
    #   -x₁ + x₂ ≤ 1
    #    x₁ - x₂ ≤ 1
    #   x₁, x₂ ≥ 0

    A_unbounded = np.array([[-1, 1, 1, 0], [1, -1, 0, 1]], dtype=float)

    b_unbounded = np.array([1, 1], dtype=float)

    c_unbounded = np.array([2, 1, 0, 0], dtype=float)
    '''
    
    #now for the method calls
    #doSimplex(A, b, c)
    #doSimplex(A_unbounded, b_unbounded, c_unbounded)
    
    #two phase edition:
    # Maximize x₁ + x₂
    # Subject to:
    #   x₁ + 2x₂ = 4
    #   2x₁ + x₂ = 5
    #   x₁, x₂ ≥ 0

    A_twophase = np.array([[1, 2],
                            [2, 1]], dtype=float)
    b_twophase = np.array([4, 5], dtype=float)
    c_twophase = np.array([1, 1], dtype=float)
    
    if needs_two_phase(A_twophase):
        x, obj, basis = two_phase_simplex(A_twophase, b_twophase, c_twophase)
    else:
        x, obj, basis = doSimplex(A_twophase, b_twophase, c_twophase)
    










if __name__ == "__main__":
    main()